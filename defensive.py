from warcraft_logs_api import WarcraftLogsAPI

api_client = WarcraftLogsAPI()

defensive_cast_data = api_client.query_defensive_casts()

cast_counts = {}
for event in defensive_cast_data["data"]["reportData"]["report"]["events"]["data"]:
    source_id = event["sourceID"]
    ability_id = event["abilityGameID"]

    # Initialize nested dictionary for sourceID if not exists
    if source_id not in cast_counts:
        cast_counts[source_id] = {}

    # Count the ability casts
    if ability_id not in cast_counts[source_id]:
        cast_counts[source_id][ability_id] = 0
    cast_counts[source_id][ability_id] += 1

print(cast_counts)