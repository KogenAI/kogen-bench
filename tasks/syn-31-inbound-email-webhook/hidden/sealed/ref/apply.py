import sys
ws = sys.argv[1]
def edit(path, old, new):
    p = f"{ws}/{path}"; s = open(p).read()
    assert old in s, f"missing in {path}: {old[:60]!r}"
    open(p, "w").write(s.replace(old, new, 1))

edit("lib/trackline/support/ticket.ex", '    field :priority, :string, default: "normal"\n',
     '    field :priority, :string, default: "normal"\n    field :requester_email, :string\n')
edit("lib/trackline_web/endpoint.ex", "    parsers: [:urlencoded, :multipart, :json],\n",
     "    parsers: [:urlencoded, :multipart, :json],\n    body_reader: {TracklineWeb.RawBodyReader, :read_body, []},\n")
edit("lib/trackline_web/router.ex", "  # Other scopes may use custom stacks.\n  # scope \"/api\", TracklineWeb do\n  #   pipe_through :api\n  # end\n",
     '  scope "/api", TracklineWeb do\n    pipe_through :api\n\n    post "/orgs/:slug/inbound-email", InboundEmailController, :create\n  end\n')
