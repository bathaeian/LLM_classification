#iran-italy flags
import csv
import random
import numpy as np
from sklearn.datasets import make_classification
import pandas as pd
from sklearn.model_selection import KFold
'''
flag iran:  ggggg
            wwwww
            rrrrr
flag italy: ggwwrr
#           ggwwrr
'''
#generate point
random.seed(23)
def point_ir():
    x = random.uniform(0, 2)
    y = random.uniform(0, 1)
    c='r'
    if y>0.66 :
       c='g'
    elif y>0.33:
        c='w'
    point=[x, y, c]
    return point
def point_it():
    x = random.uniform(0, 2)
    y = random.uniform(0, 1)
    c='r'
    if x<0.7 :
        c='g'
    elif x<1.4:
        c='w'
    point=[x, y, c]
    return point
# Generate dataset
rows=[]
n_samples=10  #total points
n_features=10
n_points=3
n_classes=2   #binary classification
col_labels = ['x1', 'y1', 'c1','x2','y2','c2','x3','y3','c3','class']
# random_state for reproducibility
for sample in range(n_samples):
    row=[]
    for _ in range(n_points):
        row.extend(point_ir())
    row.append('a')
    rows.append(row)
    row=[]
    for _ in range(n_points):
        row.extend(point_it())
    row.append('b')
    rows.append(row)

df = pd.DataFrame(rows, columns=col_labels)
# Save to CSV
output_file = "ir_it_data.csv"
df.to_csv(output_file, index=False)

print(f"Dataset saved to {output_file}")