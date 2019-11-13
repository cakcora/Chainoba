import pandas as pd

def VertexListCreation(temp_path,vertexlist):

    #read the csv to append vertexlist
    df=pd.read_csv(temp_path,names=["From","To"])
    df=df[1:]

    #Check whether is colomn is present or not

    if 'From' in df.columns:
        vertex = df[df.columns[0]]
    else:
        vertex = None
    if 'To' in df.columns:
        vertex1 = df[df.columns[1]]
    else:
        vertex1 = None

    #Consider only not null values
    vertex = vertex[vertex.notnull()]
    vertex1 = vertex1[vertex1.notnull()]
    total_vertex = pd.DataFrame()
    total_vertex=pd.concat([vertex,vertex1],ignore_index=True)

    #Consider unique vertices only
    df = pd.DataFrame(total_vertex, columns=list('a'))
    df=pd.DataFrame(df.a.unique())

    #create csv for unique vertices
    df.to_csv(vertexlist,header=False,index=False)
    return 'Success'

def EdgeListCreation(temp_path,edgelist):

    #create the dataframe for edgelist
    df = pd.read_csv(temp_path)
    df1 = pd.DataFrame(df, columns=list('ab'))

    # drop all the rows with NaN
    df1 = df.dropna(how='any')

    # convert the dataframe to csv
    df1.to_csv(edgelist,header=False,index=False)
    return 'Success'
