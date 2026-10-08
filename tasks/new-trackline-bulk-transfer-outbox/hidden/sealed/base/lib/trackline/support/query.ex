defmodule Trackline.Support.Query do
  @moduledoc """
  Parses the ticket search box syntax into a structured query.

      status:open,pending priority:high assignee:me "login bug" -spam

  Rules:

    * `status:` and `priority:` take comma separated values. Values are
      case-insensitive, unknown values are dropped, duplicates are removed and
      several tokens for the same key are merged, keeping first-seen order.
    * `assignee:` takes `me`, `none` or an email address (lower-cased). When
      given more than once the last one wins.
    * A `key:` token with nothing after the colon is ignored.
    * Unknown keys (`color:red`) are ordinary search terms.
    * Double quotes group words into one term: `"login bug"`. An unterminated
      quote runs to the end of the input.
    * A term starting with `-` is an exclusion (`-spam`); a lone `-` is a term.
    * Terms are lower-cased.
  """

  @statuses ~w(open pending closed)
  @priorities ~w(low normal high urgent)

  @type t :: %{
          status: [String.t()],
          priority: [String.t()],
          assignee: nil | :me | :none | String.t(),
          terms: [String.t()],
          exclude: [String.t()]
        }

  @spec parse(String.t() | nil) :: t()
  def parse(nil), do: parse("")

  def parse(input) when is_binary(input) do
    empty = %{status: [], priority: [], assignee: nil, terms: [], exclude: []}

    input
    |> tokenize()
    |> Enum.reduce(empty, &apply_token/2)
    |> then(fn q ->
      %{
        q
        | status: Enum.uniq(q.status),
          priority: Enum.uniq(q.priority),
          terms: Enum.reverse(q.terms),
          exclude: Enum.reverse(q.exclude)
      }
    end)
  end

  defp apply_token({:quoted, text}, q), do: add_term(q, text)

  defp apply_token({:word, word}, q) do
    case String.split(word, ":", parts: 2) do
      [key, value] -> apply_key(String.downcase(key), value, word, q)
      [_] -> add_term(q, word)
    end
  end

  defp apply_key("status", value, _word, q),
    do: %{q | status: q.status ++ values(value, @statuses)}

  defp apply_key("priority", value, _word, q),
    do: %{q | priority: q.priority ++ values(value, @priorities)}

  defp apply_key("assignee", value, _word, q) do
    case String.downcase(value) do
      "" -> q
      "me" -> %{q | assignee: :me}
      "none" -> %{q | assignee: :none}
      email -> %{q | assignee: email}
    end
  end

  defp apply_key(_other, _value, word, q), do: add_term(q, word)

  defp values(value, allowed) do
    value
    |> String.split(",", trim: true)
    |> Enum.map(&String.downcase(String.trim(&1)))
    |> Enum.filter(&(&1 in allowed))
  end

  defp add_term(q, text) do
    term = text |> String.trim() |> String.downcase()

    cond do
      term == "" ->
        q

      term != "-" and String.starts_with?(term, "-") ->
        %{q | exclude: [String.slice(term, 1..-1//1) | q.exclude]}

      true ->
        %{q | terms: [term | q.terms]}
    end
  end

  defp tokenize(input), do: tokenize(String.trim_leading(input), [])

  defp tokenize("", acc), do: Enum.reverse(acc)

  defp tokenize("\"" <> rest, acc) do
    case String.split(rest, "\"", parts: 2) do
      [text, remainder] -> tokenize(String.trim_leading(remainder), [{:quoted, text} | acc])
      [text] -> tokenize("", [{:quoted, text} | acc])
    end
  end

  defp tokenize(input, acc) do
    case Regex.run(~r/^(\S+)\s*(.*)$/s, input) do
      [_, word, rest] -> tokenize(rest, [{:word, word} | acc])
    end
  end
end
