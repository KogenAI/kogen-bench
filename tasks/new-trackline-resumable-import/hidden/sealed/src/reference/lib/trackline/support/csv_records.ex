defmodule Trackline.Support.CSVRecords do
 def stream(path) do
   File.stream!(path, 4096)
   |> Stream.flat_map(&:binary.bin_to_list/1)
   |> Stream.concat([:eof])
   |> Stream.transform({[], [], :start}, &step/2)
 end
 defp field(chars), do: chars |> Enum.reverse() |> :binary.list_to_bin()
 defp step(:eof, {[], [], :start}=s), do: {[], s}
 defp step(:eof, {_, _, :quoted}), do: raise(ArgumentError, "unterminated CSV quote")
 defp step(:eof, {fs, f, _}), do: {[Enum.reverse([field(f)|fs])], {[], [], :start}}
 defp step(34, {fs, f, :quoted}), do: {[], {fs, f, :closed}}
 defp step(c, {fs, f, :quoted}), do: {[], {fs, [c|f], :quoted}}
 defp step(34, {fs, f, :closed}), do: {[], {fs, [34|f], :quoted}}
 defp step(34, {fs, [], :start}), do: {[], {fs, [], :quoted}}
 defp step(44, {fs, f, _}), do: {[], {[field(f)|fs], [], :start}}
 defp step(10, {fs, f, _}), do: {[Enum.reverse([field(f)|fs])], {[], [], :start}}
 defp step(13, s), do: {[], s}
 defp step(_, {_, _, :closed}), do: raise(ArgumentError, "invalid CSV quote suffix")
 defp step(34, _), do: raise(ArgumentError, "invalid CSV quote")
 defp step(c, {fs, f, _}), do: {[], {fs, [c|f], :unquoted}}
end
