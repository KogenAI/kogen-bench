defmodule Trackline.Inbound do
  @moduledoc "Turns inbound emails (already authenticated) into tickets and comments."

  alias Trackline.Repo
  alias Trackline.Support.{Comment, InboundMessage, Organization, Ticket}

  @max_title 200
  @max_comment 5_000

  def ingest(%Organization{id: org_id}, %{"message_id" => mid, "from" => from} = payload)
      when is_binary(mid) and mid != "" and is_binary(from) and from != "" do
    Repo.transact(fn ->
      case find(org_id, mid) do
        %InboundMessage{ticket_id: ticket_id} -> {:ok, {:duplicate, ticket_id}}
        nil -> create(org_id, mid, from, payload)
      end
    end)
  end

  def ingest(_org, _payload), do: {:error, :invalid}

  defp find(org_id, message_id),
    do: Repo.get_by(InboundMessage, organization_id: org_id, message_id: message_id)

  defp create(org_id, mid, from, payload) do
    text = if is_binary(payload["text"]), do: payload["text"], else: ""
    parent = if is_binary(payload["in_reply_to"]), do: find(org_id, payload["in_reply_to"])

    with {:ok, ticket_id} <- create_ticket_or_comment(org_id, parent, from, payload, text),
         {:ok, _} <-
           Repo.insert(%InboundMessage{
             organization_id: org_id,
             ticket_id: ticket_id,
             message_id: mid
           }) do
      {:ok, {:created, ticket_id}}
    end
  end

  defp create_ticket_or_comment(_org_id, %InboundMessage{ticket_id: ticket_id}, _from, _p, text) do
    body = String.slice(text, 0, @max_comment)
    body = if String.trim(body) == "", do: "(empty message)", else: body

    with {:ok, _} <- %Comment{ticket_id: ticket_id} |> Comment.changeset(%{body: body}) |> Repo.insert() do
      {:ok, ticket_id}
    end
  end

  defp create_ticket_or_comment(org_id, nil, from, payload, text) do
    subject = if is_binary(payload["subject"]), do: String.trim(payload["subject"]), else: ""
    title = if subject == "", do: "(no subject)", else: String.slice(subject, 0, @max_title)

    with {:ok, ticket} <-
           %Ticket{organization_id: org_id, requester_email: from}
           |> Ticket.changeset(%{title: title, body: text})
           |> Repo.insert() do
      {:ok, ticket.id}
    end
  end
end
