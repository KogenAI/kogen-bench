defmodule Beltway.Report do
  @moduledoc """
  Renders a tabular report as text, CSV or JSON.

      report = %{title: "Errors", columns: ["service", "count"], rows: [["api", 3], ["web", nil]]}
      Beltway.Report.render(report, :text)
  """

  @type t :: %{title: binary(), columns: [binary()], rows: [[term()]]}

  @spec render(t(), :text | :csv | :json) :: binary()
  def render(%{title: title, columns: columns, rows: rows}, :text) do
    cells =
      Enum.map(rows, fn row ->
        Enum.map(row, fn
          nil -> "-"
          v when is_float(v) -> :erlang.float_to_binary(v, decimals: 2)
          v -> to_string(v)
        end)
      end)

    widths =
      columns
      |> Enum.with_index()
      |> Enum.map(fn {col, i} ->
        Enum.max([
          String.length(col) | Enum.map(cells, fn row -> String.length(Enum.at(row, i, "")) end)
        ])
      end)

    header =
      columns
      |> Enum.zip(widths)
      |> Enum.map_join("  ", fn {col, w} -> String.pad_trailing(col, w) end)
      |> String.trim_trailing()

    rule = widths |> Enum.map_join("  ", &String.duplicate("-", &1))

    body =
      Enum.zip_with(cells, rows, fn cell_row, raw_row ->
        cell_row
        |> Enum.zip(widths)
        |> Enum.zip(raw_row)
        |> Enum.map_join("  ", fn
          {{cell, w}, raw} when is_integer(raw) -> String.pad_leading(cell, w)
          {{cell, w}, _raw} -> String.pad_trailing(cell, w)
        end)
        |> String.trim_trailing()
      end)

    Enum.join(
      [title, String.duplicate("=", String.length(title)), "", header, rule] ++ body,
      "\n"
    ) <> "\n"
  end

  def render(%{columns: columns, rows: rows}, :csv) do
    quote_field = fn field ->
      if String.contains?(field, [",", "\"", "\n", "\r"]) do
        "\"" <> String.replace(field, "\"", "\"\"") <> "\""
      else
        field
      end
    end

    cell = fn
      nil -> ""
      v -> to_string(v)
    end

    lines =
      [columns | Enum.map(rows, fn row -> Enum.map(row, cell) end)]
      |> Enum.map(fn fields -> fields |> Enum.map(quote_field) |> Enum.join(",") end)

    Enum.join(lines, "\r\n") <> "\r\n"
  end

  def render(%{title: title, columns: columns, rows: rows}, :json) do
    objects = Enum.map(rows, fn row -> columns |> Enum.zip(row) |> Map.new() end)
    JSON.encode!(%{"title" => title, "rows" => objects})
  end

  def render(_report, format) do
    raise ArgumentError, "unknown format: #{inspect(format)}"
  end
end
