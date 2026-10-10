defmodule Workflow do
  @moduledoc "Revision approval and build admission state."

  def init do
    %{revision: :r1, approved: :none, admitted: false}
  end

  def step(state, event) do
    if event == :approve do
      approve(state)
    else
      dispatch(state, event)
    end
  end

  def dispatch(state, event) do
    if event == :start do
      start(state)
    else
      edit_event(state, event)
    end
  end

  def edit_event(state, event) do
    if event == :edit_r1 do
      edit(state, :r1)
    else
      if event == :edit_r2 do
        edit(state, :r2)
      else
        state
      end
    end
  end

  def approve(state) do
    %{state | approved: state.revision}
  end

  def edit(state, revision) do
    %{state | revision: revision, admitted: false}
  end

  def start(state) do
    %{state | admitted: admission(state)}
  end

  def admission(state) do
    state.approved != :none
  end
end
