from pathlib import Path
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

# 1. Locate outputs.csv
csv_candidates = [
    Path("outputs.csv"),
    Path(__file__).parent / "outputs.csv",
    Path(__file__).parent.parent / "outputs.csv",
]
csv_path = next((p for p in csv_candidates if p.exists()), None)

if not csv_path:
    raise FileNotFoundError("Could not find outputs.csv.")

# 2. Read CSV with pandas (skips corrupt/fragmented rows like 'ay')
df = pd.read_csv(
    csv_path,
    header=None,
    names=["time", "subsystem", "category", "message"],
    on_bad_lines="skip",
    dtype=str,
)

# Convert timestamp and drop invalid rows
df["time"] = pd.to_datetime(df["time"], format="ISO8601", errors="coerce")
df = df.dropna(subset=["time"])

# 3. Filter Telemetry with Pandas
# A. Water Temperature
temp_df = df[(df["subsystem"] == "TEMP") & (df["category"] == "ACTION")].copy()
temp_df["temp"] = pd.to_numeric(temp_df["message"], errors="coerce")
temp_df = temp_df.dropna(subset=["temp"])

# B. LDR Light Intensity & State Output
ldr_df = df[(df["subsystem"] == "LDR") & (df["category"] == "STATUS")].copy()

# Extract intensity from either 'Low Light (<val> < ...)' or 'Left: <val>; Right: <val>'
low_light = ldr_df["message"].str.extract(r"Low Light \((\d+)").astype(float)
lr_light = (
    ldr_df["message"]
    .str.extract(r"Left:\s*(\d+).*?Right:\s*(\d+)")
    .astype(float)
    .max(axis=1)
)
ldr_df["light"] = low_light[0].fillna(lr_light)

# Normalize state labels: 'Low Light', 'Stay', 'Clockwise', 'Anti-clockwise'
ldr_df["state"] = ldr_df["message"].replace(
    {r".*Low Light.*": "Low Light"}, regex=True
)
ldr_state_df = ldr_df[
    ldr_df["state"].isin(["Low Light", "Stay", "Clockwise", "Anti-clockwise"])
].copy()
ldr_light_df = ldr_df.dropna(subset=["light"]).copy()

# C. Motor Actions
motor_df = df[
    (df["subsystem"] == "MOTOR")
    & (df["category"] == "ACTION")
    & (df["message"].isin(["Stopped", "Clockwise", "Anti-clockwise"]))
].copy()

# 4. Plot 4-Panel Dashboard
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
fig.suptitle(
    "Solar Sustainability System Telemetry", fontsize=14, fontweight="bold"
)

# 1. Water Temperature
if not temp_df.empty:
    ax1.plot(
        temp_df["time"],
        temp_df["temp"],
        color="#d9534f",
        marker="o",
        markersize=3,
        linestyle="-",
        label="Water Temp (°C)",
    )
    ax1.set_ylabel("Temp (°C)")
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.legend(loc="upper left")

# 2. Max Light Intensity
if not ldr_light_df.empty:
    ax2.plot(
        ldr_light_df["time"],
        ldr_light_df["light"],
        color="#f0ad4e",
        marker="s",
        markersize=3,
        linestyle="-",
        label="Max Light Intensity",
    )
    ax2.axhline(1000, color="gray", linestyle=":", label="Threshold (1000)")
    ax2.set_ylabel("ADC Value")
    ax2.grid(True, linestyle="--", alpha=0.6)
    ax2.legend(loc="upper left")

# 3. LDR State Decisions
if not ldr_state_df.empty:
    states = ["Low Light", "Stay", "Clockwise", "Anti-clockwise"]
    state_map = {s: i for i, s in enumerate(states)}
    ldr_state_df["state_code"] = ldr_state_df["state"].map(state_map)

    ax3.step(
        ldr_state_df["time"],
        ldr_state_df["state_code"],
        where="post",
        color="#0275d8",
        marker=".",
        label="LDR State",
    )
    ax3.set_yticks(range(len(states)))
    ax3.set_yticklabels(states)
    ax3.set_ylabel("LDR State")
    ax3.grid(True, linestyle="--", alpha=0.6)
    ax3.legend(loc="upper left")

# 4. Motor Actions
if not motor_df.empty:
    motor_actions = ["Stopped", "Clockwise", "Anti-clockwise"]
    action_map = {a: i for i, a in enumerate(motor_actions)}
    motor_df["action_code"] = motor_df["message"].map(action_map)

    ax4.step(
        motor_df["time"],
        motor_df["action_code"],
        where="post",
        color="#5cb85c",
        marker="^",
        label="Motor Action",
    )
    ax4.set_yticks(range(len(motor_actions)))
    ax4.set_yticklabels(motor_actions)
    ax4.set_ylabel("Motor Action")
    ax4.grid(True, linestyle="--", alpha=0.6)
    ax4.legend(loc="upper left")
else:
    ax4.text(
        0.5,
        0.5,
        "No motor movement logged yet (system remained stopped)",
        ha="center",
        va="center",
        transform=ax4.transAxes,
    )

ax4.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
fig.autofmt_xdate()
ax4.set_xlabel("Time (HH:MM:SS)")

plt.tight_layout()
output_img = csv_path.parent / "telemetry_dashboard.png"
plt.savefig(output_img, dpi=150)
print(f"Loaded {len(df)} rows. Dashboard saved to {output_img}")
plt.show()
