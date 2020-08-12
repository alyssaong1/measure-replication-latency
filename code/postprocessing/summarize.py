"""
This is a python script to summarize the replication results
"""

import sys
import pandas as pd
from tabulate import tabulate
import argparse

parser = argparse.ArgumentParser(description='Run the postprocessing script for data consistency testing, to generate the results summary.')

# Add the arguments to the parser
parser.add_argument("-n", "--name", required=True,
   help="Name of experiment")
parser.add_argument("-f", "--folder", required=True,
   help="Relative folder path where experiment results are stored in e.g. logs/raw")
args = vars(parser.parse_args())

filename = args["name"]
filepath = args["folder"]

# Enter your logged columns below, in order
columns = ["log_time", "run_id", "updated_at", "read_time", "read_user_id"]

try:
    df = pd.read_csv(f"{filepath}/{filename}.csv", names=columns, sep=',',
                     engine='python', error_bad_lines=False, index_col=False).dropna()
except:
    print("Unable to read log file. Please enter a valid run id.")
    sys.exit()


print(df.to_string())

print('==============================')
print('Obtained replication latency')
print('==============================')

df.loc[:, 'read_time'] = pd.to_datetime(df.loc[:, 'read_time'])
df.loc[:, 'updated_at'] = pd.to_datetime(df.loc[:, 'updated_at'])

# Convert the datetime difference to miliseconds
df["replication_latency"] = (
    (df["read_time"] - df["updated_at"]).dt.total_seconds() * 10**3)

df.to_csv(f'logs/processed/{filename}.csv', header=False, index=False)

print('==============================')
print('Summary')
print('==============================')

print('\n Average replication latency times, grouped by user:')

df_results = df.groupby('read_user_id')[
    ["read_user_id", "replication_latency"]].agg(['count', 'mean']).reset_index().round(2)

print(tabulate(df_results, headers=[
      "User ID", "Number of operations", "Mean replication latency (ms)"], tablefmt="pretty"))

print('Mean replication latency (ms) across all users:')
print(df["replication_latency"].mean().round(2))
