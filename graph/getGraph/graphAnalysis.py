""" Aurthor: Tadepalli Sarada Kiranmayee

Summary: Address features: Functions for Amount received to Address,level of activity

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