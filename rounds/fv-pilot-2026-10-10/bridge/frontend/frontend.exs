defmodule FV.Frontend do
  def json(v) when is_map(v) do
    "{" <> Enum.map_join(Enum.sort(Map.to_list(v)), ",", fn {k, x} -> json(to_string(k)) <> ":" <> json(x) end) <> "}"
  end
  def json(v) when is_list(v), do: "[" <> Enum.map_join(v, ",", &json/1) <> "]"
  def json(v) when is_binary(v) do
    escaped = v |> String.replace("\\", "\\\\") |> String.replace("\"", "\\\"") |> String.replace("\n", "\\n") |> String.replace("\r", "\\r") |> String.replace("\t", "\\t")
    "\"" <> escaped <> "\""
  end
  def json(nil), do: "null"
  def json(true), do: "true"
  def json(false), do: "false"
  def json(v) when is_integer(v), do: Integer.to_string(v)

  def fail(loc, reason), do: raise(ArgumentError, "FV-FRONTEND #{loc.file}:#{loc.line}:#{loc.column}: #{reason}")
  def loc(meta, parent), do: %{file: parent.file, line: Keyword.get(meta, :line, parent.line), column: Keyword.get(meta, :column, parent.column)}
  def node(kind, data, l), do: Map.merge(%{kind: kind, loc: l}, data)
  def modname({:__aliases__, _, names}), do: Enum.map_join(names, ".", &Atom.to_string/1)
  def modname(other), do: raise(ArgumentError, "invalid module #{inspect(other)}")

  def parse(source, file) do
    parent = %{file: file, line: 1, column: 1}
    encoder = fn value, meta ->
      if is_integer(value) or (is_atom(value) and Keyword.get(meta, :format) != :keyword and value not in [:do, :else]) do
        {:ok, {:__fv_literal__, meta, [value]}}
      else
        {:ok, value}
      end
    end
    case Code.string_to_quoted(source, columns: true, token_metadata: true, literal_encoder: encoder) do
      {:ok, ast} -> top(ast, parent)
      {:error, {meta, message, token}} -> fail(loc(meta, parent), "syntax error: #{message} #{token}")
    end
  end
  def top({:__block__, _, xs}, l), do: Enum.flat_map(xs, &top(&1, l))
  def top({:defmodule, meta, [name, [do: body]]}, l) do
    l = loc(meta, l)
    declarations = case body do {:__block__, _, xs} -> xs; x -> [x] end
    declarations = Enum.reject(declarations, &documentation?/1)
    structs = Enum.filter(declarations, &match?({:defstruct, _, _}, &1))
    if length(structs) > 1, do: fail(l, "multiple defstruct declarations")
    struct_fields = case structs do
      [] -> nil
      [{:defstruct, meta, [fs]}] when is_list(fs) ->
        sl = loc(meta, l)
        fs = Enum.map(fs, fn
          {key, value} when is_atom(key) -> {key, value}
          {:__fv_literal__, _, [key]} when is_atom(key) -> {key, nil}
          key when is_atom(key) -> {key, nil}
          _ -> fail(sl, "unsupported defstruct fields")
        end)
        fields(fs, sl, &expr/2) |> Enum.map(fn f ->
          unless f.value.kind in ["atom", "bool", "int"], do: fail(f.loc, "struct defaults must be finite literals")
          f
        end)
      _ -> fail(l, "unsupported defstruct declaration")
    end
    functions = declarations |> Enum.reject(&match?({:defstruct, _, _}, &1)) |> Enum.map(&function(&1, l))
    [node("module", %{name: modname(name), functions: functions, struct_fields: struct_fields}, l)]
  end
  def top(_, l), do: fail(l, "only defmodule declarations are allowed")
  def documentation?({:@, _, [{name, _, [value]}]}) when name in [:doc, :moduledoc] and (is_binary(value) or is_boolean(value)), do: true
  def documentation?({:@, _, [{name, _, [{:__fv_literal__, _, [value]}]}]}) when name in [:doc, :moduledoc] and is_boolean(value), do: true
  def documentation?(_), do: false

  def function({visibility, meta, [{name, headmeta, params}, [do: body]]}, l) when visibility in [:def, :defp] and is_atom(name) and (is_list(params) or is_nil(params)) do
    l = loc(meta, l)
    node("function", %{name: Atom.to_string(name), visibility: if(visibility == :def, do: "public", else: "private"), params: Enum.map(params || [], &pattern(&1, loc(headmeta, l))), body: expr(body, l)}, l)
  end
  def function({_, meta, _}, l), do: fail(loc(meta, l), "unsupported declaration or function guard")
  def function(_, l), do: fail(l, "unsupported module declaration")

  def pattern({:__fv_literal__, meta, [value]}, l), do: literal(value, loc(meta, l))
  def pattern({name, meta, context}, l) when is_atom(name) and (is_atom(context) or is_nil(context)) do
    l = loc(meta, l)
    if name == :_, do: node("wildcard", %{}, l), else: node("var", %{name: Atom.to_string(name)}, l)
  end
  def pattern({:%{}, meta, fields}, l) do
    l = loc(meta, l)
    node("record_pattern", %{fields: fields(fields, l, &pattern/2)}, l)
  end
  def pattern({:{}, meta, items}, l), do: node("tuple_pattern", %{items: Enum.map(items, &pattern(&1, loc(meta, l)))}, loc(meta, l))
  def pattern({a, b}, l), do: node("tuple_pattern", %{items: [pattern(a, l), pattern(b, l)]}, l)
  def pattern(v, l) when is_atom(v) or is_integer(v), do: literal(v, l)
  def pattern({_, meta, _}, l), do: fail(loc(meta, l), "unsupported pattern")
  def pattern(_, l), do: fail(l, "unsupported pattern")

  def literal(true, l), do: node("bool", %{value: true}, l)
  def literal(false, l), do: node("bool", %{value: false}, l)
  def literal(v, l) when is_atom(v), do: node("atom", %{value: Atom.to_string(v)}, l)
  def literal(v, l) when is_integer(v), do: node("int", %{value: v}, l)

  def fields(fs, l, translator) do
    Enum.map(fs, fn
      {key, value} when is_atom(key) ->
        if key == :__struct__, do: fail(l, "struct tag introspection is outside the subset")
        translated = translator.(value, l)
        node("field", %{name: Atom.to_string(key), value: translated}, translated.loc)
      _ -> fail(l, "record fields must have literal atom keys")
    end)
  end
  def expr({:__fv_literal__, meta, [value]}, l), do: literal(value, loc(meta, l))
  def expr({:__block__, meta, xs}, l), do: block(xs, loc(meta, l))
  def expr({:if, meta, [cond, kw]}, l) do
    l = loc(meta, l)
    unless Keyword.keys(kw) -- [:do, :else] == [], do: fail(l, "unsupported if options")
    node("if", %{condition: expr(cond, l), then: expr(Keyword.fetch!(kw, :do), l), else: expr(Keyword.get(kw, :else, nil), l)}, l)
  end
  def expr({:case, meta, [value, [do: branches]]}, l) do
    l = loc(meta, l)
    branches = Enum.map(branches, fn
      {:->, m, [[pat], body]} -> bl = loc(m, l); node("branch", %{pattern: pattern(pat, bl), body: expr(body, bl)}, bl)
      _ -> fail(l, "unsupported case branch or guard")
    end)
    node("case", %{value: expr(value, l), branches: branches}, l)
  end
  def expr({:%{}, meta, [{:|, _, [base, fs]}]}, l) do
    l = loc(meta, l)
    node("update", %{base: expr(base, l), struct: nil, fields: fields(fs, l, &expr/2)}, l)
  end
  def expr({:%{}, meta, fs}, l) do
    l = loc(meta, l)
    node("record", %{struct: nil, fields: fields(fs, l, &expr/2)}, l)
  end
  def expr({:%, meta, [name, {:%{}, _, [{:|, _, [base, fs]}]}]}, l) do
    l = loc(meta, l)
    node("update", %{base: expr(base, l), struct: modname(name), fields: fields(fs, l, &expr/2)}, l)
  end
  def expr({:%, meta, [name, {:%{}, _, fs}]}, l) do
    l = loc(meta, l)
    node("record", %{struct: modname(name), fields: fields(fs, l, &expr/2)}, l)
  end
  def expr({{:., _, [{:__aliases__, _, _} = mod, name]}, meta, args}, l) when is_list(args) do
    l = loc(meta, l)
    module = modname(mod)
    if module == "Map" and not ((name == :get and length(args) == 3) or (name == :has_key? and length(args) == 2)), do: fail(l, "unsupported Map helper (only Map.get/3 and Map.has_key?/2)")
    node("call", %{module: module, name: Atom.to_string(name), args: Enum.map(args, &expr(&1, l))}, l)
  end
  def expr({{:., _, [base, field]}, meta, []}, l) when is_atom(field) do
    l = loc(meta, l)
    unless Keyword.get(meta, :no_parens, false), do: fail(l, "dynamic zero-arity dispatch is outside the subset")
    if field == :__struct__, do: fail(l, "struct tag introspection is outside the subset")
    node("get", %{base: expr(base, l), field: Atom.to_string(field)}, l)
  end
  def expr({op, meta, [a, b]}, l) when op in [:and, :or, :==, :!=, :===, :!==, :+, :-] do
    l = loc(meta, l)
    op = case op do :=== -> :==; :!== -> :!=; x -> x end
    node("binary", %{op: Atom.to_string(op), left: expr(a, l), right: expr(b, l)}, l)
  end
  def expr({:not, meta, [v]}, l), do: node("unary", %{op: "not", value: expr(v, loc(meta, l))}, loc(meta, l))
  def expr({:-, meta, [v]}, l) when is_integer(v), do: literal(-v, loc(meta, l))
  def expr({:-, meta, [{:__fv_literal__, _, [v]}]}, l) when is_integer(v), do: literal(-v, loc(meta, l))
  def expr({:{}, meta, items}, l), do: node("tuple", %{items: Enum.map(items, &expr(&1, loc(meta, l)))}, loc(meta, l))
  def expr({a, b}, l), do: node("tuple", %{items: [expr(a, l), expr(b, l)]}, l)
  def expr({name, meta, context}, l) when is_atom(name) and (is_atom(context) or is_nil(context)), do: node("var", %{name: Atom.to_string(name)}, loc(meta, l))
  def expr({name, meta, args}, l) when is_atom(name) and is_list(args) do
    l = loc(meta, l)
    if name in [:&&, :||, :|>, :=, :fn, :for, :receive, :quote, :unquote, :cond, :with, :try, :raise, :throw, :send, :spawn, :apply, :in, :*, :/, :<, :>, :<=, :>=, :++, :--], do: fail(l, "unsupported construct #{name}")
    node("call", %{module: nil, name: Atom.to_string(name), args: Enum.map(args, &expr(&1, l))}, l)
  end
  def expr(v, l) when is_atom(v) or is_integer(v), do: literal(v, l)
  def expr(_, l), do: fail(l, "unsupported expression (strings, floats, lists, dynamic calls and effects are outside the subset)")

  def block([x], l), do: expr(x, l)
  def block([{:=, meta, [pat, value]} | rest], l) when rest != [] do
    l = loc(meta, l)
    node("let", %{pattern: pattern(pat, l), value: expr(value, l), body: block(rest, l)}, l)
  end
  def block(_, l), do: fail(l, "only lexical assignments may precede a block result")

  def app(dir) do
    paths = Path.wildcard(Path.join([dir, "lib", "**", "*.ex"])) |> Enum.sort()
    if paths == [], do: fail(%{file: "lib/", line: 1, column: 1}, "no Elixir source found")
    modules = Enum.flat_map(paths, fn p -> parse(File.read!(p), Path.relative_to(p, dir)) end)
    modules = expand_structs(modules)
    validate(modules)
    %{version: 1, modules: modules}
  end
  def expand_structs(modules) do
    structs = for m <- modules, not is_nil(m.struct_fields), into: %{}, do: {m.name, m.struct_fields}
    walk = fn walk, value ->
      cond do
        is_list(value) -> Enum.map(value, &walk.(walk, &1))
        is_map(value) ->
          value = Map.new(value, fn {k, v} -> {k, walk.(walk, v)} end)
          if Map.get(value, :kind) in ["record", "update"] and not is_nil(value.struct) do
            defaults = Map.get(structs, value.struct) || fail(value.loc, "undefined struct #{value.struct}")
            names = Enum.map(defaults, & &1.name)
            if Enum.any?(value.fields, &(&1.name not in names)), do: fail(value.loc, "unknown struct field")
            if value.kind == "record" do
              overrides = Map.new(value.fields, &{&1.name, &1})
              %{value | fields: Enum.map(defaults, &Map.get(overrides, &1.name, &1))}
            else
              value
            end
          else
            value
          end
        true -> value
      end
    end
    walk.(walk, modules)
  end
  def validate(modules) do
    Enum.reduce(modules, [], fn m, names ->
      if m.name in names, do: fail(m.loc, "module redefinition is outside the subset")
      if m.name == "Map", do: fail(m.loc, "cannot redefine the standard Map helper module")
      [m.name | names]
    end)
    functions = (for m <- modules, f <- m.functions, do: {{m.name, f.name, length(f.params)}, f}) |> Enum.group_by(&elem(&1, 0), &elem(&1, 1))
    graph = for {{module, _, _} = key, clauses} <- functions, into: %{} do
      deps = Enum.flat_map(clauses, &calls(&1.body)) |> Enum.flat_map(fn n ->
        if n.module == "Map" do
          []
        else
          target = {n.module || module, n.name, length(n.args)}
          unless Map.has_key?(functions, target), do: fail(n.loc, "unknown or effectful helper #{inspect(target)}")
          [target]
        end
      end)
      {key, deps}
    end
    visit = fn visit, key, path ->
      if key in path, do: fail(hd(functions[key]).loc, "recursive helpers are outside the subset")
      Enum.each(graph[key], &visit.(visit, &1, [key | path]))
    end
    Enum.each(Map.keys(graph), &visit.(visit, &1, []))
    :ok
  end
  def calls(v) when is_map(v) do
    own = if Map.get(v, :kind) == "call", do: [v], else: []
    own ++ Enum.flat_map(Map.values(v), &calls/1)
  end
  def calls(v) when is_list(v), do: Enum.flat_map(v, &calls/1)
  def calls(_), do: []
end
