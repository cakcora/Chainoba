# Graph
To get any graph, import 
<b>getGraph(dd, mm, yy, dOffset,graphType,dirPath)</b> function from getAPIData 
<br>
<h3>Inputs: </h3>
<b>graphType</b> may take one of the three values :<br>
<ul>
<li>COMPOSITE
<li>ADDRESS
<li>TRANSACTION
</ul>
Suppose you want a COMPOSITE graph for 10 days from date February 9, 2009 at a location "../XYZ" then :<br>
dd = 9  <br>
mm = 2 <br>
yy = 2009  <br>
dOffset = 10 <br>
graphType = COMPOSITE
dirPath = "../XYZ"

<h3>Output:</h3>
<ul>
<li>
In case of <b>COMPOSITE </b> graph you will get an edge list file at the given directory path("../XYZ")
<br>
<li>
In case of <b>ADDRESS</b> graph you will get an edge list file and a vertex list file at the given directory path("../XYZ")
<br>
<li>
In case of <b>TRANSACTION</b> graph you will get an edge list file and a vertex list file at the given directory path("../XYZ")
</ul>