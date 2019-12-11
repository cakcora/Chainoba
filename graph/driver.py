from graph.getGraph.getAPIData import getGraph
from graph.getGraph.ethereumGraph.getAPIData import getEthereumgraph
from graph.getGraph.graphanalysisSrija import CurrentBalanceAnalysis
from graph.getGraph.mainAnalysis import getAnalysisResults
from graph.getGraph.addressFeatures import getFeatures

# to get Bitcoin graph object
res1, graphobj = getGraph(9, 1, 2009, 1, 'COMPOSITE')

# to get Ethereum graph object
res2 , ethergraphobj = getEthereumgraph(24, 4, 2018, 1, "zrx")

# to evaluate current balance metric and store it in cummulative manner
res3, currBal=CurrentBalanceAnalysis(2009, 1, 9)

# evaluate all graph metrics and store it in daily basis from start and to date
res4 = getAnalysisResults(2009, 2, 1, 2009, 2, 28)

# get address feature for the specified date
res5, feat = getFeatures(2,2,2009,'LEVEL_OF_ACTIVITY')

