import pandas as pd
import matplotlib.pyplot as plt
import math

df = pd.read_csv("out.csv")

def parse_time(text: str):
    [minutes_text, seconds_text] = text.split("m")
    minutes = int(minutes_text)
    seconds = float(seconds_text)
    return minutes * 60 + seconds

df["real_time"] = df["real_time"].map(parse_time)
df["user_time"] = df["user_time"].map(parse_time)
df["sys_time"] = df["sys_time"].map(parse_time)

# Select values that fit into the chart
# df = df[(df["type"] == 1) | (df["type"] == 2)]
df = df[df["depth"] < 6]

grouped_data = df.groupby(["type_name", "depth"])["real_time"].mean().reset_index()
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
plt.savefig("postprocess.png")
