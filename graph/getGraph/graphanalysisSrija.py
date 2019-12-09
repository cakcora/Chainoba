""" Author: Srija Srivastava"""
"""To perform statistical and structural analysis on Bitcoin composite graph and store the results simultaneously"""
""" Reference Papers are listed below:"""
"""1. Akcora, Cuneyt Gurcan, Yulia R. Gel, and Murat Kantarcioglu. "Blockchain: A
graph primer." arXiv preprint arXiv:1708.08749 (2017).
2. Chen, Ting, Yuxiao Zhu, Zihao Li, Jiachi Chen, Xiaoqi Li, Xiapu Luo, Xiaodong
Lin, and Xiaosong Zhange. "Understanding ethereum via graph analysis."
In IEEE INFOCOM 2018-IEEE Conference on Computer Communications, pp.
1484-1492. IEEE, 2018.
3. Ron, Dorit, and Adi Shamir. "Quantitative analysis of the full bitcoin transaction
graph." In International Conference on Financial Cryptography and Data
Security, pp. 6-24. Springer, Berlin, Heidelberg, 2013."""


import networkx as nx
import pandas as pd
from datetime import date, datetime, timedelta
import requests
from graph.getGraph.getAPIData import getGraph

ADD_URL="http://159.203.28.234:5000/bitcoin/address_distribution"
TRANS_URL="http://159.203.28.234:5000/bitcoin/transaction_size"
ASSORT_URL ="http://159.203.28.234:5000/bitcoin/assortativity_coefficient"
CURRENT_URL ="http://159.203.28.234:5000/bitcoin/current_balance"

def CurrentBalance(ntObj):
    """To get current balance feature of addresses"""
    df = pd.DataFrame(columns=["Node", "Current Balance"])
    try:

        outdegree = dict(ntObj.out_degree(weight='weight'))
        indegree = dict(ntObj.in_degree(weight='weight'))
        for ele, inval in indegree.items():
            if len(ele) != 64:
                current = (inval - outdegree[ele])
                df = df.append({"Node": ele, "Current Balance": current}, ignore_index=True)
    except Exception as e:
        return 'Fail', e
    return "Success", df


def BitcoinSent(ntObj):
    """To get Bitcoin sent feature of addresses"""
    dfObj = pd.DataFrame(columns=["Node", "Bitcoin Sent"])
    try:
        outdegree = dict(ntObj.out_degree(weight='weight'))
        for ele, outval in outdegree.items():
            if len(ele) != 64:
                dfObj = dfObj.append({"Node": ele, "Bitcoin Sent": outval}, ignore_index=True)
    except Exception as e:
        return 'Fail', e
    return "Success", dfObj


def AddressDistAnalysis(date, netxObj, dfObj):
    """To get the address distribution of the Bitcoin system at the end of each day"""
    try:
        totalAddr = 0
        count = 0
        outdegree = list(netxObj.out_degree)
        for ele in outdegree:
            if len(ele[0]) != 64:
                totalAddr += 1
                if ele[1] == 0:
                    count += 1
        dfObj = dfObj.append({"Date": date, "Total Addresses": totalAddr,
                              "Receive-only Address %": (count / totalAddr) * 100,
                              "Send/receive Address %": ((totalAddr - count) / totalAddr) * 100}, ignore_index=True)

        data = {
            'Date': date,
            'ReceiveOnlyPer': ((count / totalAddr) * 100),
            'SendReceivePer': (((totalAddr - count) / totalAddr) * 100)
        }
        r = requests.post(url=ADD_URL, data=data)

    except Exception as e:
        return 'Fail', e
    return "Success", dfObj


