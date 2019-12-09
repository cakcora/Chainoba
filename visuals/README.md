# Visuals
Install Requirements

```
pip install -r visuals/requirements.txt
```
* Use class  <b>show_composite_graph</b> to visualize composite graph: <br>
    * create an object of this class<br>
    * call <b>add_composite_nodes(input,amount_in, output,amount_out,time)</b>
    to add new transactions to composite graphs. this function can get one transaction at a time.<br>
    input: pass a list of addresses who are sending bitcoin.<br> output: pass a list of addresses who receive bitcoin. <br>
    amount_in: pass how many bitcoins each corresponding address is sending. <br> amount_out: pass
    how much bitcoin each address has taken. <br> time: add values from 1,2,... inputs will appear 
    from left to right based on their time values. 
    * call <b> show_graph </b> to see the graph on your browser. 

* Use class  <b>show_cluster</b> to visualize addresses belonging to the same cluster in a address graph: <br>
    * create an object of this class <br>
    * call <b>add_address_graph( input, output, amount)</b>
    to add new transactions to composite graphs. this function can get one transaction at a time.<br>
    input: pass a list of addresses who are sending bitcoin.<br> output: pass a list of addresses who receive bitcoin. <br>
    amount: pass how many bitcoins each input is sending to its corresponding output. <br>
    * call <b> show_graph </b> to see the graph on your browser. 
    * call <b>cluster_addresses</b> and pass two lists: addresses and cluster corresponding to each address
    
* Use class  <b>show_address_graph</b> to visualize addresses belonging to the same cluster in a address graph: <br>
    * create an object of this class <br>
    * call <b>add_address_graph( input, output, amount)</b>
    to add new transactions to composite graphs. this function can get one transaction at a time.<br>
    input: pass a list of addresses who are sending bitcoin.<br> output: pass a list of addresses who receive bitcoin. <br>
    amount: pass how many bitcoins each input is sending to its corresponding output. <br>
    * call <b> show_graph </b> to see the graph on your browser. 

* Use class  <b>show_path</b> to visualize a single path <br>
    * create an object of this class <br>
    * call <b>add_path( input, amount)</b>: input is a list which form a path. amount is the amount transferred from nodes
    in a consecutive order. 
    * call <b> show_graph </b> to see the graph on your browser. 
    
* Use class  <b>show_transaction_graph</b> to visualize a single path <br>
    * create an object of this class <br>
    * call <b>add_transaction(input, output, in_time, out_time, amount)</b>: this function adds transactions to the 
    graph. input are the set of transactions that have a directed edge to the output transactions. in_time is the 
    time where each transaction has appeared out_time is the time where an output transaction has appeared and amount 
    corresponds to the number of bitcoin transfered between two transactions.  
    * call <b> show_graph </b> to see the graph on your browser. 
    
<br> All parameters of functions should be in form of a list</br>
<br> All classes have a local main function and the output of each main function is stored in 
visuals\show_graph\output</br>. Refer to them in case the explanation in here is not sufficient.
  
 * Use <b>exampleDriver</b> to visualize scatter graph and box plot <br>
    * call <b>generate_scattered_graph(node_array, xaxis_name, yaxis_name)</b>: this function takes the coordinates of x and y,        
    xaxis name and y axis name as function parameters.   
    * it displays a scatter plot as output. 
    * call <b>generate_box_plot(node_array, xaxis_name, yaxis_name)</b>:this function takes the minimum value , maximum value 
    and median value of a box in the array along with the xaxis and yaxis names. 
    * it displays a box plot as output. 
