defmodule Trackline.Support.TicketImport do
  @moduledoc """
  Imports tickets from a CSV export of another tool. Partial success: valid rows
  are created, bad rows are reported by row number (header = row 1). Tickets whose
  `external_id` already exists in the organization are skipped.
  """

  import Ecto.Query, warn: false

  alias Trackline.Accounts.User
  alias Trackline.Repo
  alias Trackline.Support.{Membership, Organization, Ticket}

  def run(%Organization{} = org, %User{} = user, csv) when is_binary(csv) do
    with {:ok, [header | records]} <- parse(csv),
         {:ok, cols} <- columns(header) do
      members =
        Repo.all(
          from u in User,
            join: m in Membership,
            on: m.user_id == u.id,
            where: m.organization_id == ^org.id,
            select: {u.email, u.id}
        )
        |> Map.new(fn {email, id} -> {String.downcase(email), id} end)

      existing =
        from(t in Ticket,
          where: t.organization_id == ^org.id and not is_nil(t.external_id),
          select: t.external_id
        )
        |> Repo.all()
        |> MapSet.new()

      acc = %{created: 0, skipped_existing: 0, errors: [], seen: existing}

      Repo.transact(fn ->
        report =
          records
          |> Enum.with_index(2)
          |> Enum.reduce(acc, fn {record, row}, acc -> import_row(acc, row, record, cols, org, user, members) end)

        {:ok, %{created: report.created, skipped_existing: report.skipped_existing, errors: Enum.reverse(report.errors)}}
      end)
    end
  end

  defp import_row(acc, _row, [""], _cols, _org, _user, _members), do: acc

  defp import_row(acc, row, record, cols, org, user, members) do
    field = fn name -> record |> Enum.at(cols[name], "") |> String.trim() end
    get = fn name -> if cols[name], do: field.(name), else: "" end
    external_id = get.("external_id")

    cond do
      external_id == "" ->
        error(acc, row, "external_id is missing")

      MapSet.member?(acc.seen, external_id) ->
        %{acc | skipped_existing: acc.skipped_existing + 1}

      true ->
        attrs = %{title: get.("title"), body: get.("body"), priority: blank_to(get.("priority"), "normal")}
        status = get.("status") |> blank_to("open") |> String.downcase()
        assignee = get.("assignee")

        with :ok <- check_status(status),
             {:ok, assignee_id} <- find_assignee(assignee, members),
             attrs = Map.update!(attrs, :priority, &String.downcase/1),
             {:ok, _} <- insert(org, user, external_id, status, assignee_id, attrs) do
          %{acc | created: acc.created + 1, seen: MapSet.put(acc.seen, external_id)}
        else
          {:error, message} -> error(acc, row, message)
        end
    end
  end

  defp error(acc, row, message), do: %{acc | errors: [%{row: row, message: message} | acc.errors]}

  defp blank_to("", default), do: default
  defp blank_to(value, _default), do: value

  defp check_status(status) do
    if status in Ticket.statuses(), do: :ok, else: {:error, "status must be one of #{Enum.join(Ticket.statuses(), ", ")}"}
  end

  defp find_assignee("", _members), do: {:ok, nil}

  defp find_assignee(email, members) do
    case Map.fetch(members, String.downcase(email)) do
      {:ok, id} -> {:ok, id}
      :error -> {:error, "assignee #{email} is not a member of this organization"}
    end
  end

  defp insert(org, user, external_id, status, assignee_id, attrs) do
    %Ticket{
      organization_id: org.id,
      author_id: user.id,
      external_id: external_id,
      assignee_id: assignee_id,
      status: status
    }
    |> Ticket.changeset(attrs)
    |> Repo.insert()
    |> case do
      {:ok, ticket} -> {:ok, ticket}
      {:error, changeset} -> {:error, changeset_message(changeset)}
    end
  end

  defp changeset_message(changeset) do
    [{field, {msg, _}} | _] = changeset.errors
    "#{field} #{msg}"
  end

  defp columns(header) do
    cols =
      header
      |> Enum.with_index()
      |> Map.new(fn {name, i} -> {name |> String.trim() |> String.downcase(), i} end)

    if cols["external_id"] && cols["title"], do: {:ok, cols}, else: {:error, :missing_columns}
  end

  ## RFC 4180 reader (quoted fields may contain commas, quotes and line breaks)

  def parse(csv) do
    csv = String.replace_prefix(csv, "﻿", "")

    case do_parse(csv, "", [], [], false) do
      {:ok, []} -> {:error, :empty}
      other -> other
    end
  end

  defp do_parse("", _cell, _row, _rows, true), do: {:error, :unterminated_quote}
  defp do_parse("", "", [], rows, false), do: {:ok, Enum.reverse(rows)}
  defp do_parse("", cell, row, rows, false), do: {:ok, Enum.reverse([Enum.reverse([cell | row]) | rows])}
  defp do_parse(<<"\"\"", rest::binary>>, cell, row, rows, true), do: do_parse(rest, cell <> "\"", row, rows, true)
  defp do_parse(<<"\"", rest::binary>>, cell, row, rows, true), do: do_parse(rest, cell, row, rows, false)
  defp do_parse(<<c, rest::binary>>, cell, row, rows, true), do: do_parse(rest, <<cell::binary, c>>, row, rows, true)
  defp do_parse(<<"\"", rest::binary>>, "", row, rows, false), do: do_parse(rest, "", row, rows, true)
  defp do_parse(<<",", rest::binary>>, cell, row, rows, false), do: do_parse(rest, "", [cell | row], rows, false)

  defp do_parse(<<"\r\n", rest::binary>>, cell, row, rows, false),
    do: do_parse(rest, "", [], [Enum.reverse([cell | row]) | rows], false)

  defp do_parse(<<"\n", rest::binary>>, cell, row, rows, false),
    do: do_parse(rest, "", [], [Enum.reverse([cell | row]) | rows], false)

  defp do_parse(<<c, rest::binary>>, cell, row, rows, false), do: do_parse(rest, <<cell::binary, c>>, row, rows, false)

end
