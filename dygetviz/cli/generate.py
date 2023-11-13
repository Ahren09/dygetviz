"""CLI commands for embedding generation."""

import argparse
import logging
import sys
import os.path as osp

# Add parent directory to path for imports
sys.path.insert(0, osp.join(osp.dirname(__file__), '..', '..'))

from dygetviz.utils.utils_logging import configure_default_logging
from dygetviz.utils.utils_misc import project_setup
from dygetviz.utils.utils_training import get_training_args

configure_default_logging()
logger = logging.getLogger(__name__)


def generate_embeddings():
    """Main entry point for embedding generation."""
    parser = argparse.ArgumentParser(description='Generate dynamic graph embeddings')
    parser.add_argument('--dataset_name', type=str, required=True,
                        help='Name of the dataset')
    parser.add_argument('--model', type=str, default='GConvGRU',
                        help='Model to use for embedding generation')
    parser.add_argument('--device', type=str, default='cpu',
                        help='Device to use for training')
    parser.add_argument('--embedding_dim', type=int, default=128,
                        help='Embedding dimension')
    parser.add_argument('--epochs', type=int, default=50,
                        help='Number of training epochs')
    parser.add_argument('--lr', type=float, default=0.01,
                        help='Learning rate')
    parser.add_argument('--save_embeds_every', type=int, default=10,
                        help='Save embeddings every N epochs')
    
    args = parser.parse_args()
    project_setup()
    
    logger.info(f"Generating embeddings for dataset: {args.dataset_name}")
    logger.info(f"Model: {args.model}, Device: {args.device}")
    logger.info(f"Embedding dim: {args.embedding_dim}, Epochs: {args.epochs}")
    
    # Import and run the appropriate training function
    if args.dataset_name.startswith('tgbl-'):
        from dygetviz.embeddings.generators import train_dynamic_graph_embeds_tgb
        train_dynamic_graph_embeds_tgb(args)
    else:
        from dygetviz.embeddings.generators import train_dynamic_graph_embeds
        train_dynamic_graph_embeds(
            args, args.dataset_name, args.device, args.embedding_dim,
            args.epochs, args.lr, args.model, args.save_embeds_every
        )


if __name__ == '__main__':
    generate_embeddings()