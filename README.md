# DyGETViz

Our framework is DyGETViz, which stands for **Dynamic Graph Embedding Trajectories Visualization**.

<img src="assets/img/illustration1.png" width="80%" style="display: block; margin: 0 auto;" />


## Installation

### Install the Dependencies

```bash
conda install scikit-learn pandas numpy matplotlib plotly
conda install -c conda-forge dash dash-daq dash-bootstrap-components biopython
pip install umap
```


Please refer to the homepage of [PyTorch](https://pytorch.org/get-started/locally/), [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/en/latest/install/installation.html), and [PyTorch Geometric Temporal](https://pytorch-geometric-temporal.readthedocs.io/en/latest/notes/installation.html) to install these 3 packages, respectively. 


### Download the data

- Download all the data from [Google Drive](https://drive.google.com/drive/folders/1Yctajha2NoF8y_JyE5hoX_47vwH0I4e2?usp=drive_link)
- Put both `data/` and `outputs/` under the root directory of this repo.



## Getting Started

### Procedures of Generating the Visualization

- Step 1: Discrete-Time Dynamic Graph (DTDG) embedding training
  - We use the [GConvGRU](https://pytorch-geometric-temporal.readthedocs.io/en/latest/modules/root.html) model from [PyTorch Geometric Temporal](https://pytorch-geometric-temporal.readthedocs.io/en/latest/notes/installation.html) to train embeddings of all datasets
  - We extended the dataloader so that we can use a wide variety of data input formats. The original dataloader only used static input at each snapshot.
  - Note: This part is not included in the code yet. For now, we directly provide the embeddings.

- **Output**: DTDG embeddings of shape (T, N, D)

  - T: The number of timestamps / snapshots
  - N: The number of nodes
  - D: Embedding dimension


Step 2: Embedding Trajectories Generation

- **Input**: DTDG embeddings of shape (T, N, D)


- **Output**: JSON file that store the embedding trajectory for [Dash](https://dash.plotly.com/)


Step 3: Visualizing in a Dash app interactively using the JSON file

- Users should be able to incrementally add node trajectories  / all nodes under a certain category (e.g., normal users v.s. anomalous users) to the visualization


- highlighted_nodes: List of nodes to be highlighted in the visualization. We need to specify these nodes because we only show the names of a small number of nodes in the plotly visualization. Otherwise, the generated plot will be too messy. 


- **plot_dtdg.py**: Script for generating the visualization
- 

Generate the visualization using the command:

```bash
python dygetviz/plot_dtdg.py --dataset_name <DATASET_NAME> --model GConvGRU
```

Currently, `DATASET_NAME` can be selected from one of: `Ant`, `Chickenpox`, `DGraphFin`, `Reddit`



```bash
python dygetviz/plot_dtdg.py --dataset_name Chickenpox --model GConvGRU

python dygetviz/plot_dash.py --dataset_name Chickenpox --model GConvGRU
```

## Terminology

- `DG`: Dynamic Graphs, which can be categorized into DTDG and CTDG
- `DTDG`: Discrete-Time Dynamic Graphs
- `CTDG`: Discrete-Time Dynamic Graphs
- `Embedding Trajectories`: Please refer to the [JODIE paper (KDD2019)]() for more details

## Datasets

We provide the following dataset to be viewd in our visualization tool:

- `Ant`: The ant movement dataset from [Tracking individuals shows spatial fidelity is a key regulator of ant social organization (Science 2013)](https://www.science.org/doi/10.1126/science.1234316)
- `Chickenpox`: The chickenpox dataset from the paper [Chickenpox Cases in Hungary: a Benchmark Dataset for Spatiotemporal Signal Processing with Graph Neural Networks](https://arxiv.org/abs/2102.08100)
- `HistWords`: The historical word co-occurrence dataset from [Diachronic Word Embeddings Reveal Statistical Laws of Semantic Change](https://arxiv.org/abs/1605.09096) ([GitHub](https://github.com/williamleif/histwords)) ([Website](https://nlp.stanford.edu/projects/histwords/))


## Explanation of Each Data File

- `node2idx`: A dictionary that maps node names to node indices (usually starting from 0 to #nodes-1).
- `embeds_<DATASET_NAME>.npy`: The node embeddings generated by DyGET. The shape of the embeddings is `#nodes x #time_steps x #embedding_dim`.


## Note



- The Reddit dataset is a bit special because it is the only dataset that describes a bipartite graph. The first 60 snapshots are for each of the 60 snapshots. The last snapshot is for the background nodes. The shape of the embeddings is `` 

## Acknowledgments

We thank members of the CLAWS Lab and SRI International for their feedback and support.


