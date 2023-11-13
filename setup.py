"""Setup script for DygETViz package."""

from setuptools import setup, find_packages
import os.path as osp

# Read the README file for long description
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "Dynamic Graph Embedding Trajectory Visualization package"

# Read requirements from requirements.txt
def read_requirements():
    requirements = []
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    requirements.append(line)
    except FileNotFoundError:
        # Fallback requirements list
        requirements = [
            "biopython",
            "dash", 
            "dash-ag-grid",
            "dash-bootstrap-components",
            "dash-dangerously-set-inner-html",
            "Markdown",
            "matplotlib",
            "numba", 
            "numpy",
            "openTSNE",
            "pandas",
            "plotly",
            "requests",
            "scikit-learn",
            "seaborn",
            "tgb",
            "torch",
            "torch-geometric",
            "torch-geometric-temporal",
            "torch-scatter",
            "torchaudio",
            "torchvision",
            "tqdm",
            "umap-learn"
        ]
    return requirements

setup(
    name="dygetviz",
    version="0.1.0",
    author="DygETViz Team",
    author_email="dygetviz@example.com",
    description="Dynamic Graph Embedding Trajectory Visualization",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/dygetviz/dygetviz",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
            "myst-parser>=0.15",
        ],
    },
    entry_points={
        "console_scripts": [
            "dygetviz-generate=dygetviz.cli.generate:generate_embeddings",
            "dygetviz-visualize=dygetviz.cli.visualize:visualize_embeddings", 
            "dygetviz-serve=dygetviz.cli.serve:serve_dashboard",
        ],
    },
    include_package_data=True,
    package_data={
        "dygetviz": [
            "assets/*",
            "static/*",
            "config/*",
        ],
    },
    zip_safe=False,
)