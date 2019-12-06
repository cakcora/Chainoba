import sys

import pyprind


def progress_bar(title, max_value):
    """
    initialize the progress bar
    :param title:
    :param max_value:
    :return: ProgBar
    """

    bar = pyprind.ProgBar(max_value, stream=sys.stdout, title=title, bar_char='.')
    return bar

# def get_address_and_transaction_nodes(edge_list_df):
#     address_list = []
#     transaction_list = []
#     minimum_node_address_len = 34
#     for row in edge_list_df.iterrows():
#         if len(row[1]['source']) <= minimum_node_address_len:
#             address_list.append(row[1]['source'])
#         else:
#             transaction_list.append(row[1]['source'])
#
#         if len(row[1]['target']) <= minimum_node_address_len:
#             address_list.append(row[1]['target'])
#         else:
#             transaction_list.append(row[1]['target'])
#
#     return address_list, transaction_list
#
#
# def visualize_graph(graph):
#     # address_list, transaction_list = get_address_and_transaction_nodes(edge_list_df=edge_list_df)
#     color_map = []
#
#     A = nx.nx_agraph.to_agraph(graph)  # convert to a graphviz graph
#     A.layout()  # neato layout
#     A.draw("k5.ps")
