import pandas as pd
import plotly.express as px

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
    with open(filename, "r") as file:
        lines = file.readlines()

    formats = {
        "Memory used": "float_mb",
        "Records": "int",
        "Disk usage": "float_mb",
        "CPU usage": "float_percent",
        "File descriptors": "int",
        "Rewards balance": "float"
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
            
            required_keys = ["Global (UTC) Timestamp", "Node", "PID", "Memory used", "Records", 
                             "Disk usage", "CPU usage", "File descriptors", "Rewards balance"]
            if all(k in entry_data for k in required_keys):
                data.append([
                    timestamp, 
                    entry_data["Node"], 
                    entry_data["PID"], 
                    entry_data["Memory used"], 
                    entry_data["Records"],
                    entry_data["Disk usage"], 
                    entry_data["CPU usage"], 
                    entry_data["File descriptors"], 
                    entry_data["Rewards balance"]
                ])
        else:
            idx += 1

    df = pd.DataFrame(data, columns=["Timestamp", "Node", "PID", "Memory", "Records", 
                                    "Disk usage", "CPU usage", "File descriptors", "Rewards balance"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format='%a %b %d %H:%M:%S %Z %Y', errors='coerce')
    if df["Timestamp"].dt.tz is None:
        df["Timestamp"] = df["Timestamp"].dt.tz_localize('UTC')
    return df


# Visualization
custom_hovertemplate = "<br>" + \
                       "Records: %{customdata[0]}<br>" + \
                       "Disk usage: %{customdata[1]}MB<br>" + \
                       "Memory used: %{customdata[2]:.2f}MB<br>" + \
                       "CPU usage: %{customdata[3]:.2f}%<br>" + \
                       "File descriptors: %{customdata[4]}<br>" + \
                       "Rewards balance: %{customdata[5]:.9f}<br>"

def visualize(df):
    fig = px.line(df, x="Timestamp", y="Rewards balance", color="PID", line_group="PID",
                  custom_data=["Records", "Disk usage", "Memory", "CPU usage", 
                               "File descriptors", "Rewards balance"],
                  title="Rewards Balance Over Time for Each Node", 
                  labels={"Rewards balance": "Rewards Balance"})

    for trace in fig.data:
        trace.hovertemplate = custom_hovertemplate

    fig.update_layout(
        hovermode='y unified',
        paper_bgcolor='darkgrey',
        plot_bgcolor='#dee0df',
        margin=dict(t=42, b=42, l=42, r=42, pad=2),
        xaxis=dict(showgrid=True, gridcolor='lightgrey', gridwidth=0.1),
        yaxis=dict(showgrid=True, gridcolor='lightgrey', gridwidth=0.1)
    )
    # Modify as needed.
    output_html_path = "/home/{user}/rewards_balance_plot.html"
    fig.write_html(output_html_path)

# Modify as needed.
df = enhanced_extract_data("/home/{user}/resources.log")
visualize(df)


