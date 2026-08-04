# Structure-Preserving Classification using LLMs

## Dataset

Dataset:
PMF_OMNIGLOT

Representation:
Point cloud extracted from grayscale images.

Each sample is represented as a set of 2D coordinates (x, y).

Maximum points per sample:
80

Classification method:
Prompt-based classification using LLM.

---

# DeepSeek Results

## Model

DeepSeek

## Classification Results

| Experiment | Classes | Test Samples | Correct | Accuracy |
| ---------- | ------- | ------------ | ------- | -------- |
| 1          | A vs B  | 10           | 10      | 100%     |
| 2          | A vs C  | 10           | 10      | 100%     |
| 3          | A vs D  | 10           | 10      | 100%     |
| 4          | B vs C  | 10           | 10      | 100%     |
| 5          | C vs D  | 10           | 10      | 100%     |

## Average Accuracy

Average classification accuracy:

100%

---

# Grok Results

## Model

Grok

## Classification Results

| Experiment | Classes   | Test Samples | Correct | Accuracy |
| ---------- | --------- | ------------ | ------- | -------- |
| 1          | A vs B    | 20           | 20      | 100%     |
| 2          | A-B-C     | 40           | 30      | 75%      |
| 3          | A-B-C-D   | 40           | 32      | 80%      |
| 4          | A-B-C-D-E | 50           | 27      | 54%      |

## Average Accuracy

Average classification accuracy:

77.25%

---

## Observation

The results demonstrate that LLMs can perform classification directly on structured point-cloud representations using prompt engineering.

The models are able to capture geometric and structural patterns from coordinate-based representations without traditional feature extraction, handcrafted descriptors, or deep learning preprocessing.

The accuracy decreases as the number of classes increases, showing that classification becomes more challenging with higher structural complexity.
