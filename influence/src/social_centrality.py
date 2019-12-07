"""
A source file to call and test all functions in influence.centralities.py
"""

import influence.driver as influence_driver

print ("influence_driver.calculate_degree_centrality_for_nodes()")
influence_driver.calculate_degree_centrality_for_nodes()
print ("influence_driver.calculate_degree_centrality_for_graph()")
influence_driver.calculate_degree_centrality_for_graph()
print ("influence_driver.calculate_betweenness_centrality_for_graph()")
influence_driver.calculate_betweenness_centrality_for_graph()
print ("influence_driver.calculate_betweenness_centrality_for_nodes()")
influence_driver.calculate_betweenness_centrality_for_nodes()
print ("influence_driver.calculate_closeness_centrality_for_graph()")
influence_driver.calculate_closeness_centrality_for_graph()
print ("influence_driver.calculate_generalized_hoede_bakker_index()")
influence_driver.calculate_generalized_hoede_bakker_index()

