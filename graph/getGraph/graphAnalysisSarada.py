"""Graph Analysis by Tadepalli Sarada Kiranmayee"""
import networkx as nx
import pandas as pd
import numpy as np
from graph.getGraph.getAPIData import getGraph
def TotalBTCreceived(curDate,ntObj,dfTotRec):
    """ Total the number of BTC received by the addresses in the graph on daily basis"""
    try:
        in_deg_amount = ntObj.in_degree(weight='weight')
        temp = pd.DataFrame(in_deg_amount, columns=["Node", "Amount"])

        temp['trans_length'] = temp['Node'].apply(len)
        dfAmtRec = temp[temp.trans_length != 64]
        dfAmtRec = dfAmtRec[["Node", "Amount"]]
        a = b = c= d = e = f =g= 0
        for index, row in dfAmtRec.iterrows():
            row['Amount'] = row['Amount'] / 100000000
            if row['Amount'] < 1:
                a += 1
            elif row['Amount'] < 10:
                b += 1
            elif row['Amount'] < 100:
                c += 1
            elif row['Amount'] < 1000:
                d += 1
            elif row['Amount'] < 10000:
                e += 1
            elif row['Amount'] < 50000:
                f += 1
            else:
                g += 1
        dfTotRec = dfTotRec.append({ "Date":curDate ,"Number of addresses with Total BTC received [0,1)": a,
                 "Number of addresses with Total BTC received [1,10)": b,
                 "Number of addresses with Total BTC received [10,100)":c,
                 "Number of addresses with Total BTC received [100,1000)": d,
                 "Number of addresses with Total BTC received [1000,10000)": e,
                 "Number of addresses with Total BTC received [10000,50000)": f,
                 "Number of addresses with Total BTC received greater than equal to 50000": g}, ignore_index=True)
        return "success",dfTotRec

    except Exception as e:
        return 'Fail', e

def diffChainlets(curDate,ntObj,dfChainletsOcc):
    """total number of different chainlets(Split,Merge and Transition) in a graph"""
    try:
        in_deg = ntObj.in_degree
        df1 = pd.DataFrame(in_deg, columns=["Node", "In"])
        out = ntObj.out_degree
        df2 = pd.DataFrame(out, columns=["Node", "Out"])
        merge_frame = pd.merge(df1, df2, how="inner")
        m = merge_frame[["In", "Node", "Out"]]
        m = pd.DataFrame(m, columns=["In", "Node", "Out"])
        m['node_length'] = m["Node"].apply(len)
        m = m[m.node_length == 64]
        m = m[["In", "Node", "Out"]]
        splitNumber=mergeNumber=transitionNumber=0
        # Total Number of Split Chainlets
        m1 = m[m["In"] > 0]
        s=m1[m1.In < m1.Out]

        splitNumber=s['In'].count()
        m=m1[m1.In > m1.Out]
        mergeNumber=m['In'].count()
        t=m1[m1.In == m1.Out]
        transitionNumber=t['In'].count()
        dfChainletsOcc = dfChainletsOcc.append({"Date":curDate, "Occurrence of split Chainlets":splitNumber,
                           "Occurrence of merge Chainlets":mergeNumber,
                           "Occurrence of transition Chainlets":transitionNumber},ignore_index=True)
        return "Success",dfChainletsOcc
    except Exception as e:
        return 'Fail', e
def diffChainletMatrix(curDate,dbObject):
    """Occurrence matrix and Amount Matrix of 20X20 Occurrence Matrix"""
    try:
        ind = dict(dbObject.in_degree)
        aind = dict(dbObject.in_degree(weight='weight'))
        outd = dict(dbObject.out_degree)
        occ = np.zeros((20, 20))
        aocc = np.zeros((20, 20))
        for ele, value in ind.items():
            if len(ele) == 64:
                out = outd[ele]
                amt = aind[ele]
                if (value > 0):
                    occ[int(value)][int(out)] += 1
                    aocc[int(value)][int(out)] += amt
        print("Date:",curDate)
        return occ,aocc
    except Exception as e:
        return 'Fail', e
