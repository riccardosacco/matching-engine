import pandas as pd
from datetime import datetime

fileinput = "input/program.csv"
fileoutput = "data.json"

df = pd.read_csv(fileinput, delimiter=";", encoding="ISO-8859-1", keep_default_na=False)


df.rename(
    columns={
        "date_time": "lastUpdate",
        "uuid": "UUID",
        "Title/episode_title": "title",
        "EPGgenre": "genre",
        "isEpisode": "entitySubtype",
        "providerId": "providerID",
        "providerType": "providerName",
        "production year": "productionYear",
        "director orig": "director",
        "master_uuid": "masterUUID",
        "alternative title": "alt_title",
        "source(scheule/enrichment)": "type",
        "episode_number": "episodeNumber",
        "season_number": "seasonNumber",
        "titleId": "titleProviderId",
        "title_id provider": "titleProviderName",
    },
    inplace=True,
)

df["lastUpdate"] = df["lastUpdate"].apply(
    lambda x: datetime.strptime(x, "%d/%m/%Y %H:%M")
)
df["alt_title"] = df["alt_title"].apply(lambda x: x.split("[[ALT]]")[1:])
df["director"] = df["director"].apply(lambda x: x.split(",") if x != "" else "")
df["entitySubtype"] = df["entitySubtype"].apply(
    lambda x: "episode" if x == "t" else "programme"
)
df["type"] = df["type"].apply(
    lambda x: "SCHED" if x in ["IBMS", "SCHED", "FINALIZED"] else "ENRICH"
)

df.to_json(fileoutput, orient="records")
