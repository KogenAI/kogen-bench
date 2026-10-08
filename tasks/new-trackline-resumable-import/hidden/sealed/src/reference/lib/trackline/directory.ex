defmodule Trackline.Directory do
  @moduledoc """
  Client for a partner's customer directory, used when onboarding a new
  organization: it can list the partner's contacts and download the full
  export archive.

  Every function takes `req_options`, merged into the request, so callers (and
  tests) can point it at a stub with `plug: {Req.Test, Name}`.
  """

  @doc """
  Lists contacts. The API answers with JSON like
  `{"contacts": [{"email": "a@b.c", "name": "A"}]}`; keys come back as atoms.
  """
  def list_contacts(base_url, req_options \\ []) do
    request =
      Req.new(
        [
          url: base_url <> "/contacts",
          params: [limit: 100],
          decode_json: [keys: :atoms],
          retry: false
        ] ++ req_options
      )

    case Req.get(request) do
      {:ok, %Req.Response{status: 200, body: %{contacts: contacts}}} -> {:ok, contacts}
      {:ok, %Req.Response{status: status}} -> {:error, {:unexpected_status, status}}
      {:error, exception} -> {:error, exception}
    end
  end

  @doc """
  Downloads the export archive (a zip) and returns its entries as
  `[{filename, contents}]`.
  """
  def fetch_export(base_url, req_options \\ []) do
    request = Req.new([url: base_url <> "/export.zip", retry: false] ++ req_options)

    case Req.get(request) do
      {:ok, %Req.Response{status: 200, body: entries}} when is_list(entries) ->
        {:ok, Enum.map(entries, fn {name, contents} -> {to_string(name), contents} end)}

      {:ok, %Req.Response{status: 200}} ->
        {:error, :not_an_archive}

      {:ok, %Req.Response{status: status}} ->
        {:error, {:unexpected_status, status}}

      {:error, exception} ->
        {:error, exception}
    end
  end
end
