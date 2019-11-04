def getBlockIds(dd=9, mm=1, yy=2009, dateOff=1):
    """
    Method to get block ids (date_offset maximum value 31)
    """
    return 'Success', "blockIds"


def getTransactionIds(blockIds):
    """
    Method to get transactions by block ids (block_ids maximum size 5)
    """

    return 'Success', "transIds"


def getTransactionDetails(transId):
    """
    Method to get transactions' details by transaction id (transaction_ids maximum size 10)
    """

    return 'Success', "response"



def getGraph(dd=9, mm=1, yy=2009, dOffset=1, graphType, path):
    """
    Method to initiate the process of extraction of data and formation of the corresponding graph at the given path
    """

    return 'Success', 'csv file at its given path'

def Extract_MainGraph(Transansaction_data,path):
    """
    Method to extract the required detail of input address and transaction hash to form a csv file

    """
    return "Graph.csv"

def Extract_AddressGraph(transaction_data,path):
    """
        Method to extract the required detail of input address and output address to form a Address.csv file

    """
    return "Address.csv"

def Clustering_co_efficient(edgelist_file_path):
    """

    Method to get the links between the related node i.e how many nodes transfer bitcoin to same address find those addresses
    """
    return "Clustering_co-efficient"

def Pearson_co_efficient(edgelist_file_path):
    """
    Method to get the large indegree node will have large out degree nodes
    """
    return "Pearson_co-efficient"

def Bitcoin_Circulation(edgelist_file_path):
    """
    Method to get the Bitcoin Circulation in a system
    """
    return "Bitcoin_Circulation"

def Maximal_Balance(edgelist_file_path):
    """
        Method to get the Maximal_Balance of address
    """
    return "Maximal_Balance"

def Most_Active_entity(edgelist_file_path):
    """
        Method to get the those activity entity which have more amount of bitcoin
    """
    return "Most_Active_entity"

def assortativityAnalysis(edgelistFilePath):
    """
        Method to analyse assortativity of the bitcoin system.
    """
    return "Success"

def correlationDegreeAnalysis(edgelistFilePath):
    """
        Method to analyse correlatio degree of the bitcoin system
    """
    return "Success"

def addressDistAnalysis(edgelistFilePath):
    """
        Method to analyse address distribution of the bitcoin system
    """
    return "Success"

def currentBalAnalysis(edgelistFilePath):
    """
        Method to analyse current balance of the bitcoin system
    """
    return "Success"

def transactionSizeAnalysis(edgelistFilePath):
    """
            Method to analyse transaction size of the bitcoin system on daily data
        """
    return "Success"


def chainletsInTime(edgelistFilePath):
    """
    Method to calculate the number of chainlets with amount
    """
    return "Number_of_Chainlets_with_Amount"
def stronglyConnectedComponents(edgelistFIlePath):
    """
    Method to find the strongly connected components in the bitcoin system on daily basis data
        """
    return "Count_of_SCC"
def weaklyConnectedComponents(edgelistFilePath):
    """
    Method to find the weakly connected components in the bitcoin system on daily basis data
        """
    return "Count_of_WCC"
def nodeIdentity(edgeListFilePath):
    """
    Method to identify the node in the bitcoin system data
        """
    return "Success"
def totalBitcoinInAddress(edgeListFilePath):
    """
    Method to calculate total bitcoin received in an address

    """
    return "Amount_of_Bitcoins_from_address"
def levelOfActivity(edgeListFilePath):
    """
    Number of transactions each address is involved in.
        """
     return "Success"