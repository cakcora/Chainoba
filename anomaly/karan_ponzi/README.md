# Detection of Ponzi Schemes using Random Forest

#### Files added:
#####1. api/account_data_collection.py
Fetches the data from Etherscan.io using the addresses provided by GetPonziAnomalyDataEndpoint()
#####2. random_forest_ponzi_detection.py : 
Builds and executes the random forest model based on the data gathered from get_account_data(). Also calculates the feature importance and stats about decision trees
#####3. graph_comparison_ponzi.py
Bar graph to compare data of Ponzi Schemes vs Non Ponzi Schemes
#####4. api_key.json
Contains API key to get data from Ethersan.io