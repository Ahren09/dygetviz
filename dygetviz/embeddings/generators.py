"""Embedding generation functions moved from main scripts."""

import json
import logging
import os
import os.path as osp
import sys

import numpy as np

try:
    import torch
    from torch import nn
    from torch.optim.lr_scheduler import StepLR
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None
    nn = None
    StepLR = None

try:
    from tqdm import trange
except ImportError:
    def trange(*args, **kwargs):
        return range(args[0] if args else 0)

# Add parent directory to path for imports
sys.path.insert(0, osp.join(osp.dirname(__file__), '..', '..'))

from dygetviz.data.dataloader import load_data_dtdg
from dygetviz.models.recurrentgcn import RecurrentGCN
from dygetviz.utils.utils_misc import project_setup
from dygetviz.utils.utils_training import get_training_args
from dygetviz.utils.utils_logging import configure_default_logging

configure_default_logging()
logger = logging.getLogger(__name__)


def train_dynamic_graph_embeds(args, dataset_name, device, embedding_dim: int,
                               epochs: int, lr: float, model_name: str,
                               save_every: int,
                               step_size: int = 50, use_pyg=True):
    """Train dynamic graph embeddings using the torch-geometric-temporal package.

    Args:
        args: Command line arguments
        dataset_name (str): Name of the dataset
        device (str): Device for embedding training
        embedding_dim (int): Dimension of the embedding
        epochs (int): Number of epochs to train
        lr (float): Learning rate
        model_name (str): Name of the model to use
        save_every (int): How many epochs to perform evaluation and save the embeddings
        step_size (int): Step size for learning rate scheduler
        use_pyg (bool): Whether to use the datasets in pytorch-geometric-temporal package

    Returns:
        None
    """
    logger.info(f"Training embeddings for {dataset_name}")
    logger.info(f"Device: {device}, Embedding dim: {embedding_dim}")
    logger.info(f"Epochs: {epochs}, Learning rate: {lr}")
    
    # Load the data
    dataset = load_data_dtdg(dataset_name, use_pyg=use_pyg, device=device)
    
    # Initialize model
    model = RecurrentGCN(
        model_name, 
        node_features=dataset.num_node_features,
        hidden_dim=embedding_dim,
        device=device
    ).to(device)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = StepLR(optimizer, step_size=step_size, gamma=0.5)
    
    model.train()
    
    # Training loop
    for epoch in trange(epochs, desc="Training"):
        total_loss = 0
        
        for time, snapshot in enumerate(dataset):
            y_hat = model(snapshot.x, snapshot.edge_index)
            loss = torch.mean((y_hat - snapshot.y) ** 2)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            total_loss += loss.item()
        
        scheduler.step()
        
        if epoch % save_every == 0:
            logger.info(f"Epoch {epoch}, Loss: {total_loss:.4f}")
            # Save embeddings if needed
            save_embeddings(model, dataset, dataset_name, epoch, embedding_dim)
    
    logger.info("Training completed")


def train_dynamic_graph_embeds_tgb(args):
    """Train embeddings using TGB datasets.
    
    Args:
        args: Command line arguments containing dataset and training parameters
    """
    logger.info(f"Training TGB embeddings for {args.dataset}")
    
    # Import TGB-specific training logic
    from dygetviz.models.tgb_modules import TGBTrainer
    
    trainer = TGBTrainer(args)
    trainer.train()


def save_embeddings(model, dataset, dataset_name, epoch, embedding_dim):
    """Save model embeddings to file.
    
    Args:
        model: Trained model
        dataset: Dataset object
        dataset_name (str): Name of the dataset
        epoch (int): Current epoch
        embedding_dim (int): Embedding dimension
    """
    embeddings_dir = osp.join("data", dataset_name)
    os.makedirs(embeddings_dir, exist_ok=True)
    
    # Extract embeddings
    model.eval()
    with torch.no_grad():
        embeddings = []
        for snapshot in dataset:
            emb = model.get_embeddings(snapshot.x, snapshot.edge_index)
            embeddings.append(emb.cpu().numpy())
    
    # Save embeddings
    embeddings_array = np.array(embeddings)
    filename = f"embeds_{dataset_name}_epoch{epoch}_dim{embedding_dim}.npy"
    filepath = osp.join(embeddings_dir, filename)
    np.save(filepath, embeddings_array)
    
    logger.info(f"Saved embeddings to {filepath}")
    model.train()