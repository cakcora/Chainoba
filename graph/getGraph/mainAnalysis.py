import pandas as pd
from datetime import date, datetime, timedelta
from graph.getGraph.getAPIData import getGraph
from graph.getGraph.graphanalysisSrija import AddressDistAnalysis, TransactionSizeAnalysis, \
    assortativityCoefficientAnalysis
from graph.getGraph.graphAnalysisSarada import diffChainletsAmount, diffChainletMatrix, TotalBTCreceived, \
    LevelOfActivity, StronglyConnectedComponents, WeaklyConnectedComponents, diffChainlets
from graph.getGraph.graphAnalysisSaumya import BTCirculation, clusteringCoefficientonGraph, PearsonCoefficient, MostActiveEntity
import networkx as nx


def getAnalysisResults(startyear, startmonth, startday, endyear, endmonth, endday):
    """Get all the graph analytics results on daily basis within the start and end date"""
    try:
        # dataFrame for address distribution
        dfAddDist = pd.DataFrame(
            columns=["Date", "Total Addresses", "Receive-only Address %", "Send/receive Address %"])
        # dataFrame for Total BTC received
        dfTotRec = pd.DataFrame(columns=["Date", "Number of addresses with Total BTC received [0,1)",
                                         "Number of addresses with Total BTC received [1,10)",
                                         "Number of addresses with Total BTC received [10,100)",
                                         "Number of addresses with Total BTC received [100,1000)",
                                         "Number of addresses with Total BTC received [1000,10000)",
                                         "Number of addresses with Total BTC received [10000,50000)",
                                         "Number of addresses with Total BTC received greater than equal to 50000"])
        # dataFrame for Level of activity
        dfLOActivity = pd.DataFrame(columns=["Date", "Number of addresses with Level of activity [1,2)",
                                             "Number of addresses with Level of activity [2,5)",
                                             "Number of addresses with Level of activity [5,10)",
                                             "Number of addresses with Level of activity [10,100)",
                                             "Number of addresses with Level of activity [100,1000)",
                                             "Number of addresses with Level of activity [1000,5000)",
                                             "Number of addresses with Level of activity greater than equal to 5000"])
        # dataFrame for Strongly connected components
        dfSCC = pd.DataFrame(columns=["Date", "Number of Strongly connected components"])
        # dataFrame for Weakly connected components
        dfWCC = pd.DataFrame(columns=["Date", "Number of Weakly connected components"])
        # dataFrame for Transaction size
        dfTranSize = pd.DataFrame(columns=["Date", "Number of transaction of size [0,1)",
                                           "Number of transaction of size  [1,10)",
                                           "Number of transaction of size  [10,100)",
                                           "Number of transaction of size  [100,5000)",
                                           "Number of transaction of size  [5000,20000)",
                                           "Number of transaction of size  [20000,50000)",
                                           "Number of transaction of size  greater than equal to 50000"])
        # dataframe for Assortativity coefficient
        dfAssortCo = pd.DataFrame(columns=["Date", "Assortativity coefficient"])
        # dataframe for Bitcoin Circulation
        dfBTCCir = pd.DataFrame(
            columns=["Date", "Total Bitcoin", "Circulating Bitcoins %", "Not Circulating Bitcoins %"])

        # dataframe for Clustering coefficient
        dfClustering = pd.DataFrame(columns=["Date", "Clustering coefficient"])

        # dataframe for Pearson coefficient
        dfPearson = pd.DataFrame(columns=["Date", "Pearson coefficient"])

        # dataframe for Active Entity
        dfMostActive = pd.DataFrame(columns=["Date", "Node", "Total Number of Transaction"])
        # dataframe for Occurrence of different Chainlets
        dfChainletsOcc = pd.DataFrame(columns=["Date", "Occurrence of Split Chainlets", "Occurrence of Merge Chainlets",
                                               "Occurrence of Transition Chainlets"])
        # dataframe for Amount of different Chainlets
        dfChainletsAocc = pd.DataFrame(columns=["Date", "Amount of split Chainlets",
                                                "Amount of merge Chainlets",
                                                "Amount of transition Chainlets"])

        d0 = date(startyear, startmonth, startday)
        d1 = date(endyear, endmonth, endday)
        delta = d1 - d0
        diff = delta.days
        print(diff)
        d = startday
        m = startmonth
        y = startyear
        while diff >= 0:

            result, ntObj = getGraph(d, m, y, 1, "COMPOSITE")
            curDate = str(y) + "-" + str(m) + "-" + str(d)

            # call Sarada's functions:
            res1, dfTotRec = TotalBTCreceived(curDate, ntObj, dfTotRec)
            if res1 == 'Fail':
                return dfTotRec
            res1, dfLOActivity = LevelOfActivity(curDate, ntObj, dfLOActivity)
            if res1 == 'Fail':
                return dfLOActivity
            res1, dfSCC = StronglyConnectedComponents(curDate, ntObj, dfSCC)
            if res1 == 'Fail':
                return dfSCC
            res1, dfWCC = WeaklyConnectedComponents(curDate, ntObj, dfWCC)
            if res1 == 'Fail':
                return dfWCC
            res1, dfChainletsOcc = diffChainlets(curDate, ntObj, dfChainletsOcc)
            if res1 == 'Fail':
                return dfChainletsOcc
            res1, dfChainletsAocc = diffChainletsAmount(curDate, ntObj, dfChainletsAocc)
            if res1 == 'Fail':
                return dfChainletsAocc
            occMat, AmtOccMat = diffChainletMatrix(curDate, ntObj)

            #call Saumya's functions:
            res2,dfBTCCir= BTCirculation(curDate,ntObj,dfBTCCir)
            if res2 == 'Fail':
                return dfBTCCir
            res2,dfMostActive = MostActiveEntity(curDate,ntObj,dfMostActive)
            if res2 == 'Fail':
                return dfMostActive
            res2, dfClustering = clusteringCoefficientonGraph(curDate, ntObj, dfClustering)
            if res2 == 'Fail':
                return dfClustering
            res2, dfPearson = PearsonCoefficient(curDate, ntObj, dfPearson)
            if res2 == 'Fail':
                return dfPearson


            # calling Srija's analysis functions
            res7, dfAddDist = AddressDistAnalysis(curDate, ntObj, dfAddDist)
            if res7 == 'Fail':
                return dfAddDist
            res8, dfTranSize = TransactionSizeAnalysis(curDate, ntObj, dfTranSize)
            if res8 == 'Fail':
                return dfTranSize
            res9, dfAssortCo = assortativityCoefficientAnalysis(curDate, ntObj, dfAssortCo)
            if res9 == 'Fail':
                return dfAssortCo
            res = (datetime.strptime(curDate, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            res = datetime.strptime(res, '%Y-%m-%d')
            d = res.day
            m = res.month
            y = res.year
            diff -= 1

    except Exception as e:
        return e
    return "Success"


if __name__ == '__main__':
    print(getAnalysisResults(2009, 1, 9, 2009, 1, 9))
