## WIRE

Conformance checks only `/model` and `/reasoning/effort` in requests; instructions, prompts and other request fields are implementation-defined.

The following is the mechanically extracted fake-provider wire vocabulary, not an exact
request template. Legacy fixture predicates for instructions, inputs, tools and
`parallel_tool_calls` do not expand the request comparison boundary above.

### HTTP and requests

- Method: `POST`, JSON body. `KOGEN_PROVIDER_URL` is the complete endpoint URL;
  scripted endpoints end in `/scripts/<escaped-id>/responses`. The smoke case records
  `/v1/responses`; the fake also accepts `/backend-api/codex/responses` and any path
  ending in `/responses`.
- Literal role defaults: Shaper `{"model":"gpt-6.1-sol","reasoning":{"effort":"high"}}`;
  Builder `{"model":"gpt-6-luna","reasoning":{"effort":"max"}}`. The effort literal
  is `max`, not `maximum`.
- Other fields represented in fixtures: `instructions` (string), `input` (conversation
  array; predicates address `/input/1/content/0/text` and `/input/5/content/0/text`),
  `tools` (tool definitions), `stream:true` (smoke case), `parallel_tool_calls:false`,
  and `tool_choice:{"type":"allowed_tools","mode":"auto","tools":[...]}`.
  Allowed-tool entries use `{"type":"function","name":"<tool>"}`. These fields
  illustrate the fixture representation; exact prompts, ordering and tool-definition
  JSON are implementation-defined.

### Tools and arguments

Tool calls in fake responses have `type:"function_call"`, a string `call_id`, string
`name`, and `arguments` containing a JSON-encoded string. Dispatch the decoded arguments
and include the actual tool result in the next provider turn.

| Role | Tool name | Argument object exercised by the scripts |
|---|---|---|
| Shaper | `write` | `{"path":string,"content":string}`; both fields supplied |
| Shaper | `read` | Listed as permitted; no call or argument schema supplied |
| Shaper | `search` | Listed as permitted; no call or argument schema supplied |
| Builder | `shell` | `{"cmd":string}`; `cmd` supplied |
| Builder | `finish` | `{}` |
| Builder | `tool_output` | Listed as permitted by Quint; no call or argument schema supplied |

These are observed argument shapes. The extracted sources do not supply formal
`parameters` schemas, optional fields, or additional-property rules. Gherkin Builder
fixtures require `shell` and `finish`; Quint builders also list `tool_output`.

### Headers and identity

- Request header in script manifests: `Content-Type: application/json`.
  The smoke case observes `Authorization: Bearer kogen-fake-access-old`, then
  `Authorization: Bearer kogen-fake-access` after owned credential refresh.
- Injected auth supplies `tokens.access_token` and `tokens.account_id`; FAKES uses
  account `acct-test`. Saved-login fixtures distinguish `acct-default` and
  `acct-research`. The research-account check looks for `acct-research` in request
  headers (or its distinct synthetic access token); it does not pin an account-header
  name. No account-header spelling is defined in the extracted scripts/manifests.
- The signed ID-token claim for the account is
  `claims["https://api.openai.com/auth"]["chatgpt_account_id"]`
  (JSON Pointer `/https:~1~1api.openai.com~1auth/chatgpt_account_id`).
  OIDC fixtures also include `iss`, `sub`, `aud`, `iat`, `exp`, `email` and `nonce`;
  their issuer is `https://auth.openai.com`. Normal signature, issuer, expiry,
  state, nonce and PKCE validation still apply.
- Successful response header: `Content-Type: text/event-stream`. The fake's generated
  streams also send `Cache-Control: no-cache` and `Connection: close`.

### SSE and Shaper output

Frames are `event: <type>\ndata: <JSON>\n\n`; HTTP chunks need not align with frames.
Quint scripts emit `response.completed`; the generated smoke/Gherkin streams also emit
`response.output_item.done` before completion:

| Event type | JSON payload fields |
|---|---|
| `response.output_item.done` | `type`, `item` (one output item) |
| `response.completed` | `type`, `response:{id,status:"completed",output:[...]}`; `model`, `object` and `usage` occur in some fixtures |

Output items are either `function_call` as above (sometimes with `status:"completed"`),
or `{"type":"message","role":"assistant","content":[{"type":"output_text","text":string}]}`.
Generated message items additionally carry `id`, `status:"completed"` and
`annotations:[]`. Usage fields are `input_tokens`, `output_tokens`, optional
`input_tokens_details.cached_tokens`, `output_tokens_details.reasoning_tokens` and
`total_tokens`; some completions omit usage entirely. Malformed-SSE fixtures deliberately
send invalid JSON and are not successful completions.

The Shaper does not return a dedicated JSON Intent object in these scripts. It writes
`.kogen/intents/<slug>/intent.md` through `write`, optionally writes an acceptance source
under `.kogen/local/acceptance/`, then returns assistant text. The Intent content is
Markdown with YAML frontmatter `title` (string), `size` (`small` in the fixtures),
`domains` (string list), a brief, and `## Acceptance`, `## Verify`, `## Notes` sections.
Acceptance uses `- A1: ...`; Verify maps that ID with `- A1: test domain=app`; Notes
starts with `Approach:`. Criteria-only fixtures write no acceptance source. Questions-only
fixtures return assistant `output_text` with a branching question and make no Intent or
acceptance-source write. Neither payload approves an Intent.

Extraction sources: `spec/features/FAKES.md`, `spec/quint/intent.qnt`'s `fixtureTurn`
and script builders, decoded `scripts` in `conformance/cases/**/*.manifest.json`,
`conformance/cases/04-shape-approve-queue-land.json`, and the fake/script builders in
`conformance/kogen_conformance/fake_provider.py` and `gherkin_runner.py`.
