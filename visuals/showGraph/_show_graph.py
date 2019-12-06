import json
from pyvis.network import Network
import os
from tempfile import gettempdir


class ShowGraphABC:
    UNDIRECTED = 'undirected'
    DIRECTED = 'directed'

    def __init__(self, layout_type, output_suffix=""):
        self.graph = Network(height="750px", width="100%", directed=True)
        with open(os.path.join(os.path.dirname(__file__), 'layouts', '{}_layout.json'.format(layout_type))) as f:
            self.options = json.load(f)
        self.output_suffix = output_suffix

    def show_graph(self):
        self.graph.show(os.path.join(gettempdir(), "index_{}.html".format(self.output_suffix)))

    def add_node(self, *args, **kwargs):
        raise NotImplemented