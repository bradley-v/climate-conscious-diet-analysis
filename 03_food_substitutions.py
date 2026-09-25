import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

environment = pd.read_csv("data/environment.csv")
nutrition = pd.read_csv("data/nutrition.csv")
#### Merge the datasets
df = pd.DataFrame(environment)
df = df.replace(',','', regex=True)
df1 = pd.DataFrame(nutrition)
df[["Freshwater withdrawals, L per kg of food"]] = df[["Freshwater withdrawals, L per kg of food"]].astype(int)

dm = pd.merge(df, df1, on = "entity")
#print(dm.to_string(index = False))

#### Create a new metric: kg emissions per 100g protein

dm["kg emissions per 100g protein"] = (10*dm["Greenhouse emissions in kg per kg of food"])/dm["protein g / 100g"]
dm["kg emissions per 100g protein"] = dm["kg emissions per 100g protein"].round(decimals = 2)

dm["m^2 land use per 100g protein"] = (10*dm["Land use, m^2 per kg"])/dm["protein g / 100g"]
dm["m^2 land use per 100g protein"] = dm["m^2 land use per 100g protein"].round(decimals = 2)

dm["Freshwater use (L)  use per 100g protein"] = (10*dm["Freshwater withdrawals, L per kg of food"])/dm["protein g / 100g"]
dm["Freshwater use (L)  use per 100g protein"] = dm["Freshwater use (L)  use per 100g protein"].round(decimals = 2)


# Substitution scenarios
substitutions = ["Beef → Poultry", "Beef → Tofu", "Poultry → Tofu"]

# Percentage reductions in environmental impact from manual calculation
ghg_reduction = [90.1, 94.3, 42.3]
land_reduction = [96.3, 98.1, 48.1]
water_reduction = [54.5, 81.5, 59.36]

# Numerical positions of the three substitution groups
x = np.arange(len(substitutions))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))

# Offset each set of bars so they appear alongside one another
bars_ghg = ax.bar(x - width, ghg_reduction, width, label="GHG emissions")
bars_land = ax.bar(x, land_reduction, width, label="Land use")
bars_water = ax.bar(x + width, water_reduction, width, label="Freshwater withdrawals")

# Labels and formatting
ax.set_ylabel("Reduction in environmental impact (%)")
ax.set_xlabel("Dietary substitution")
ax.set_title("Environmental Impact of Equal-Protein Food Substitutions")
ax.set_xticks(x)
ax.set_xticklabels(substitutions)
ax.set_ylim(0, 105)
ax.legend()

# Put the percentage above each bar
ax.bar_label(bars_ghg, fmt="%.1f%%", padding=3)
ax.bar_label(bars_land, fmt="%.1f%%", padding=3)
ax.bar_label(bars_water, fmt="%.1f%%", padding=3)

plt.tight_layout()

# Save before showing

plt.savefig("figures/substitution_reductions.png", dpi=300, bbox_inches="tight")
plt.show()
