import subprocess,sys
sys.exit(subprocess.call(["mix","test","test/generation_cache_test.exs"],cwd=sys.argv[1]))
