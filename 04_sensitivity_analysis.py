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

#### Create a new metrics:

dm["kg emissions per 100g protein"] = (10*dm["Greenhouse emissions in kg per kg of food"])/dm["protein g / 100g"]
dm["kg emissions per 100g protein"] = dm["kg emissions per 100g protein"].round(decimals = 2)

dm["m^2 land use per 100g protein"] = (10*dm["Land use, m^2 per kg"])/dm["protein g / 100g"]
dm["m^2 land use per 100g protein"] = dm["m^2 land use per 100g protein"].round(decimals = 2)

dm["Freshwater use (L)  use per 100g protein"] = (10*dm["Freshwater withdrawals, L per kg of food"])/dm["protein g / 100g"]
dm["Freshwater use (L)  use per 100g protein"] = dm["Freshwater use (L)  use per 100g protein"].round(decimals = 2)

dm["kg emissions per 100 kcal"] = (10*dm["Greenhouse emissions in kg per kg of food"])/dm["calories kcal / 100g"]
dm["kg emissions per 100 kcal"] = dm["kg emissions per 100 kcal"].round(decimals = 2)

dm["m^2 land use per 100 kcal"] = (10*dm["Land use, m^2 per kg"])/dm["calories kcal / 100g"]
dm["m^2 land use per 100 kcal"] = dm["m^2 land use per 100 kcal"].round(decimals = 2)

dm["Freshwater use (L)  use per 100 kcal"] = (10*dm["Freshwater withdrawals, L per kg of food"])/dm["calories kcal / 100g"]
dm["Freshwater use (L)  use per 100 kcal"] = dm["Freshwater use (L)  use per 100 kcal"].round(decimals = 2)


# Environmental metrics
metrics = ["GHG emissions", "Land use", "Freshwater use"]

# Percentage reduction from replacing poultry with tofu
# Negative value = environmental impact increased
equal_weight = [68.0, 71.2, 77.4]
equal_protein = [42.3, 48.1, 59.4]
equal_calories = [-2.4, 9.8, 29.0]

x = np.arange(len(metrics))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))

bars_weight = ax.bar(x - width, equal_weight, width, label="Equal weight")

bars_protein = ax.bar(x, equal_protein, width, label="Equal protein")

bars_calories = ax.bar(x + width, equal_calories, width, label="Equal calories")

ax.set_ylabel("Reduction in environmental impact (%)")
ax.set_xlabel("Environmental metric")
ax.set_title("Sensitivity of Poultry → Tofu Substitution to Comparison Method")

ax.set_xticks(x)
ax.set_xticklabels(metrics)

# Include negative space so the +2.4% GHG increase is visible
ax.set_ylim(-10, 90)

# Zero line distinguishes reductions from increases
ax.axhline(0, linewidth=0.8)

ax.legend()

# Percentage labels
ax.bar_label(bars_weight, fmt="%.1f%%", padding=3)
ax.bar_label(bars_protein, fmt="%.1f%%", padding=3)
ax.bar_label(bars_calories, fmt="%.1f%%", padding=3)

plt.tight_layout()
plt.savefig("figures/sensitivity_analysis.png", dpi=300, bbox_inches="tight")
plt.show()
