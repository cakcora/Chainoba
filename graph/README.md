# Bitcoin Graph
To get Bitcoin graph, import 
<b>getGraph(dd, mm, yy, dOffset,graphType)</b> function from getAPIData. 
<br>

![Image of Composite graph](images/composite.png)
* To get the <b>COMPOSITE</b> graph object: <br>
 Suppose you want a COMPOSITE graph for 10 days from date February 9, 2009 then :<br>
    * Inputs: <br> 
dd = 9  <br>
mm = 2 <br>
yy = 2009  <br>
dOffset = 10 <br>
graphType = COMPOSITE
    * Output:
Two values will be returned:<br>
        * "Success"/"Fail"<br>
        * The composite graph in the form of object of <b>MultiDiGraph</b>
    * Here, edges of the graph will be of 2 types:
        * "From:" Address, "To:" Transaction hash, Amount
        * "From:" Transaction hash, "To:" Address, Amount

One can differentiate Transaction hash by its length, which is 64.
   

![Image of Address graph](images/address.png)

* To get the <b>ADDRESS</b> graph object: <br>
 Suppose you want a ADDRESS graph for 10 days from date February 9, 2009 then :<br>
    * Inputs: <br> 
dd = 9  <br>
mm = 2 <br>
yy = 2009  <br>
dOffset = 10 <br>
graphType = ADDRESS
    * Output:
Two values will be returned:<br>
        * "Success"/"Fail"<br>
        * The address graph in the form of object of <b>MultiDiGraph</b>
    * Here, edges of the graph will be of only 1 type:
        * "From:" Address, "To:" Address, Amount
      

![Image of transaction graph](images/transaction.png)

* To get the <b>TRANSACTION</b> graph object: <br>
 Suppose you want a TRANSACTION graph for 10 days from date February 9, 2009 then :<br>
    * Inputs: <br> 
dd = 9  <br>
mm = 2 <br>
yy = 2009  <br>
dOffset = 10 <br>
graphType = TRANSACTION
    * Output:
Two values will be returned:<br>
        * "Success"/"Fail"<br>
        * The transaction graph in the form of object of <b>MultiDiGraph</b>
    * Here, edges of the graph will be of only 1 type:
        * "From:" Transaction, "To:" Transaction, Amount
        
        

# Analysis

To get any feature, import
<b>getFeatures(dd,mm,yy,"Feature")</b> function from addressFeatures.
<br>

* To get the <b>LEVEL_OF_ACTIVITY</b> for each address: <br>
 Suppose you want a LEVEL_OF_ACTIVITY for date February 9, 2009 then :<br>
    * Inputs: <br>
dd = 9  <br>
mm = 2 <br>
yy = 2009  <br>
Feature = LEVEL_OF_ACTIVITY<br>
*   Output:
Two values will be returned:<br>
    * "Success"/"Fail"<br>
    * The data will be provided in form of dataframe object where each row will corresponds to  ["Address","Value"]<br>
       

Note : Different features are :<br>
* The Feature :LEVEL_OF_ACTIVITY<br>
* The Feature : TOTAL_BTC_RECEIVED<br>
* The Feature : TOTAL_BTC_SENT<br>
* The Feature :CURRENT_BALANCE

##Note: The data retrieved will be on daily basis

# Ethereum Graph
To get Ethereum graph, call 
<b>getEthereumgraph(24, 4, 2018, 1, "zrx")</b> function from graph.getGraph.ethereumGraph.getAPIData import getEthereumgraph, 
where the function signature is getEthereumgraph(day,month,year,dOffset,tokename)
<br>


<h6>References</h6>
[1] Images from "Data Science on Blockchain", UM Learn, Cuneyt Gurcan Akcora
