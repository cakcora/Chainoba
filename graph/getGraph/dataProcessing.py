""" Aurthor: Tadepalli Sarada Kiranmayee """
""" Reference Papers are listed below:"""
"""1. Akcora, Cuneyt Gurcan, Yulia R. Gel, and Murat Kantarcioglu. "Blockchain: A
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

def VertexListCreation(datafObj, vertexlist):

    #Check whether is colomn is present or not
    try:
        if 'source' in datafObj.columns:
            vertex = datafObj[datafObj.columns[0]]
        else:
            vertex = None
        if 'target' in datafObj.columns:
            vertex1 = datafObj[datafObj.columns[1]]
        else:
            vertex1 = None

        #Consider only not null values
        vertex = vertex[vertex.notnull()]
        vertex1 = vertex1[vertex1.notnull()]
        total_vertex = pd.DataFrame()
        total_vertex = pd.concat([vertex,vertex1],ignore_index=True)

        #Consider unique vertices only
        df = pd.DataFrame(total_vertex, columns=list('a'))
        df=pd.DataFrame(df.a.unique())

        vertexlist=list(df[0])
    except Exception as e:
        return 'Fail', e
    return 'Success',vertexlist

def EdgeListCreation(datafObj):
    # drop all the rows with NaN
    try:
        datafObj = datafObj.dropna(how='any')
    except Exception as e:
        return 'Fail', e
    return 'Success',datafObj