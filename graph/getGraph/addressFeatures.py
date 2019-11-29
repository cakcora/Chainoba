import pandas as pd
from graph.getGraph.getAPIData import getGraph
from graph.getGraph.graphanalysisSrija import CurrentBalance,BitcoinSent
from graph.getGraph.graphAnalysis import levelOfActivity,amountToAddress
import numpy as np

def getFeatures(day,month,year,feature):
    df = pd.DataFrame()
    try:
        result, networkxObj = getGraph(day, month, year, 1,"COMPOSITE")
        if result=='Success':
            if feature =='LEVEL_OF_ACTIVITY':
                result, df = levelOfActivity(networkxObj)
                df.index = np.arange(1, len(df) + 1)
            elif feature =='TOTAL_BTC_RECEIVED':
                result, df = amountToAddress(networkxObj)
                df.index = np.arange(1, len(df) + 1)
            elif feature =='TOTAL_BTC_SENT':
                result, df = BitcoinSent(networkxObj)
            elif feature =='CURRENT_BALANCE':
                result, df = CurrentBalance(networkxObj)
            else:
                return 'Fail','Incorrect node feature'
        else:
            return 'Fail', networkxObj
    except Exception as e:
        return 'Fail', e
    return 'Success', df

