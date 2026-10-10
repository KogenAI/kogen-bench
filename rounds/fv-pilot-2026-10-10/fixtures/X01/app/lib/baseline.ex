defmodule Baseline do
  @moduledoc "A single cached baseline and computation accounting."

  def init do
    %{tree: :t1, context: :c1, cached_tree: :none,
      cached_context: :none, computations: 0, reused: false}
  end

  def step(state, event) do
    if event == :request do
      request(state)
    else
      select_tree(state, event)
    end
  end

  def select_tree(state, event) do
    if event == :tree_t1 do
      %{state | tree: :t1, reused: false}
    else
      if event == :tree_t2 do
        %{state | tree: :t2, reused: false}
      else
        select_context(state, event)
      end
    end
  end

  def select_context(state, event) do
    if event == :context_c1 do
      %{state | context: :c1, reused: false}
    else
      if event == :context_c2 do
        %{state | context: :c2, reused: false}
      else
        state
      end
    end
  end

  def request(state) do
    key = cache_key(state.tree, state.context)
    if cache_matches(state, key) do
      %{state | reused: true}
    else
      compute(state, key)
    end
  end

  def cache_key(_tree, context) do
    %{tree: :any, context: context}
  end

  def cache_matches(state, key) do
    state.cached_tree == key.tree and state.cached_context == key.context
  end

  def compute(state, key) do
    %{state | cached_tree: key.tree, cached_context: key.context,
      computations: state.computations + 1, reused: false}
  end
end
