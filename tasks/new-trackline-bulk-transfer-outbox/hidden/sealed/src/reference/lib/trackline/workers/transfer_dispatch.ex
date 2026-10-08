defmodule Trackline.Workers.TransferDispatch do
 use Oban.Worker, queue: :default
 def perform(%Oban.Job{args: %{"batch_id" => id}}), do: Trackline.Support.Transfer.dispatch(id)
end
