import pandas as pd

# List of Showcases
showcases = [
    "Gar Saxon - Viceroy of Mandalore", 
    "Qi'ra - I Alone Survived", 
    "Finn - This is a Rescue", 
    "Rey - More Than a Scavenger", 
    "Hondo Ohnaka - That's Good Business", 
    "Jabba the Hutt - His High Exaltedness", 
    "Boba Fett - Daimyo",
    "Hunter - Outcast Sergeant", 
    "Bossk - Hunting His Prey", 
    "Kylo Ren - Rash and Deadly", 
    "Bo-Katan Kryze - Princess in Exile", 
    "Han Solo - Worth the Risk", 
    "Cad Bane - He Who Needs No Introduction", 
    "Doctor Aphra - Rapacious Archaeologist",
    "Fennec Shand - Honoring the Deal", 
    "Lando Calrissian - With Impeccable Taste"
]

# Read Market Data CSV
market_value_df = pd.read_csv('market_values.csv')
print(market_value_df.count)

#Cleaning up Market data to remove bases and add the showcase printing option
showcase_filter = market_value_df['Product Name'].isin(showcases)
base_filter = market_value_df['Product Name'].str.contains("//")
market_value_df = market_value_df[~showcase_filter]
market_value_df = market_value_df[~base_filter]


print(market_value_df.count)
