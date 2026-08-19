# DeepGaze Integration Documentation

## Overview

This document explains the setup and integration process for the DeepGaze visual attention model used in the UX Analyzer project.

DeepGaze is responsible for predicting visual attention on webpage screenshots. The goal is:

```
Website Screenshot
        ↓
DeepGaze III Model
        ↓
Saliency Map
        ↓
Heatmap Visualization
```

The saliency map represents regions of the webpage that are likely to attract human attention.

---

# 1. DeepGaze Dependency Installation

The project already had the required computer vision and deep learning dependencies installed:

```bash
torch
torchvision
opencv-python
pillow
numpy
```

PyTorch was installed with CUDA support to enable GPU acceleration:

```
PyTorch: 2.13.0+cu126
TorchVision: 0.28.0+cu126
CUDA: Available
GPU: NVIDIA GeForce RTX 3050 Laptop GPU
```

Additional dependencies required by the DeepGaze PyTorch implementation were installed:

```bash
pip install timm scipy matplotlib
```

Explanation:

- `timm`
  - Provides modern pretrained computer vision model components.
  - Used by some vision feature extraction pipelines.

- `scipy`
  - Provides scientific computing utilities used in image processing and model operations.

- `matplotlib`
  - Used for visualizing saliency maps during development.

---

# 2. Installing DeepGaze Model

## Repository

The PyTorch implementation was cloned from:

```
https://github.com/matthias-k/DeepGaze
```

The repository contains several DeepGaze models:

```
DeepGazeI
DeepGazeIIE
DeepGazeIII
DeepGazeMSDB
```

---

## Why DeepGaze III?

DeepGaze III was selected because it is the latest model architecture in the repository and is designed for predicting human visual attention using deep learning.

Compared to older saliency approaches, DeepGaze III models:

- deep visual features
- human fixation behavior
- scanpath information

This makes it suitable for webpage UX analysis because webpages contain complex visual layouts where users do not look at every region equally.

---

## Loading the Model

The model is loaded using:

```python
from deepgaze_pytorch.deepgaze3 import DeepGazeIII


model = DeepGazeIII(
    pretrained=True
)
```

When initialized, the model automatically downloads pretrained weights:

- DenseNet201 feature extractor weights
- DeepGazeIII trained parameters

The weights are cached locally by PyTorch.

The model is moved to GPU:

```python
model.to(device)
```

and switched to inference mode:

```python
model.eval()
```

---

# 3. DeepGaze III Model Input and Prediction

During investigation of the source code, we found that the model forward function is:

```python
def forward(
    self,
    x,
    centerbias,
    x_hist=None,
    y_hist=None,
    durations=None
):
```

The required inputs are:

| Input | Description |
|---|---|
| `x` | Input image tensor (webpage screenshot) |
| `centerbias` | Human viewing tendency bias toward image regions |
| `x_hist` | Previous fixation x-coordinates |
| `y_hist` | Previous fixation y-coordinates |
| `durations` | Previous fixation durations |

For the first version of this project, we only use:

```python
model(
    image,
    centerbias
)
```

because we are predicting general webpage attention rather than modeling a specific user's eye movement history.

---

# 4. How DeepGaze Produces Attention Predictions

DeepGaze III combines multiple components:

```
Webpage Screenshot
        |
        ↓
Visual Feature Extraction
        |
        ↓
Deep Neural Network
        |
        +
Human Center Bias
        |
        ↓
Final Saliency Prediction
```

## Visual Features

The model extracts visual information from the screenshot:

Examples:

- colors
- edges
- shapes
- objects
- layout patterns

These features represent what is visually present on the webpage.

---

## Human Center Bias

Humans naturally tend to look closer to the center of an image.

DeepGaze incorporates this prior knowledge using a center bias map.

The model combines:

```
Visual Information
        +
Expected Human Viewing Bias
```

to better approximate real human attention.

---

## Final Saliency Prediction

The output is a saliency map:

```
Low attention  →  High attention
```

Each pixel receives an attention probability.

Example:

```
Screenshot:

+----------------+
| Logo           |
|                |
| Main CTA       |
|                |
| Footer         |
+----------------+


Saliency Map:

+----------------+
| Low            |
|                |
| High           |
|                |
| Low            |
+----------------+
```

This saliency map will later be converted into:

- OpenCV heatmaps
- screenshot overlays
- webpage element attention scores

---

