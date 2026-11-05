import pandas as pd

df = pd.read_csv("temp_log_proper.txt")

# Converts to date-time object from string
df["time"] = pd.to_datetime("2026-11-05 " + df["time"])

# Shift the timeline so the first log starts precisely at 12:45:00
true_start = pd.to_datetime("2026-11-05 12:45:00")  # reference object
time_offset = (
    true_start - df["time"].iloc[0]
)  # calculate diff b/w reference and 1st time entry
df["time"] = df["time"] + time_offset  # add diff to all rows

# Calculate the step size to get roughly num_points points total
num_points = 100
step = max(1, len(df) // num_points)

# Slice every N-th row to keep real data points without averaging
df_subset = df.iloc[::step].reset_index(drop=True)

# df.info()
# df_subset.info()

df.to_csv("unfiltered_temp.csv")
df_subset.to_csv("filtered_temp.csv")

# print(df_subset.head())

# import matplotlib.dates as mdates
# import matplotlib.pyplot as plt
#
# # Assuming df_subset has your shifted 'time' and 'temperature' columns
# fig, ax = plt.subplots(figsize=(10, 6))
#
# ax.plot(
#     # df_subset["time"], df_subset["temperature"], marker="o", linestyle="-", markersize=3
#     df["time"],
#     df["temperature"],
#     marker="o",
#     linestyle="-",
#     markersize=3,
# )
#
# # Configure the x-axis to display only Hour:Minute
# ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
#
# # Optional: Auto-format tick spacing so they don't crowd each other
# fig.autofmt_xdate()
#
# # string = "Filtered Rise in Temperature against Time"
# string = "Unfiltered Rise in Temperature against Time"
# ax.set_title(string)
# ax.set_xlabel("Time (HH:MM)")
# ax.set_ylabel("Temperature (°C)")
#
# # plt.legend()
# # plt.tight_layout()
# plt.show()
