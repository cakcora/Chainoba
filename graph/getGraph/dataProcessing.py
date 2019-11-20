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