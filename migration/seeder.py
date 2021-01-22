import pandas as pd

df = pd.read_csv('input/program.csv', delimiter=";",
                 encoding="ISO-8859-1", keep_default_na=False)

print(df.to_json(orient="table"))