def CurrentBalanceAnalysis(year, month, day):
    """To get the Current Balance of each address in the Bitcoin system at the end of each day"""
    try:
        dfObj = pd.DataFrame(columns=["Date", "Number of addresses with Current balance [0,1)",
                                      "Number of addresses with Current balance [1,10)",
                                      "Number of addresses with Current balance [10,100)",
                                      "Number of addresses with Current balance [100,1000)",
                                      "Number of addresses with Current balance [1000,10000)",
                                      "Number of addresses with Current balance [10000,50000)",
                                      "Number of addresses with Current balance greater than equal to 50000"])
        d0 = date(2009, 1, 9)
        d1 = date(year, month, day)
        delta = d1 - d0
        diff = delta.days
        print(diff)
        d = 9
        m = 1
        g = nx.MultiDiGraph()
        while diff >= 0:

            result, dfobject = getGraph(d, m, year, 1, "COMPOSITE")
            g = nx.compose(g, dfobject)

            lt1 = lt10 = lt100 = lt1000 = lt10000 = lt50000 = gt50000 = 0
            outdegree = dict(g.out_degree(weight='weight'))
            indegree = dict(g.in_degree(weight='weight'))
            # print(outdegree)
            for ele, inval in indegree.items():
                if len(ele) != 64:
                    current = (inval - outdegree[ele]) / 100000000
                    if current < 1:
                        lt1 += 1
                    elif current < 10:
                        lt10 += 1
                    elif current < 100:
                        lt100 += 1
                    elif current < 1000:
                        lt1000 += 1
                    elif current < 10000:
                        lt10000 += 1
                    elif current < 50000:
                        lt50000 += 1
                        # print(ele,current)
                    else:
                        gt50000 += 1
            dfObj = dfObj.append({"Date": str(year) + "-" + str(m) + "-" + str(d),
                                  "Number of addresses with Current balance [0,1)": lt1,
                                  "Number of addresses with Current balance [1,10)": lt10,
                                  "Number of addresses with Current balance [10,100)": lt100,
                                  "Number of addresses with Current balance [100,1000)": lt1000,
                                  "Number of addresses with Current balance [1000,10000)": lt10000,
                                  "Number of addresses with Current balance [10000,50000)": lt50000,
                                  "Number of addresses with Current balance greater than equal to 50000": gt50000
                                  },
                                 ignore_index=True)
            dates=str(year) + "-" + str(m) + "-" + str(d)
            data = {
                'Date': dates,
                'CurrBal1': lt1,
                'CurrBal10': lt10,
                'CurrBal100': lt100,
                'CurrBal1000': lt1000,
                'CurrBal10000': lt10000,
                'CurrBal50000': lt50000,
                'CurrBalGT50000': gt50000
            }
            r = requests.post(url=CURRENT_URL, data=data)

            x = str(year) + "-" + str(m) + "-" + str(d)
            res = (datetime.strptime(x, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            res = datetime.strptime(res, '%Y-%m-%d')
            d = res.day
            m = res.month
            diff -= 1

    except Exception as e:
        return 'Fail', e
    return "Success", dfObj


def TransactionSizeAnalysis(date, netxObj, dfObj):
    """To get the Transaction Size of each transaction in the Bitcoin system at the end of each day"""
    try:
        lt1 = lt10 = lt100 = lt5000 = lt20000 = lt50000 = gt50000 = 0
        outdegree = dict(netxObj.out_degree(weight='weight'))
        for ele, outval in outdegree.items():
            if len(ele) == 64:
                size = outval / 100000000
                if size < 1:
                    lt1 += 1
                elif size < 10:
                    lt10 += 1
                elif size < 100:
                    lt100 += 1
                elif size < 5000:
                    lt5000 += 1
                elif size < 20000:
                    lt20000 += 1
                elif size < 50000:
                    lt50000 += 1
                else:
                    gt50000 += 1
        dfObj = dfObj.append(
            {"Date": date, "Number of transaction of size [0,1)": lt1, "Number of transaction of size  [1,10)": lt10,
             "Number of transaction of size  [10,100)": lt100, "Number of transaction of size  [100,5000)": lt5000,
             "Number of transaction of size  [5000,20000)": lt20000,
             "Number of transaction of size  [20000,50000)": lt50000,
             "Number of transaction of size  greater than equal to 50000": gt50000}, ignore_index=True)
        data = {
            'Date': date,
            'TransSizeLT1': lt1,
            'TransSizeLT10': lt10,
            'TransSizeLT100': lt100,
            'TransSizeLT5000': lt5000,
            'TransSizeLT20000': lt20000,
            'TransSizeLT50000':lt50000,
            'TransSizeGT50000': gt50000
        }
        r = requests.post(url=TRANS_URL, data=data)
    except Exception as e:
        return 'Fail', e
    return "Success", dfObj


def assortativityCoefficientAnalysis(date, netxObj, dfObj):
    """To get the Assortativity coefficient of Bitcoin system at the end of each day"""
    try:

        assortCoeff = nx.degree_assortativity_coefficient(netxObj)
        dfObj = dfObj.append({"Date": date, "Assortativity coefficient": assortCoeff}, ignore_index=True)
        data = {
            'Date': date,
            'AssortCoeff': assortCoeff
        }
        r = requests.post(url=ASSORT_URL, data=data)
    except Exception as e:
        return 'Fail', e
    return "Success", dfObj

