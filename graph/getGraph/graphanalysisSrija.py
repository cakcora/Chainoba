import pandas as pd

def CurrentBalance(ntObj):
    df = pd.DataFrame(columns=["Node", "Current Balance"])
    try:

        outdegree = dict(ntObj.out_degree(weight='weight'))
        indegree = dict(ntObj.in_degree(weight='weight'))
        for ele, inval in indegree.items():
            if len(ele) != 64:
                current = (inval - outdegree[ele])
                df = df.append({"Node": ele, "Current Balance":current}, ignore_index = True)
                #print(ele+":"+str(current))
    except Exception as e:
        return 'Fail', e
    return "Success",df


def BitcoinSent(ntObj):
    dfObj = pd.DataFrame(columns=["Node", "Bitcoin Sent"])
    try:
        outdegree = dict(ntObj.out_degree(weight='weight'))
        for ele, outval in outdegree.items():
            if len(ele) != 64:
                dfObj = dfObj.append({"Node": ele, "Bitcoin Sent":outval}, ignore_index=True)
    except Exception as e:
        return 'Fail', e
    return "Success",dfObj
