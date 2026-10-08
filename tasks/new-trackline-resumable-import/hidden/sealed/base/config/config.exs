# This file is responsible for configuring your application
# and its dependencies with the aid of the Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.

# General application configuration
import Config

config :trackline, :scopes,
  user: [
    default: true,
    module: Trackline.Accounts.Scope,
    assign_key: :current_scope,
    access_path: [:user, :id],
    schema_key: :user_id,
    schema_type: :id,
    schema_table: :users,
    test_data_fixture: Trackline.AccountsFixtures,
    test_setup_helper: :register_and_log_in_user
  ]

config :trackline, Oban,
  engine: Oban.Engines.Lite,
  repo: Trackline.Repo,
  queues: [default: 10, webhooks: 5]

config :trackline,
  ecto_repos: [Trackline.Repo],
  generators: [timestamp_type: :utc_datetime]

# Configure the endpoint
config :trackline, TracklineWeb.Endpoint,
  url: [host: "localhost"],
  adapter: Bandit.PhoenixAdapter,
  render_errors: [
    formats: [html: TracklineWeb.ErrorHTML, json: TracklineWeb.ErrorJSON],
    layout: false
  ],
  pubsub_server: Trackline.PubSub,
  live_view: [signing_salt: "MQ1twsfq"]

# Configure LiveView
config :phoenix_live_view,
  # the attribute set on all root tags. Used for Phoenix.LiveView.ColocatedCSS.
  root_tag_attribute: "phx-r"

# Configure the mailer
#
# By default it uses the "Local" adapter which stores the emails
# locally. You can see the emails in your browser, at "/dev/mailbox".
#
# For production it's recommended to configure a different adapter
# at the `config/runtime.exs`.
config :trackline, Trackline.Mailer, adapter: Swoosh.Adapters.Local

# Configure Elixir's Logger
config :logger, :default_formatter,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

# Use Jason for JSON parsing in Phoenix
config :phoenix, :json_library, Jason

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{config_env()}.exs"
