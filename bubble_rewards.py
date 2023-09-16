import pandas as pd
import numpy as np
import plotly.express as px
import os


def convert_value(value, format_type, default=0):
    if format_type == 'float':
        try:
            return float(value)
        except ValueError:
            return default
    elif format_type == 'int':
        try:
            return int(value)
        except ValueError:
            return default
    elif format_type == 'float_mb':
        try:
            return float(value.replace("MB", "").strip())
        except ValueError:
            return default
    elif format_type == 'float_percent':
        try:
            return float(value.replace("%", "").strip())
        except ValueError:
            return default
    return value

def enhanced_extract_data(filename):
    all_data = []
    # Process the single filename directly
    with open(filename, "r") as file:
        lines = file.readlines()
        formats = {
            "Memory used": "float_mb",
            "Records": "int",
            "Disk usage": "float_mb",
            "CPU usage": "float_percent",
            "File descriptors": "int",
            "Rewards balance": "float",
            "Number": "int"
        }
        data = []
        idx = 0
        while idx < len(lines):
            if "Global (UTC) Timestamp:" in lines[idx]:
                timestamp = lines[idx].split(": ", 1)[1].strip()
                entry_data = {"Global (UTC) Timestamp": timestamp}
                idx += 1
                while idx < len(lines) and "------------------------------------------" not in lines[idx]:
                    if ": " in lines[idx]:
                        key, raw_value = lines[idx].split(": ", 1)
                        if key in formats:
                            value = convert_value(raw_value, formats[key])
                        else:
                            value = raw_value.strip()
                        entry_data[key] = value
                    idx += 1
                data.append(entry_data)
            idx += 1
        all_data.extend(data)
    df = pd.DataFrame(all_data)
    df = df.dropna(subset=["Global (UTC) Timestamp"])
    df["Timestamp"] = pd.to_datetime(df["Global (UTC) Timestamp"], errors='coerce')
    df = df.dropna(subset=["Timestamp"]).groupby("Node").last().reset_index()
    return df

def logarithmic_bubble_visualize(df):
    df["x"] = np.random.rand(len(df))
    df["y"] = np.random.rand(len(df))
    df["log_rewards"] = 2 * np.log(df["Rewards balance"] + 1)
    
    fig = px.scatter(df, x="x", y="y", size="log_rewards", color="PID", hover_name="Node",
                     hover_data=["Number", "Node", "PID", "Rewards balance"], 
                     labels={"log_rewards": "Log-scaled Rewards Balance"},
                     size_max=100)
    
    fig.update_traces(hovertemplate="Number: %{customdata[0]}<br>Node: %{customdata[1]}<br>PID: %{customdata[2]}<br>Rewards balance: %{customdata[3]}<extra></extra>")
    
    fig.update_layout(
        hovermode='closest',
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        margin=dict(t=42, b=42, l=42, r=42, pad=2),
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(showgrid=False, visible=False)
    )
    
    output_html_path = os.path.join(os.path.expanduser("~"), ".local/share/safe/tools/Rewards_plotting/rewards_bubbles.html")
    fig.write_html(output_html_path)
    return output_html_path

file_path = os.path.join(os.path.expanduser("~"), ".local/share/safe/tools/Rewards_plotting/resources.log")
df = enhanced_extract_data(file_path)
log_bubble_plot_path = logarithmic_bubble_visualize(df)

