import pandas as pd
from sqlalchemy import create_engine

temp_db = create_engine("sqlite:///salaries.db")

user_df = pd.read_csv("Datacsv/RegisteredUsers.csv")
equipment_df = pd.read_csv("Datacsv/Equipments.csv")
userequipment_df = pd.read_csv("Datacsv/RegisteredEquipments.csv")
location_df = pd.read_csv("Datacsv/Locations.csv")
# search_transactions_df = pd.read_csv("data/search_transactions.csv")
# monitoring_events_df = pd.read_csv("data/monitoring_events.csv")
# monitoring_event_types_df = pd.read_csv("data/monitoring_event_types.csv")


# user_df.to_sql(name="users", con=temp_db, if_exists="replace")
# customers_df.to_sql(name="customers", con=temp_db, if_exists="replace")
# events_df.to_sql(name="events", con=temp_db, if_exists="replace")
# filters_df.to_sql(name="filter", con=temp_db, if_exists="replace")
# search_transactions_df.to_sql(
#     name="search_transactions", con=temp_db, if_exists="replace")
# monitoring_event_types_df.to_sql(
#     name="monitoring_event_types", con=temp_db, if_exists="replace")
# monitoring_events_df.to_sql(
#     name="monitoring_events", con=temp_db, if_exists="replace")

# Create a dictionary to associate table names with DataFrames

dataframes = {
    'users': user_df,
    'catalog.equipments': equipment_df,
    'userequipments': userequipment_df,
    'dbo.installationlocation': location_df,
    # 'search_transactions': search_transactions_df,
    # "monitoring_events": monitoring_events_df,
    # "monitoring_event_types": monitoring_event_types_df
}
