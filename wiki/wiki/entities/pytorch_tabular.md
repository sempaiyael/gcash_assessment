---
title: pytorch-tabular
type: entity
entity_type: tool
created: 2026-10-19
updated: 2026-10-19
sources: []
tags: [library, pytorch, tabular, ft-transformer]
---

# pytorch-tabular

Unified library for tabular deep learning models in PyTorch.

## Installation

```bash
pip install pytorch-tabular
```

## Supported Models

- FT-Transformer
- TabNet
- NODE
- TabTransformer
- And more

## Usage

```python
from pytorch_tabular import TabularModel
from pytorch_tabular.models import FTTransformerConfig

model = TabularModel(
    data_config=data_config,
    model_config=model_config,
    trainer_config=trainer_config,
)
model.fit(train=train_df, validation=val_df)
predictions = model.predict(test_df)
```

## Related

- [[concepts/FT_Transformer]]
- [[entities/FT_Transformer_Paper]]