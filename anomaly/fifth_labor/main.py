import argparse
import sys
import textwrap

sys.path.append("../..")

import anomaly.fifth_labor.DataLoader as dl
import anomaly.fifth_labor.GraphHelper as gh
import anomaly.fifth_labor.GraphX as gx

"""
CLI for the fifth labor project
"""

def run(args):
    """
    - parse the parameters
    - load ransomware data
    - build the graph
    - find the loops
    - find split addresses

    :param args:
    """
    __number_of_ransomware__ = args.n
    __ransomware_file_name__ = args.f
    __find_loop__ = args.l
    __find_split_address__ = args.s
    __output_address_threshold__ = args.o
    print("------------- Parameter Received-----------------------------------------")
    print('Number of ransomware address: {}'.format(__number_of_ransomware__))
    print('Ransomware file:  {}'.format(__ransomware_file_name__))
    print('Find loop: {}'.format(__find_loop__))
    print('Find split: {}'.format(__find_split_address__))
    print('Split output address threshold: {}'.format(__output_address_threshold__))
    print("-------------------------------------------------------------------------")

    try:
        data_loader = dl.DataLoader(number_of_address=__number_of_ransomware__,
                                    file_name=__ransomware_file_name__)
        ransomware_data = data_loader.load_ransomware_data()
        print('Ransomware address loading complete.\n')

    except Exception as e:
        print(e)
        return
    graph_helper = gh.GraphHelper(ransomware_df=ransomware_data)
    edge_list = graph_helper.get_edge_list()

    graph = gx.GraphX(edge_list=edge_list)
    graph_ref = graph.build_graph()
    print("Graph building successful!!!!\n")

    number_of_nodes = graph_ref.number_of_nodes()
    number_of_edges = graph_ref.number_of_edges()

    print('Number of nodes: {}'.format(number_of_nodes))
    print('Number of edges: {}'.format(number_of_edges))

    if __find_loop__ is True:
        print('\nFinding loops..')
        loop_list = graph.get_loop()
        print('Number of loop detected: {}'.format(str(len(loop_list))))

    if __find_split_address__ is True:
        print('\nFinding Split address..')
        split_node_list = graph.get_split_nodes(output_address_threshold=__output_address_threshold__)
        print('Number of split node detected: {}'.format(str(len(split_node_list))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='main.py',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
                    Submitted as COMP7570 Blockchain Analysis Course Project
                                    by Tanbir Ahmed
                    Code available at:
                    https://github.com/cakcora/Chainoba/tree/fifth_labor_nx/anomaly/fifth_labor
            
        '''),
        description=textwrap.dedent('''\
                                The Fifth labor:
                  How to launder the coins gained from a BitcoinHeist
                            --------------------------------
                            Detecting Linkage Behavior 
                            1. Looping behavior 
                            2. Splitting behavior
                            ''')
    )

    parser.add_argument('-v', action='version',
                        version='%(prog)s 1.0')
    parser.add_argument('-n', type=int, help='Number of ransomware (default=1)', default=1)
    parser.add_argument('-f', help='File name for ransomware addresses (default=chainletElimination.txt)',
                        default='chainletElimination.txt')
    parser.add_argument('-l', help='Find Loops in the network (default=True)',
                        type=lambda x: (str(x).lower() == 'true'),
                        default=True)
    parser.add_argument('-s', help='Find Split addresses (default=True)', type=lambda x: (str(x).lower() == 'true'),
                        default=True)
    parser.add_argument('-o', help='Output address threshold (default=2)', type=int,
                        default=2)
    args = parser.parse_args()

    run(args)

    # parser.print_help()
