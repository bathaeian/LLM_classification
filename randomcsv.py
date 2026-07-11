import csv
import random
random.seed(70)
percen= 100
filename= "warehouse_sim.csv"
newfile="warehouse_rand2.csv"
rows = []

with open(filename, newline='') as csvfile:
   csvreader = csv.DictReader(csvfile)
   for r in csvreader:
        if(random.randint(1, percen)==1):
            rows.append(r)

with open(newfile, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("Saved "+newfile)