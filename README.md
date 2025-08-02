<div align="center">

# DyGETViz: Dynamic Graph Embedding Trajectory Visualization

![DyGETViz Logo](static/img/DyGETViz_logo.png)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-dygetviz-blue.svg)](https://pypi.org/project/dygetviz/)
[![Documentation](https://img.shields.io/badge/Documentation-Read%20the%20Docs-blue.svg)](https://dygetviz.readthedocs.io/)
[![Tests](https://img.shields.io/badge/Tests-Passing-green.svg)](tests/)

*A comprehensive Python package for generating, analyzing, and visualizing dynamic graph embedding trajectories with an interactive web-based interface.*

</div>

## Overview

DyGETViz addresses the challenge of understanding temporal evolution in dynamic graphs by providing a unified framework for training dynamic graph neural networks (DGNNs), generating temporal embeddings, and creating interactive visualizations. The package enables researchers and practitioners to explore how nodes and communities evolve over time in various domains including social networks, biological systems, and financial networks.

## Key Contributions

- **Unified Framework**: End-to-end pipeline from data preprocessing to interactive visualization
- **Multi-Modal Visualization**: Support for both trajectory-based and snapshot-based visualizations
- **Interactive Exploration**: Real-time node selection, trajectory highlighting, and temporal analysis
- **Scalable Architecture**: Efficient handling of large-scale dynamic graphs with optimized rendering
- **Extensible Design**: Modular components supporting custom datasets and models

## Features

<div align="center">

| 🗂️ **Dataset Support** | 🤖 **Model Integration** | 🎨 **Interactive Interface** |
|------------------------|---------------------------|------------------------------|
| HistWords-CN-GNN, HistWords-EN-GNN, DGraphFin, Chickenpox, Reddit, and more | GConvGRU, TGAT, TGN, and other state-of-the-art dynamic graph models | Dash-based visualization with real-time trajectory exploration |

| 📊 **Temporal Analysis** | ⚡ **High Performance** | 📤 **Export & Sharing** |
|--------------------------|--------------------------|--------------------------|
| Node evolution tracking, community dynamics, and anomaly detection | Optimized for large-scale graphs with WebGL acceleration | Save visualizations, export trajectories, and generate reports |

</div>

## Technical Architecture

<div align="center">
<img src="static/img/dynamic_graph.png" alt="Dynamic Graph Visualization" width="600"/>
</div>

### Core Components

1. **Data Processing Pipeline**: Efficient preprocessing of temporal graph data with support for multiple formats
2. **Model Training Framework**: Unified interface for training various dynamic graph neural networks
3. **Embedding Generation**: Temporal embedding extraction with configurable dimensionality and sampling
4. **Visualization Engine**: Interactive web-based interface with real-time updates and responsive design
5. **Analysis Tools**: Built-in temporal analysis capabilities for community detection and anomaly identification

### Methodology

DyGETViz employs a three-stage pipeline:
1. **Temporal Graph Processing**: Converts raw temporal data into structured graph snapshots
2. **Dynamic Embedding Generation**: Trains DGNN models to learn temporal node representations
3. **Interactive Visualization**: Creates explorable visualizations with trajectory highlighting and temporal analysis

## Installation

<div align="center">

### 🚀 Quick Installation

```bash
git clone <repository-url>
cd dygetviz
conda create -n dygetviz python=3.11
conda activate dygetviz
pip install -r requirements.txt
pip install -e .
```

</div>

### Prerequisites

- 🐍 Python 3.8+
- 📦 Conda (recommended)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd dygetviz
   ```

2. **Create conda environment**:
   ```bash
   conda create -n dygetviz python=3.8
   conda activate dygetviz
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the package**:
   ```bash
   pip install -e .
   ```

## Quick Start

<div align="center">
<img src="static/img/simple_graph.png" alt="Simple Graph Example" width="400"/>
</div>

### 1. Generate Embeddings

```bash
# Generate embeddings for HistWords-CN-GNN dataset
python dygetviz/generate_dtdg_embeds.py --dataset_name HistWords-CN-GNN --model GConvGRU
```

### 2. Launch Visualization

```bash
# Start the interactive web interface
python dygetviz/plot_dash.py --dataset_name HistWords-CN-GNN --model GConvGRU --port 8050
```

### 3. Access the Interface

Open your browser and navigate to `http://127.0.0.1:8050`

## Usage

### Command Line Interface

```bash
# Generate embeddings
dygetviz-generate --dataset_name HistWords-CN-GNN --model GConvGRU

# Visualize embeddings
dygetviz-visualize --dataset_name HistWords-CN-GNN --model GConvGRU

# Serve dashboard
dygetviz-serve --dataset_name HistWords-CN-GNN --model GConvGRU --port 8050
```

### Python API

```python
import dygetviz
from dygetviz.data import load_data
from dygetviz.visualization import create_dash_app

# Load data
data = load_data("HistWords-CN-GNN", debug=False)

# Create visualization
app = create_dash_app(data)
app.run(debug=True, port=8050)
```

## Supported Datasets

<div align="center">

| Dataset | Description | Domain |
|---------|-------------|---------|
| 🈶 **HistWords-CN-GNN** | Chinese word embeddings evolution over time (37 age groups, 20-99 years) | NLP |
| 🈺 **HistWords-EN-GNN** | English word embeddings temporal dynamics | NLP |
| 💰 **DGraphFin** | Large-scale financial transaction network with fraud detection | Finance |
| 🦠 **Chickenpox** | Disease spread network with temporal infection patterns | Healthcare |
| 📱 **Reddit** | Social network dynamics with user interaction evolution | Social Media |
| 🏆 **TGB Datasets** | Temporal Graph Benchmark datasets for link prediction and node classification | Benchmark |

</div>

## Supported Models

<div align="center">

| Model | Architecture | Features |
|-------|--------------|----------|
| 🧠 **GConvGRU** | Graph Convolutional Recurrent Networks | Temporal graph modeling |
| 👁️ **TGAT** | Temporal Graph Attention Networks | Attention mechanisms |
| 💾 **TGN** | Temporal Graph Networks | Memory modules |
| 🔄 **DySAT** | Dynamic Self-Attention Networks | Self-attention |
| ⏰ **CTGCN** | Continuous-Time Graph Convolutional Networks | Continuous-time modeling |

</div>

## Project Structure

```
dygetviz/
├── dygetviz/
│   ├── cli/                 # Command line interface tools
│   ├── components/          # Interactive Dash components
│   ├── data/               # Data loading and preprocessing
│   ├── models/             # Dynamic graph neural network models
│   ├── embeddings/         # Embedding generation and processing
│   ├── utils/              # Utility functions and helpers
│   └── visualization/      # Visualization and dashboard modules
├── config/                 # Dataset and model configurations
├── data/                   # Dataset storage and cache
├── docs/                   # Documentation and API reference
├── examples/               # Usage examples and tutorials
├── outputs/                # Generated embeddings and results
├── saved_models/           # Trained model checkpoints
└── tests/                  # Comprehensive test suite
```

## Configuration

Configuration files are stored in the `config/` directory and define dataset-specific parameters:

- `HistWords-CN-GNN.json`: Chinese word embeddings with temporal evolution parameters
- `HistWords-EN-GNN.json`: English word embeddings configuration
- `DGraphFin.json`: Financial network with fraud detection settings
- `Chickenpox.json`: Disease spread network parameters
- `Reddit.json`: Social network dynamics configuration
- `TGBL.json`: Temporal Graph Benchmark link prediction settings

## Troubleshooting

### Common Issues

1. **"ID not found in Layout" errors**: 
   - Ensure all required components are properly imported
   - Check for missing callback dependencies

2. **Background nodes not showing**:
   - Verify data loading is successful
   - Check trace conversion and rendering modes

3. **Port already in use**:
   - Use a different port: `--port 8051`
   - Kill existing processes: `lsof -ti:8050 | xargs kill`

### Debug Mode

Enable debug mode for detailed logging:

```bash
python dygetviz/plot_dash.py --dataset_name HistWords-CN-GNN --model GConvGRU --debug
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citation

If you use DyGETViz in your research, please cite:

```bibtex

```

## Contact

For questions, bug reports, and feature requests, please open an issue on GitHub. For collaboration opportunities, please contact the development team.

---

<div align="center">

### 🌟 Star us on GitHub!

[![GitHub stars](https://img.shields.io/github/stars/dygetviz/dygetviz?style=social)](https://github.com/Ahren09/dygetviz)
[![GitHub forks](https://img.shields.io/github/forks/dygetviz/dygetviz?style=social)](https://github.com/Ahren09/dygetviz)
[![GitHub issues](https://img.shields.io/github/issues/dygetviz/dygetviz)](https://github.com/Ahren09/dygetviz/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/dygetviz/dygetviz)](https://github.com/Ahren09/dygetviz/pulls)

</div>
