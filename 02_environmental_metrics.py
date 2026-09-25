import pandas as pd

environment = pd.read_csv("data/environment.csv")
nutrition = pd.read_csv("data/nutrition.csv")
#### Merge the datasets
df = pd.DataFrame(environment)
df = df.replace(',','', regex=True)
df1 = pd.DataFrame(nutrition)
df[["Freshwater withdrawals, L per kg of food"]] = df[["Freshwater withdrawals, L per kg of food"]].astype(int)

#Create rankings for each of the three metrics
dm = pd.merge(df, df1, on = "entity")
gasrank = df["Greenhouse emissions in kg per kg of food"].rank(method='average', na_option='keep', ascending=True)
df["gasrank"] = gasrank

landrank = df["Land use, m^2 per kg"].rank(method='average', na_option='keep', ascending=True)
df["landrank"] = landrank

waterrank = df["Freshwater withdrawals, L per kg of food"].rank(method='average', na_option='keep', ascending=True)
df["waterrank"] = waterrank

'''
print(df[["entity", "Greenhouse emissions in kg per kg of food", "gasrank"]].to_string(index=False))
print(df[["entity", "Land use, m^2 per kg", "landrank"]].to_string(index=False))
print(df[["entity", "Freshwater withdrawals, L per kg of food", "waterrank"]].to_string(index=False))
'''

ranked_table = df[["entity", "gasrank", "landrank", "waterrank"]]


##Calculate the Spearman Rank coefficients
land_water = ranked_table[["landrank", "waterrank"]]
coeff_land_water = land_water.corr(method="spearman", numeric_only=False).loc["landrank", "waterrank"]
coeff_land_water = round(coeff_land_water,3)
print("The Spearman's coefficient between land and water usage is ", coeff_land_water)

land_ghg = ranked_table[["landrank", "gasrank"]]
coeff_land_gas = land_ghg.corr(method="spearman", numeric_only=False).loc["landrank", "gasrank"]
coeff_land_gas = round(coeff_land_gas,3)
print("The Spearman's coefficient between land usage and greenhouse gas emissions is ", coeff_land_gas)

water_ghg = ranked_table[["waterrank", "gasrank"]]
coeff_water_gas = water_ghg.corr(method="spearman", numeric_only=False).loc["waterrank", "gasrank"]
coeff_water_gas = round(coeff_water_gas,3)
print("The Spearman's coefficient between water usage and greenhouse gas emissions is ", coeff_water_gas)

##Calculate the standard deviation and range
#print(ranked_table.std(axis=1, numeric_only=True))
ranked_table["standard deviation"] = round(ranked_table.std(axis=1, numeric_only=True, ddof=0),3)

ranked_table["range"] = ranked_table[["gasrank", "waterrank", "landrank"]].max(axis=1, numeric_only = True) - ranked_table[["gasrank", "waterrank", "landrank"]].min(axis=1, numeric_only = True)

ranked_table = ranked_table.sort_values(by = "standard deviation", ascending = False)
print(ranked_table[["entity", "standard deviation"]])
ranked_table = ranked_table.sort_values(by = "range", ascending = False)
print(ranked_table[["entity", "range"]])
