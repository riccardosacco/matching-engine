import pandas as pd
from datetime import datetime

fileinput = "input/program.csv"
fileoutput = "data.json"

# 1. Read CSV file and create DataFrame
df = pd.read_csv(fileinput, delimiter=";", keep_default_na=False)

# 2. Rename columns
df.rename(
    columns={
        "date_time": "lastUpdate",
        "uuid": "UUID",
        "program_title": "title",
        "epg_genre": "genre",
        "is_episode": "entitySubtype",
        "providerid": "providerID",
        "provider_type": "providerName",
        "production_year": "productionYear",
        "directori_orig": "director",
        "master_uuid": "masterUUID",
        "alternative_titles": "alt_title",
        "source": "type",
        "episode_number": "episodeNumber",
        "season_number": "seasonNumber",
        "titleid": "titleProviderId",
        "titleid_provider": "titleProviderName",
        "series_uuid": "seriesUUID",
        "series_provider_id": "seriesProviderId",
    },
    inplace=True,
)

# 3. Parse data with functions
df["lastUpdate"] = df["lastUpdate"].apply(
    lambda x: datetime.strptime(x, "%d/%m/%Y %H:%M")
)
df["alt_title"] = df["alt_title"].apply(lambda x: list(set(x.split("[[ALT]]")[1:])))
df["director"] = df["director"].apply(lambda x: x.split(",") if x != "" else "")
df["entitySubtype"] = df["entitySubtype"].apply(
    lambda x: "episode" if x == "t" else "programme"
)
df["type"] = df["type"].apply(
    lambda x: "SCHED" if x in ["IBMS", "SCHED", "FINALIZED"] else "ENRICH"
)
# 4. Export to JSON with orient = "records"
df.to_json(fileoutput, orient="records")
