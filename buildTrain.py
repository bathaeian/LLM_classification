import numpy as np
from PIL import Image
import skimage as ski
import os
import csv
import pandas as pd

trainset='0'
directory='.\\PMF_OMNIGLOT-main\\PMF_OMNIGLOT-main\\data\\train\\'
traindir=directory+trainset+"\\"
file_list = os.listdir(traindir)
image_file_list = [file for file in file_list if file.endswith(".png")]
print(image_file_list)
max=2
rows=[]
labels=[]
for i in range(1,21):
    img = np.array(Image.open(traindir+str(i)+'.png').convert('L'))   # read image as grayscale, uint8, 0 / 255
    mask = img < 127                 # binarize
    edges = ski.filters.sobel(mask)
    coords = ski.feature.corner_peaks(ski.feature.corner_harris(edges), min_distance=5, threshold_rel=0.02)
    print(coords.shape)
    cf=coords.flatten()
    row=cf.tolist()
    if max<coords.size:
        max=coords.size
    rows.append(row)
    if i%2==0:
        labels.append(chr(ord('@')+i-1))
    else:
        labels.append(chr(ord('@')+i))
col_labels=[]
for i in range(1,int(max/2)+1):
    col_labels.append('x'+str(i))
    col_labels.append('y'+str(i))
df = pd.DataFrame(rows, columns=col_labels)
df['class'] = labels
# Save to CSV
output_file = trainset+".csv"
df.to_csv(output_file, index=False)
print(f"Dataset saved to {output_file}")

