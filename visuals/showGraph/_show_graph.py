import json
from pyvis.network import Network
import os
from tempfile import gettempdir


class ShowGraphABC:
    """
    Abstract super class. Methods of this class are over-ridden by the following classes:
    ShowTransactionGraph
    ShowAddressGraph
    ShowPath
    ShowCompositeGraph
    ShowCluster
    """
    # Two enums defined for layouts for two json files: directed_layout.json and undirected_layout.json
    _UNDIRECTED = 'undirected'
    _DIRECTED = 'directed'

    def __init__(self, layout_type, output_suffix=""):
        """
        Initialize the browser based on width, height and other properties defined in json files.
        :param layout_type: The type of layout that needs to be applied on the output browser.
        :param output_suffix: The name of the HTML file.
        """
        self.graph = Network(height="750px", width="100%", directed=True)
        with open(os.path.join(os.path.dirname(__file__), 'layouts', '{}_layout.json'.format(layout_type))) as f:
            self.options = json.load(f)
        self.output_suffix = output_suffix

    def show_graph(self):
        """
        This abstract method needs to be over-ridden by all the classes in this module.
        Shows the output graph in a browser.
        :return:
        """
        self.graph.show(os.path.join(gettempdir(), "index_{}.html".format(self.output_suffix)))

    def add_node(self, *args, **kwargs):
        """
        Abstract method to be over-ridden by all classes who extend ShowGraphABC class.
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplemented