import pandas as pd, json

# when you read it, tell pandas to json‑decode those columns
df = pd.read_csv(
    "logs/alice_experiments.csv",
    converters={
        "params": json.loads,
        "metrics": json.loads,
        "extra": json.loads,
    }
)

# now ‘params’ and ‘metrics’ are real dicts in each cell,
# so you can normalize them into their own columns:
params_df  = pd.json_normalize(df["params"])
metrics_df = pd.json_normalize(df["metrics"])

# stitch them back onto your main df
df = pd.concat(
    [df.drop(["params","metrics"], axis=1), params_df, metrics_df],
    axis=1,
)



# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')