from skimage import io, color, filters,feature
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
def build1dataset(traindir):
    max=2
    rows=[]
    labels=[]
    for i in range(1,21):
        image = io.imread(traindir+str(i)+'.png')
        # Create binary mask
        mask = image<127
        # Apply mask
        masked = image*mask#gray * mask
        # Edge detection
        ed2= feature.canny(masked)
        y, x = np.nonzero(ed2)                   # coordinates of the points
        points = np.column_stack([x, y])
        pf=points.flatten()
        row=pf.tolist()
        if max<points.size:
            max=points.size
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
    output_file = "train"+trainset+".csv"
    df.to_csv(output_file, index=False)
    print(f"Dataset saved to {output_file}")

for ts in range(0,20):
    trainset=str(ts)
    directory='.\\PMF_OMNIGLOT-main\\PMF_OMNIGLOT-main\\data\\train\\'
    traindir=directory+trainset+"\\"
    build1dataset(traindir)