def diffChainletsAmount(curDate,ntObj,dfChainletsAocc):
    """total amount of different chainlets(Split,Merge and Transition) in a graph """
    try:
        ind = dict(ntObj.in_degree)
        aind = dict(ntObj.in_degree(weight='weight'))
        outd = dict(ntObj.out_degree)
        splitAmt=mergeAmt=transitionAmt=0
        for ele, value in ind.items():
            if len(ele) == 64:
                if(value>0):
                    if(value<outd[ele]):
                        splitAmt += aind[ele]
                    elif (value > outd[ele]):
                        mergeAmt += aind[ele]
                    elif (value > outd[ele]):
                        transitionAmt += aind[ele]

        dfChainletsAocc = dfChainletsAocc.append({"Date": curDate,"Amount of split Chainlets": format((splitAmt/100000000), '.2f'),
                                                "Amount of merge Chainlets": format((mergeAmt/100000000), '.2f'),
                                                "Amount of transition Chainlets": format((transitionAmt/100000000), '.2f')},ignore_index=True)
        return "Success", dfChainletsAocc
    except Exception as e:
        return 'Fail', e

def StronglyConnectedComponents(curDate,ntObj,dfSCC):
    """Number of Strongly Connected Components in the graph"""
    try:
        count=0
        for i in nx.strongly_connected_components(ntObj):
            count += 1
        dfSCC = dfSCC.append({"Date":curDate,"Number of Strongly connected components":count},ignore_index=True)
        return "Success", dfSCC
    except Exception as e:
        return 'Fail', e
def WeaklyConnectedComponents(curDate,ntObj,dfWCC):
    """Number of Weakly Connected Components in the graph"""
    try:
        count = 0
        for i in nx.weakly_connected_components(ntObj):
            count += 1
        dfWCC = dfWCC.append({"Date": curDate, "Number of Weakly connected components": count},ignore_index=True)
        return "Success", dfWCC
    except Exception as e:
        return 'Fail', e

def LevelOfActivity(curDate,ntObj,dfLOActivity):
    """Analysis of level of Activity for the all the addresses on daily basis """
    try:
        in_deg = ntObj.in_degree
        df1 = pd.DataFrame(in_deg, columns=["Node", "In"])
        out = ntObj.out_degree
        df2 = pd.DataFrame(out, columns=["Node", "Out"])
        merge_frame = pd.merge(df1, df2, how="inner")
        m = merge_frame[["In", "Node", "Out"]]
        m = pd.DataFrame(m, columns=["In", "Node", "Out"])
        m['node_length'] = m["Node"].apply(len)
        m = m[m.node_length != 64]
        m['total_degree']=m['In']+m['Out']
        ml=m[["Node","total_degree"]]
        #ml = pd.DataFrame(ml, columns=["Node","total_degree"])
        a = b = c = d = e = f = g = 0
        for index, row in ml.iterrows():
            if row['total_degree'] < 2:
                a += 1
            elif row['total_degree'] < 5:
                b += 1
            elif row['total_degree'] < 10:
                c += 1
            elif row['total_degree'] < 100:
                d += 1
            elif row['total_degree'] < 1000:
                e += 1
            elif row['total_degree'] < 5000:
                f += 1
            else:
                g += 1
        dfLOActivity = dfLOActivity.append({"Date":curDate, "Number of addresses with Level of activity [1,2)":a,
                                             "Number of addresses with Level of activity [2,5)":b,
                                             "Number of addresses with Level of activity [5,10)":c,
                                             "Number of addresses with Level of activity [10,100)":d,
                                             "Number of addresses with Level of activity [100,1000)":e,
                                             "Number of addresses with Level of activity [1000,5000)":f,
                                             "Number of addresses with Level of activity greater than equal to 5000":g},ignore_index=True)
        return "Success", dfLOActivity
    except Exception as e:
        return 'Fail', e



