defmodule Preservation do
  @moduledoc "Bookkeeping for preserving and retiring a work copy."

  def init do
    %{work: true, saved: false, pending: false}
  end

  def step(state, event) do
    if event == :preserve_ok do
      preserve(state)
    else
      dispatch(state, event)
    end
  end

  def dispatch(state, event) do
    if event == :preserve_fail do
      failed(state)
    else
      cleanup_event(state, event)
    end
  end

  def cleanup_event(state, event) do
    if event == :cleanup or event == :retry do
      cleanup(state)
    else
      state
    end
  end

  def preserve(state) do
    %{state | saved: state.saved or state.work, pending: state.work}
  end

  def failed(state) do
    %{state | pending: state.work}
  end

  def cleanup(state) do
    if cleanup_ready(state) do
      retire(state)
    else
      state
    end
  end

  def cleanup_ready(state) do
    state.pending
  end

  def retire(state) do
    %{state | work: false, pending: false}
  end
end
