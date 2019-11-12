# Graph
To get any graph, import <br>
<b>getGraph(dd, mm, yy, dOffset,graphType,dirPath)</b> function from getAPIData 
<br>
####Inputs: <br>
graphType may take one of the three values :<br>
COMPOSITE<br>
ADDRESS<br>
TRANSACTION

Suppose you want a COMPOSITE graph for 10 days from date February 9, 2009 at a location "../XYZ" then :<br>
dd = 9  <br>
mm = 2 <br>
yy = 2009  <br>
dOffset = 10 <br>
graphType = COMPOSITE
dirPath = "../XYZ"
<br>
####Output: <br>
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