import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
environment = pd.read_csv("data/environment.csv")
nutrition = pd.read_csv("data/nutrition.csv")

env = pd.DataFrame(environment)
env = env.replace(',','', regex=True)
env[["Freshwater withdrawals, L per kg of food"]] = env[["Freshwater withdrawals, L per kg of food"]].astype(int)
nut = pd.DataFrame(nutrition)

#merge datasets
foods = pd.merge(env, nut, on = "entity")

#create new metrics
foods["kg emissions per 100g protein"] = (10*foods["Greenhouse emissions in kg per kg of food"])/foods["protein g / 100g"]
foods["kg emissions per 100g protein"] = foods["kg emissions per 100g protein"].round(decimals = 2)

# Find The Best Protein Source
    #1. Filter to sources >20g /100g protein
    #2. Sort them by kg emissions per 100g protein
    #3. Print their entity and emissions/protein ratio
high_protein = foods[foods["protein g / 100g"] > 10]
protein_sorted = high_protein.sort_values(by = "kg emissions per 100g protein", ascending = True)
protein_sorted2 = high_protein.sort_values(by = "kg emissions per 100g protein", ascending = False)

#bar chart for food types and kg emissions per 100g protein.
plt.barh(protein_sorted2["entity"] , protein_sorted2["kg emissions per 100g protein"])
plt.title("Greenhouse gas emissions per 100g protein")
plt.xlabel("Greenhouse emissions (kg) per 100g protein")

plt.savefig("figures/protein_efficiency.png", dpi=300, bbox_inches="tight")
plt.show()