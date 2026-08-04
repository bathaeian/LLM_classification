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

Model:
DeepSeek


## Classification Results

| Experiment | Classes | Test Samples | Correct | Accuracy |
|------------|---------|--------------|---------|----------|
| 1 | A vs B | 10 | 10 | 100% |
| 2 | A vs C | 10 | 10 | 100% |
| 3 | A vs D | 10 | 10 | 100% |
| 4 | B vs C | 10 | 10 | 100% |
| 5 | C vs D | 10 | 10 | 100% |


## Average Accuracy

Average classification accuracy:

100%


## Observation

The results show that the LLM can classify structured point-cloud representations directly using prompt engineering, without traditional feature extraction or deep learning preprocessing.
