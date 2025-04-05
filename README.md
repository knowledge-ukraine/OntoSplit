# OntoSplit
This repository contains the dataset, experimental scripts, and results for the study on ontology partitioning and SPARQL query optimization. The research focuses on improving the execution time of complex SPARQL queries by splitting large RDF/XML ontologies and leveraging parallel query execution in Apache Jena Fuseki.

### 📂 Contents:

 - 📂 [./data](data) - stores all ontology (or RDF/XML structures) files (original and partitioned), as well as any sample datasets or additional resources needed for experimentation and demonstrations.
 - 📊 [./benchmarking-data](benchmarking-data) – experiments data
 - 📊 [./benchmarking-data/benchmark.xlsx](benchmarking-data/benchmark.xlsx) – final tests results data: tables, charts
 - 📜 [./benchmarking-data/sparql-queries](benchmarking-data/sparql-queries) – test SPARQL queries categorized by execution time (fast -1, medium -2, slow - 3)
 - 📜 [./benchmarking-data/results-time](benchmarking-data/results-time) - contains **JSON files** capturing the execution time for SPARQL queries of different categories (fast -1, medium -2, slow - 3) across various ontology partition configurations (1–15 parts)
 - 🔧 [./benchmarking-data/scripts](benchmarking-data/scripts) - Python scripts for benchmarking execution and results calculation
 - 🔧 [./scripts/ontology-creation](scripts/ontology-creation) - Python scripts for ontology creation (PDF to JSON; JSON to XML/RDF ontology with different splitting options)
 - 📕 [./parsed-pdfs-json](parsed-pdfs-json) - Stores files related to PDFs from the [Dataset](#-dataset), including **original PDFs** (optional) and **JSON outputs** resulting from parsing scripts
 - 📖 ./docs/ – methodology, findings, and implementation details - TODO 

### 🚀 Sponsor this project

Please support @malakhovks. Despite the Wartime in Ukraine, R&D in the field of Digital Health and Ontology Engineering are being resumed:

Via credit card: [https://send.monobank.ua/jar/5ad56oNAcD](https://send.monobank.ua/jar/5ad56oNAcD)

Public Address to Receive USDT (BEP20): 0x1128A7b84728123dd4F55176c378754Dd396A674

<!-- ![alt text](https://github.com/knowledge-ukraine/OntoSplit/blob/master/usdt-bsc.jpg?raw=true) -->

<p align="center" width="100%">
<img align="center" src="https://github.com/knowledge-ukraine/OntoSplit/blob/master/usdt-bsc.jpg?raw=true" width=20% height=20%/>
</p>

Pay me via Trust Wallet: https://link.trustwallet.com/send?asset=c20000714_t0x55d398326f99059fF775485246999027B3197955&address=0x1128A7b84728123dd4F55176c378754Dd396A674

### 🔍 Key Topics:

 - SPARQL query optimization
 - Ontology partitioning (sharding)
 - Parallel query execution
 - Apache Jena Fuseki performance benchmarking
 - Semantic Web & RDF processing

### 🚀 Future Work:
The repository will be updated with further optimizations, including machine learning-based query performance prediction and dynamic ontology partitioning.

Contributions and discussions are welcome!

#### 📕 Dataset

EBSCO articles dataset (domain knowledge: rehabilitation medicine) + JSON of every article

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8308214.svg)](https://doi.org/10.5281/zenodo.8308214)

```bash
wget -O ./ebsco-rehabilitation-dataset.zip https://cdn.e-rehab.pp.ua/u/ebsco-rehabilitation-dataset.zip
```

### 💳 Funding

<!-- ![alt text](https://github.com/knowledge-ukraine/OntoSplit/blob/master/logo_nrfu_eng.png?raw=true) -->

<p align="center" width="100%">
<img align="center" src="https://github.com/knowledge-ukraine/OntoSplit/blob/master/logo_nrfu_eng.png?raw=true" width=25% height=25%/>
</p>

This study would not have been possible without the financial support of the [National Research Foundation of Ukraine](https://nrfu.org.ua/) (Open Funder Registry: 10.13039/100018227). Our work was funded by Grant contract:

- [Development of the cloud-based platform for patient-centered telerehabilitation of oncology patients with mathematical-related modeling, application ID: 2021.01/0136](https://doi.org/10.5195/ijt.2024.6686).

### 📖 How to Cite / BibTex

If you use this repository in your research, please cite it as follows:

🔹 Citation format for article:

```bibtex
@article{palagin_2025_ontosplit,
  title={A Method for Enhancing the Efficiency of RDF/XML-Structure Processing in the Apache Jena Semantic Web Framework},
  author={Palagin, O. V. and Petrenko, M. G. and Kaverinskiy, V. V. and Malakhov, K.S.},
  journal={Cybernetics and Systems Analysis},
  volume={61},
  number={3},
  DOI={},
  year={2025}
}
```

🔹 Citation format for repository:

```bibtex
@misc{OntoSplit,
  author = {Kyrylo Malakhov and Vladislav Kaverinskiy},
  title = {OntoSplit: Ontology Partitioning and SPARQL Query Optimization},
  year = {2025},
  howpublished = {GitHub Repository},
  url = {https://github.com/knowledge-ukraine/OntoSplit}
}
```

