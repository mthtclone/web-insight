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

| Input        | Description                                      |
| ------------ | ------------------------------------------------ |
| `x`          | Input image tensor (webpage screenshot)          |
| `centerbias` | Human viewing tendency bias toward image regions |
| `x_hist`     | Previous fixation x-coordinates                  |
| `y_hist`     | Previous fixation y-coordinates                  |
| `durations`  | Previous fixation durations                      |

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

# 5. DeepGaze III Inference Pipeline

Pipeline:

```
Website Screenshot
        |
        v
Image Preprocessing
        |
        v
DeepGaze III
        |
        v
Raw Saliency Map
        |
        v
Heatmap Visualization
```

---

## 5.1. Screenshot Preprocessing

The screenshot generated by Playwright is converted into a PyTorch tensor.

Input:

```
page.png
```

Processing:

```
PNG
 |
Pillow
 |
RGB Image
 |
Torch Tensor
```

The final tensor format:

```
(batch, channels, height, width)
```

Example:

```
torch.Size([1, 3, 900, 1440])
```

Meaning:

| Dimension | Meaning      |
| --------- | ------------ |
| 1         | Batch size   |
| 3         | RGB channels |
| 900       | Image height |
| 1440      | Image width  |

The tensor is moved to the GPU:

```python
image_tensor.to(device)
```

---

## 5.2. Center Bias Generation

DeepGaze III does not only use visual information.

Human attention has a natural tendency to focus near the center of an image.

Therefore, the model requires:

```python
centerbias
```

The generated tensor format:

```
(batch, height, width)
```

Example:

```
torch.Size([1, 900, 1440])
```

The center bias represents the probability distribution of where humans are naturally likely to look.

---

## 5.3. DeepGaze III Input Requirements

During source code investigation, the model forward function was found:

```python
def forward(
    self,
    x,
    centerbias,
    x_hist=None,
    y_hist=None,
    durations=None
)
```

Required inputs:

| Input      | Description                     |
| ---------- | ------------------------------- |
| x          | Screenshot tensor               |
| centerbias | Human viewing bias map          |
| x_hist     | Previous fixation x coordinates |
| y_hist     | Previous fixation y coordinates |
| durations  | Fixation durations              |

---

## 5.4. Scanpath History Handling

DeepGaze III is a scanpath model.

Unlike simple saliency models, it predicts attention while considering previous human fixation locations.

The model expects four previous fixations:

```python
included_fixations=[
    -1,
    -2,
    -3,
    -4
]
```

However, our application does not receive real eye-tracking data.

Therefore, we initialize the fixation history using four center fixations.

Example:

```python
x_hist = [
    width/2,
    width/2,
    width/2,
    width/2
]

y_hist = [
    height/2,
    height/2,
    height/2,
    height/2
]
```

This provides a neutral starting point for static webpage analysis.

---

## 5.5. Running Inference

The model is loaded:

```python
model = DeepGazeIII(
    pretrained=True
)

model.to(device)
model.eval()
```

Inference:

```python
with torch.no_grad():

    saliency = model(
        image,
        centerbias,
        x_hist=x_hist,
        y_hist=y_hist
    )
```

---

## 5.6. Model Output

The model returns:

```
torch.Size([1, 1, 900, 1440])
```

The dimensions represent:

| Dimension | Meaning          |
| --------- | ---------------- |
| 1         | Batch            |
| 1         | Saliency channel |
| 900       | Height           |
| 1440      | Width            |

This is the raw saliency prediction.

The output is not yet a visual image.

Next processing steps:

```
Raw saliency tensor
        |
        v
Normalize values
        |
        v
Convert to NumPy
        |
        v
OpenCV colormap
        |
        v
Heatmap image
```

---
