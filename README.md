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

## Changelog

### Extended Findings and Recommendations Rules

### Findings
Added CTA attention analysis:
- Detects strong, moderate, or weak CTA visibility.
- Identifies whether the CTA receives enough user attention.

Added headline prominence analysis:
- Evaluates whether the main headline successfully attracts attention.
- Detects when the headline is competing with other elements.

Added visual hierarchy analysis:
- Measures whether important and secondary elements have clear attention differences.
- Detects weak or unclear hierarchy.

Added overall attention distribution analysis:
- Evaluates whether the webpage guides users effectively.
- Detects poor attention patterns.

Added attention competition analysis:
- Detects when too many elements receive high attention.
- Identifies potential user distraction.

Added CTA priority analysis:
- Checks whether the CTA is the strongest attention target.
- Detects when users may focus on unintended elements.

Added low-attention element analysis:
- Identifies elements that receive very little attention.
- Detects potentially overlooked content.

### Recommendations

Added CTA improvement recommendations:
- Suggests increasing size, contrast, spacing, or placement when CTA attention is low.
- Suggests strengthening CTA emphasis when visibility is moderate.

Added headline improvement recommendations:
- Suggests improving typography, contrast, and positioning.
- Recommends reducing distractions around important messaging.

Added visual hierarchy recommendations:
- Suggests improving size, spacing, contrast, and prioritization between elements.
- Recommends reducing competition between important and secondary content.

Added overall UX improvement recommendations:
- Suggests restructuring layouts with poor attention distribution.
- Encourages stronger user attention flow.

Added attention competition recommendations:
- Suggests simplifying layouts when too many elements compete for attention.
- Suggests creating stronger visual anchors when no element stands out.

Added CTA prioritization recommendations:
- Detects when CTA is not the main visual focus.
Suggests redesigning CTA emphasis and placement.
- Added balanced UX feedback:
Provides positive feedback when attention distribution is effective.