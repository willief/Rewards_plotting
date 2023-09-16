import pandas as pd
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

def enhanced_extract_data(filenames):
    all_data = []
    
    # Iterate over each file and extract data
    for filename in filenames:
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
                        entry_data["Number"],
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

        all_data.extend(data)

    df = pd.DataFrame(all_data, columns=["Timestamp", "Node", "Number", "PID", "Memory", "Records", 
                                        "Disk usage", "CPU usage", "File descriptors", "Rewards balance"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format='%a %b %d %H:%M:%S %Z %Y', errors='coerce')
    if df["Timestamp"].dt.tz is None:
        df["Timestamp"] = df["Timestamp"].dt.tz_localize('UTC')
    return df

# Visualization
custom_hovertemplate = "%{customdata[0]}<br>" + \
                       "Records: %{customdata[1]}<br>" + \
                       "Disk usage: %{customdata[2]}MB<br>" + \
                       "Memory used: %{customdata[3]:.2f}MB<br>" + \
                       "CPU usage: %{customdata[4]:.2f}%<br>" + \
                       "File descriptors: %{customdata[5]}<br>"
                       
                       
def visualize(df):
    fig = px.line(df, x="Timestamp", y="Memory", color="PID", line_group="PID",
                  custom_data=["Number", "Records", "Disk usage", "Memory", "CPU usage", 
                               "File descriptors", "Rewards balance"],
                  title="Memory Usage Over Time", 
                  labels={"Memory": "Memory Usage (MB)"})

    fig.update_layout(
        hovermode='y unified',
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        margin=dict(t=42, b=42, l=42, r=42, pad=2),
        xaxis=dict(showgrid=True, gridcolor='#f5f5f5', gridwidth=0.05),
        yaxis=dict(showgrid=True, gridcolor='#f5f5f5', gridwidth=0.05)
    )

    output_html_path = os.path.join(os.path.expanduser("~"), ".local/share/safe/tools/rewards_plotting/memory.html")
    fig.write_html(output_html_path)
    return output_html_path

file_path = os.path.join(os.path.expanduser("~"), ".local/share/safe/tools/rewards_plotting/resources.log")
df = enhanced_extract_data([file_path])
visualize(df)
