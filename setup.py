import pandas as pd

# Create DataFrames to associate with respective csv files
user_df = pd.read_csv("Datacsv/Users.csv")
userequipments_df = pd.read_csv("Datacsv/UserEquipments.csv")
equipment_df = pd.read_csv("Datacsv/Equipments.csv")
location_df = pd.read_csv("Datacsv/Locations.csv")

# Create a dictionary to associate table names with DataFrames
dataframes = {
    'dbo.Users': user_df,
    'dbo.UserEquipments': userequipments_df,
    'catalog.equipments': equipment_df,
    'dbo.installationlocation': location_df,
}
