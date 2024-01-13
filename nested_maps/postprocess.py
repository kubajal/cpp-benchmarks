import pandas as pd
import matplotlib.pyplot as plt
import math

NAME="out100"

df = pd.read_csv(f"{NAME}.csv")

def parse_time(text: str):
    [minutes_text, seconds_text] = text.split("m")
    minutes = int(minutes_text)
    seconds = float(seconds_text.split("s")[0])
    return minutes * 60 + seconds

df["real_time"] = df["real_time"].map(parse_time)
df["user_time"] = df["user_time"].map(parse_time)
df["sys_time"] = df["sys_time"].map(parse_time)

# Select values that fit into the chart
# df = df[(df["type"] == 1) | (df["type"] == 2)]

# Calculate Q1 and Q3
q1 = df.groupby('type_name')['real_time'].quantile(0.25)
q3 = df.groupby('type_name')['real_time'].quantile(0.75)

# Calculate the Interquartile Range (IQR)
iqr = q3 - q1

# Define bounds for outliers
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

# Filter df based on these bounds
filtered_df = df[df.apply(lambda x: lower_bound[x['type_name']] <= x['real_time'] <= upper_bound[x['type_name']], axis=1)]
# filtered_df = df[df["depth"] < 6]

grouped_data = filtered_df.groupby(["type_name", "depth"])["real_time"].mean().reset_index()
# grouped_data["real_time"] = grouped_data["real_time"].map(lambda x: math.log10(x))

# Plotting
plt.figure(figsize=(10, 6))
for t in grouped_data["type_name"].unique():
    subset = grouped_data[grouped_data["type_name"] == t]
    plt.plot(subset["depth"], subset["real_time"], marker='o', label=f"{t}")

plt.xlabel("Nesting Depth")
plt.ylabel("Mean Real Time [s]")
plt.title("Mean Real Time by Type and Nesting Depth")
plt.legend()
plt.grid(True)
plt.savefig(f"{NAME}.png")
