# Visuals

**This package includes visualization modules based on graphs in [Blockchain: A Graph Primer](https://arxiv.org/abs/1708.08749).**

### Install requirements
```
pip install -r visuals/requirements.txt
```

### Project structure
```python
visuals/
├── show_graph/
│   ├── layouts/
│   │   ├── directed_layout.json
│   │   └── undirected_layout.json
│   ├── _show_graph.py
│   ├── show_address_graph.py
│   ├── show_cluster.py
│   ├── show_composite_graph.py
│   ├── show_path.py
│   └── show_transaction_graph.py
├── show_plot/
└── └── visualization_manager.py
├── example_driver.py
├── README.py
└── requirements.txt
```

### visuals/show_graph  
Implementations of all graphs proposed in 
* <b>ShowAddressGraph</b>: visualize address graph.<br>
* <b>ShowCluster</b>: visualize address graph and clusters which each address belongs to it. <br>  
* <b>ShowCompositeGraph</b>: visualize composite graph. <br>
* <b>ShowPath</b>: visualize a single path.<br>
* <b>ShowTransactionGraph</b>: visualize transaction graph.<br>
<br> All parameters of functions should be in form of a list</br>.
<br>Sample implementation of visualizations are available in <b>example_driver.py</b> </br>
 
### visuals/show_plot  
* Functions in this file implements scatter plot.

