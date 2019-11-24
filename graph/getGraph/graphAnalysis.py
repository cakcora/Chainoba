import pandas as pd

def amountToAddress(dfobject):
    try:
        in_deg_amount = dfobject.in_degree(weight='weight')
        da = pd.DataFrame(in_deg_amount, columns=["Node", "Amount"])
        da['da_length'] = da['Node'].apply(len)
        dx = da[da.da_length != 64]
        dx = dx[["Node", "Amount"]]
    except Exception as e:
        return 'Fail', e
    return "Success", dx


def levelOfActivity(dfObject):
    try:
        in_deg = dfObject.in_degree
        df1 = pd.DataFrame(in_deg, columns=["Node", "In"])
        out = dfObject.out_degree
        df2 = pd.DataFrame(out, columns=["Node", "Out"])
        merge_frame = pd.merge(df1, df2, how="inner")
        m = merge_frame[["In", "Node", "Out"]]
        m = pd.DataFrame(m, columns=["In", "Node", "Out"])
        # Find total number of chianlets
        m['node_length'] = m["Node"].apply(len)
        m = m[m.node_length != 64]
        m['total_degree']=m['In']+m['Out']
        ml=m[["Node","total_degree"]]
        ml = pd.DataFrame(ml, columns=["Node","total_degree"])
    except Exception as e:
        return 'Fail', e
    return "Success", ml