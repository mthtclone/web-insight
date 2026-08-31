# WebSight - AI-Powered UX Analysis Tool

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-orange)
![Computer Vision](https://img.shields.io/badge/Computer%20Vision-AI-purple)
![DeepGaze III](https://img.shields.io/badge/Model-DeepGaze%20III-red)

## Overview

WebSight is an AI-powered UX analysis tool that evaluates website designs by predicting human visual attention and generating data-driven UX insights.

The system combines **computer vision**, **deep learning**, and **web analysis** to understand how users are likely to view a webpage and whether important elements receive sufficient attention.

Instead of relying only on manual UX reviews, WebSight automatically analyzes website screenshots, identifies important UI elements, calculates attention scores, and provides recommendations for improving visual hierarchy and user experience.

---

## Features

- Website screenshot capture using Playwright
- Human visual attention prediction using DeepGaze III
- Saliency map generation
- Visual attention heatmap overlay
- DOM element attention analysis
- CTA detection
- UX metric generation:
  - CTA visibility
  - Headline prominence
  - Visual hierarchy
  - Overall UX score
- Automated UX recommendations

---

## How It Works

## How It Works

```
Website URL
v
Capture Website Screenshot
v
DeepGaze III Attention Prediction
v
Generate Saliency Map
v
Analyze UI Elements
v
Calculate UX Metrics
v
Generate Recommendations
v
Display Results
```

## Technology Stack

### Backend
- Python
- FastAPI
- Playwright

### Machine Learning
- PyTorch
- DeepGaze III
- Computer Vision
- OpenCV

### Frontend
- JavaScript
- HTML
- CSS

---

## Machine Learning Approach

WebSight uses **DeepGaze III** to predict visual attention.

The model combines:

- Visual features extracted from the webpage screenshot
- Human center bias
- Attention prediction layers

The output is a saliency map representing areas where users are most likely to focus.

The saliency information is then mapped to webpage elements to measure how effectively the design guides user attention.

---