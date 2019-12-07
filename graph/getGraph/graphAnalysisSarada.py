""" Aurthor: Tadepalli Sarada Kiranmayee


Summary: Analysis on Composite Graph:
1)Total Bitcoins received
2)Level of activity of address nodes,
3)Number of chainlets(merge/split/transition)
4)Incoming amount to chainlets
5)Number of chainlets in 20X20 matrix
6)Amount of incoming chianlets in 20X20 matrix
7) Number of Strongly Connected Components
8) number of Weakly Connected Components

Reference Papers are listed below:
1. Akcora, Cuneyt Gurcan, Yulia R. Gel, and Murat Kantarcioglu. "Blockchain: A
graph primer." arXiv preprint arXiv:1708.08749 (2017).
2. Akcora, C. G., Dey, A. K., Gel, Y. R., & Kantarcioglu, M. (2018, June). Forecasting
bitcoin price with graph chainlets. In Pacific-Asia Conference on Knowledge
Discovery and Data Mining (pp. 765-776). Springer, Cham.
3. Chen, Ting, Yuxiao Zhu, Zihao Li, Jiachi Chen, Xiaoqi Li, Xiapu Luo, Xiaodong
Lin, and Xiaosong Zhange. "Understanding ethereum via graph analysis."
In IEEE INFOCOM 2018-IEEE Conference on Computer Communications, pp.
1484-1492. IEEE, 2018.
4. Ron, Dorit, and Adi Shamir. "Quantitative analysis of the full bitcoin transaction
graph." In International Conference on Financial Cryptography and Data
Security, pp. 6-24. Springer, Berlin, Heidelberg, 2013."""


import networkx as nx
import pandas as pd
import numpy as np
import requests

from graph.getGraph.getAPIData import getGraph
BTC_REC_URL="http://159.203.28.234:5000/bitcoin/total_btc_received"
LOA_URL="http://159.203.28.234:5000/bitcoin/activity_level"
SCC_URL="http://159.203.28.234:5000/bitcoin/strongly_connected_component"
WCC_URL="http://159.203.28.234:5000/bitcoin/weakly_connected_component"
ChianletsOCC_URL="http://159.203.28.234:5000/bitcoin/chainlets_occurance"
ChianletsOCCAmt_URL="http://159.203.28.234:5000/bitcoin/chainlets_occurance_amount"

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

        data = {"Date" : curDate,"BTCrecLT1": a,"BTCrecLT10":b,"BTCrecLT100": c,"BTCrecLT1000": d,
                "BTCrecLT10000": e,"BTCrecLT50000":f,"BTCrecGT50000":g
        }
        r = requests.post(url=BTC_REC_URL, data=data)

    except Exception as e:
        return 'Fail', e
    return "success", dfTotRec


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
        data = {"Date": curDate,"SplitChlt": splitNumber,"MergeChlt": mergeNumber,"TransitionChlt": transitionNumber
                }
        r = requests.post(url=ChianletsOCC_URL, data=data)

    except Exception as e:
        return 'Fail', e
    return "Success", dfChainletsOcc

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
                    aocc[int(value)][int(out)] += amt/100000000
        print("Date:",curDate)

    except Exception as e:
        return 'Fail', e
    return occ, aocc

def diffChainletsAmount(curDate,ntObj,dfChainletsAocc):
    """total amount of different chainlets(Split,Merge and Transition) in a graph """
    try:
        ind = dict(ntObj.in_degree)
        aind = dict(ntObj.in_degree(weight='weight'))
        outd = dict(ntObj.out_degree)
        splitAmt=mergeAmt=transitionAmt=0.0
        for ele, value in ind.items():
            if len(ele) == 64:
                if (value > 0):
                    if(value<outd[ele]):
                        splitAmt += aind[ele]
                    elif (value > outd[ele]):
                        mergeAmt += aind[ele]
                    elif (value > outd[ele]):
                        transitionAmt += aind[ele]

        dfChainletsAocc = dfChainletsAocc.append({"Date": curDate,"Amount of split Chainlets": format((splitAmt/100000000), '.2f'),
                                                "Amount of merge Chainlets": format((mergeAmt/100000000), '.2f'),
                                                "Amount of transition Chainlets": format((transitionAmt/100000000), '.2f')}
                                                 ,ignore_index=True)
        data = {"Date": curDate, "SplitChAmt": (splitAmt/100000000),
                "MergeChAmt": (mergeAmt/100000000),
                "TransitionChAmt":(transitionAmt/100000000)
                }

        r = requests.post(url=ChianletsOCCAmt_URL, data=data)
        print(r.text)
    except Exception as e:
        return 'Fail', e
    return "Success", dfChainletsAocc

def StronglyConnectedComponents(curDate,ntObj,dfSCC):
    """Number of Strongly Connected Components in the graph"""
    try:
        l=nx.number_strongly_connected_components(ntObj)
        dfSCC = dfSCC.append({"Date":curDate,"Number of Strongly connected components":l},ignore_index=True)
        data = {"Date": curDate, "SCC": l }
        r = requests.post(url=SCC_URL, data=data)


    except Exception as e:
        return 'Fail', e
    return "Success", dfSCC

def WeaklyConnectedComponents(curDate,ntObj,dfWCC):
    """Number of Weakly Connected Components in the graph"""
    try:
        a = nx.number_weakly_connected_components(ntObj)
        dfWCC = dfWCC.append({"Date": curDate, "Number of Weakly connected components": a},ignore_index=True)
        data = {"Date": curDate, "WCC": a}
        r = requests.post(url=WCC_URL, data=data)


    except Exception as e:
        return 'Fail', e
    return "Success", dfWCC

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
        data={"Date": curDate,"LOALT2": a,"LOALT5": b,"LOALT10": c,"LOALT100":d,"LOALT1000":e,"LOALT5000":f,
              "LOAGT5000":g}
        r=requests.post(url=LOA_URL, data=data)



    except Exception as e:
        return 'Fail', e
    return "Success", dfLOActivity

