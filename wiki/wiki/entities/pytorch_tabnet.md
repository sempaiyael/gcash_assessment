---
title: pytorch-tabnet
type: entity
entity_type: tool
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [library, pytorch, tabular, tabnet]
---

# pytorch-tabnet

Official TabNet implementation for PyTorch.

## Installation

```bash
pip install pytorch-tabnet
```

## Usage

```python
from pytorch_tabnet.tab_model import TabNetClassifier

clf = TabNetClassifier()
clf.fit(X_train, y_train, eval_set=[(X_valid, y_valid)])
predictions = clf.predict(X_test)
```

## Key Features

- Classification and regression
- Unsupervised pre-training
- Feature importance via attention masks
- GPU accelerated

## Related

- [[concepts/TabNet]]
- [[entities/TabNet_Paper]]