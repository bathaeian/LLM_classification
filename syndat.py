import csv
import random
from datetime import datetime, timedelta

random.seed(42)

inventory = {
    "A": 120,
    "B": 80,
    "C": 50
}

rows = []
current_time = datetime(2026, 1, 1)

for day in range(30):
    for product in inventory:
        daily_orders = random.randint(0, 12)

        for _ in range(daily_orders):
            qty = random.randint(1, 5)
            before = inventory[product]

            if inventory[product] >= qty:
                inventory[product] -= qty
                status = "fulfilled"
            else:
                status = "backorder"

            rows.append({
                "time": current_time.isoformat(),
                "product": product,
                "qty": qty,
                "stock_before": before,
                "stock_after": inventory[product],
                "status": status
            })

        if inventory[product] < 20:
            restock = random.randint(30, 80)
            inventory[product] += restock
            rows.append({
                "time": current_time.isoformat(),
                "product": product,
                "qty": restock,
                "stock_before": inventory[product] - restock,
                "stock_after": inventory[product],
                "status": "restock"
            })

    current_time += timedelta(days=1)

with open("warehouse_sim.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("Saved warehouse_sim.csv")