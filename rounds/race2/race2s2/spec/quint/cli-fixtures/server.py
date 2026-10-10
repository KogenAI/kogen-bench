#!/usr/bin/env python3
"""Versioned loopback Responses/OpenID fixture server. Never start during generation.

server.py serve --script ID --port PORT --control DIR --label default|work
server.py browser URL                 (installed as open/xdg-open by manifest)
Each request and selected response is logged. Gates use control/GATE.arrived and
control/GATE.release; the IO runner's ProviderGate adapter uses those files.
"""
import argparse
import base64
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent

def b64(data):
    return base64.urlsafe_b64encode(data).decode().rstrip('=')

def encode(value):
    return json.dumps(value,separators=(',',':')).encode()

def signed(claims):
    head = b64(encode({'alg':'RS256','kid':'cli-fixture','typ':'JWT'}))
    body = b64(encode(claims))
    material = (head+'.'+body).encode()
    signature = subprocess.check_output(['openssl','dgst','-sha256','-sign',str(ROOT/'synthetic-key.pem')],input=material)
    return material.decode()+'.'+b64(signature)

def jwks():
    # OpenSSL exposes only the public modulus here; key is synthetic fixture data.
    text = subprocess.check_output(['openssl','rsa','-in',str(ROOT/'synthetic-key.pem'),'-noout','-modulus']).decode()
    modulus = bytes.fromhex(text.strip().split('=',1)[1])
    return {'keys':[{'kty':'RSA','kid':'cli-fixture','alg':'RS256','use':'sig','n':b64(modulus),'e':'AQAB'}]}

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):
        pass
    def send(self,status,body,content='application/json'):
        body = encode(body) if not isinstance(body,bytes) else body
        self.send_response(status)
        self.send_header('Content-Type',content)
        self.send_header('Content-Length',str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        url=urlsplit(self.path)
        base=f'http://127.0.0.1:{self.server.server_port}'
        if url.path.endswith('/.well-known/openid-configuration'):
            self.send(200,{'issuer':'https://auth.openai.com','authorization_endpoint':base+'/authorize','token_endpoint':base+'/token','jwks_uri':base+'/jwks','revocation_endpoint':base+'/revoke'})
        elif url.path=='/jwks':
            self.send(200,jwks())
        elif url.path=='/authorize':
            q=parse_qs(url.query)
            required={'client_id','ext_agent_host_id','response_type','redirect_uri','scope','resource','state','nonce','code_challenge_method','code_challenge'}
            assert required<=q.keys() and q['response_type']==['code'] and q['code_challenge_method']==['S256']
            assert urlsplit(q['redirect_uri'][0]).hostname=='127.0.0.1'
            code='cli-code-'+self.server.label
            self.server.authorized[code]=q
            self.server.record({'kind':'authorize','query':q})
            callback=q['redirect_uri'][0]+'?'+urlencode({'code':code,'state':q['state'][0]})
            with urlopen(callback,timeout=10) as response:
                response.read()
            self.send(200,{'done':True})
        else:
            self.send(404,{'error':'unexpected GET '+url.path})
    def do_POST(self):
        raw=self.rfile.read(int(self.headers.get('Content-Length','0')))
        path=urlsplit(self.path).path
        self.server.record({'kind':'request','path':path,'body':raw.decode(),'authorization':self.headers.get('Authorization')})
        if path=='/token':
            q=parse_qs(raw.decode())
            auth=self.server.authorized[q['code'][0]]
            assert b64(hashlib.sha256(q['code_verifier'][0].encode()).digest())==auth['code_challenge'][0]
            label=self.server.label
            claims={'iss':'https://auth.openai.com','aud':q['client_id'][0],'sub':'cli-'+label,'exp':4102444800,'nonce':auth['nonce'][0],'https://api.openai.com/auth':{'chatgpt_account_id':'cli-'+label}}
            self.send(200,{'access_token':'cli-'+label+'-access','refresh_token':'cli-'+label+'-refresh','id_token':signed(claims),'expires_in':2102444800,'scope':'openid profile email offline_access resource.invoke chatgpt.tokens.use.direct'})
        elif path=='/revoke':
            q=parse_qs(raw.decode())
            assert q['token']==['cli-'+self.server.label+'-refresh']
            assert q['token_type_hint']==['refresh_token']
            self.send(200,{})
        elif path.endswith('/responses'):
            with self.server.lock:
                index=self.server.ordinal
                self.server.ordinal+=1
            turns=self.server.script['turns']
            if index>=len(turns) and not self.server.script.get('repeat_last'):
                self.send(409,{'error':'unexpected Responses turn'})
                return
            turn=turns[min(index,len(turns)-1)]
            if 'gate' in turn:
                gate=turn['gate']
                (self.server.control/(gate+'.arrived')).touch()
                deadline=time.monotonic()+60
                while not (self.server.control/(gate+'.release')).exists():
                    if time.monotonic()>deadline:
                        self.send(504,{'error':'unreleased provider gate'})
                        return
                    time.sleep(.01)
            self.server.record({'kind':'response','ordinal':index,'response':turn})
            if turn['status']!=200:
                self.send(turn['status'],turn['body'])
            else:
                response={'id':'cli-response-'+str(index),'status':'completed','model':'gpt-6.1-sol','output':turn['output'],'usage':turn['usage']}
                event={'type':'response.completed','response':response}
                self.send(200,b'event: response.completed\ndata: '+encode(event)+b'\n\n','text/event-stream')
        else:
            self.send(404,{'error':'unexpected POST '+path})


def main():
    if len(sys.argv)>1 and sys.argv[1]=='browser':
        url=sys.argv[2]
        assert urlsplit(url).hostname=='127.0.0.1', 'browser fixture only accepts loopback'
        with urlopen(url,timeout=15) as response:
            response.read()
        return
    p=argparse.ArgumentParser()
    p.add_argument('serve',choices=['serve'])
    p.add_argument('--script',required=True)
    p.add_argument('--port',type=int,default=0)
    p.add_argument('--control',type=Path,required=True)
    p.add_argument('--label',choices=['default','work'],default='default')
    args=p.parse_args()
    scripts=json.loads((ROOT/'scripts.json').read_text())['scripts']
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    server.script=scripts[args.script]
    server.control=args.control
    server.control.mkdir(parents=True,exist_ok=True)
    server.label=args.label
    server.ordinal=0
    server.lock=threading.Lock()
    server.authorized={}
    def record(row):
        with server.lock:
            with (server.control/'transcript.jsonl').open('a') as f:
                f.write(json.dumps(row)+'\n')
    server.record=record
    print(f'http://127.0.0.1:{server.server_port}',flush=True)
    server.serve_forever()

if __name__=='__main__':
    main()
