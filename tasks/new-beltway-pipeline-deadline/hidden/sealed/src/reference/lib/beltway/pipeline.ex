defmodule Beltway.Pipeline do
 use GenServer
 def start(items,command,opts), do: GenServer.start(__MODULE__,{self(),items,command,opts})
 def await(handle), do: GenServer.call(handle,:await,:infinity)
 def cancel(handle), do: GenServer.call(handle,:cancel)
 def run(items,command,opts) do
   {:ok,h}=start(items,command,opts)
   await(h)
 end
 def init({owner,items,{cmd,args},opts}) do
   jobs=Keyword.fetch!(opts,:max_concurrency);pending=Keyword.fetch!(opts,:max_pending);limit=Keyword.fetch!(opts,:max_output)
   if jobs<1 or pending<1 or limit<0 or not is_list(items), do: raise(ArgumentError,"invalid pipeline limits")
   remaining=Keyword.fetch!(opts,:deadline)-System.monotonic_time(:millisecond)
   helper=Application.app_dir(:beltway,"priv/pipeline_runner.py")
   argv=Enum.map([jobs,pending,limit,remaining,length(args)+1],&to_string/1)++[cmd|args]++items
   port=Port.open({:spawn_executable,System.find_executable("python3")},[:binary,:exit_status,:use_stdio,args: [helper|argv]])
   {:ok,%{port: port,owner: Process.monitor(owner),buffer: "",results: %{},count: length(items),wait: nil,cancelled: false}}
 end
 def handle_call(:await,from,s) do
   if map_size(s.results)==s.count do
     {:stop,:normal,ordered(s),s}
   else
     {:noreply,%{s|wait: from}}
   end
 end
 def handle_call(:cancel,_,s) do
   if not s.cancelled, do: Port.command(s.port,"cancel\n")
   {:reply,:ok,%{s|cancelled: true}}
 end
 def handle_info({port,{:data,data}},%{port: port}=s) do
   parts=String.split(s.buffer<>data,"\n");buffer=List.last(parts)
   results=parts |> Enum.drop(-1) |> Enum.reduce(s.results,fn line,acc ->
     [index,status,out]=String.split(line,"\t")
     value=case String.split(status,":") do
       ["ok",code] -> {:ok,%{status: String.to_integer(code),output: Base.decode64!(out)}}
       [reason] -> {:error,String.to_existing_atom(reason),Base.decode64!(out)}
     end
     Map.put(acc,String.to_integer(index),value)
   end)
   {:noreply,%{s|buffer: buffer,results: results}}
 end
 def handle_info({port,{:exit_status,status}},%{port: port}=s) do
   if status==0 and map_size(s.results)==s.count do
     if s.wait do GenServer.reply(s.wait,ordered(s));{:stop,:normal,s} else {:noreply,s} end
   else
     if s.wait, do: GenServer.reply(s.wait,{:error,:runner_failed})
     {:stop,:normal,s}
   end
 end
 def handle_info({:DOWN,ref,:process,_,_},%{owner: ref}=s), do: {:stop,:normal,s}
 def terminate(_,s) do
   try do Port.close(s.port) rescue ArgumentError -> :ok end
 end
 defp ordered(%{count: 0}), do: []
 defp ordered(s), do: Enum.map(0..(s.count-1),&Map.fetch!(s.results,&1))
 # Public error atoms, used by the bounded helper protocol.
 def error_kinds, do: [:deadline,:cancelled,:output_limit]
end
