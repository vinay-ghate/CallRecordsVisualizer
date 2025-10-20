import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def top_contacts_chart(df: pd.DataFrame, top_n: int = 10):
    top_contacts = df["Number"].value_counts().nlargest(top_n).reset_index()
    top_contacts.columns = ["Number", "Call Count"]
    fig = px.bar(
        top_contacts, x="Number", y="Call Count", text="Call Count",
        title=f"Top {top_n} Most Contacted Numbers"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_tickangle=-45, xaxis_type="category", height=600,
                      margin=dict(t=150, b=150), xaxis=dict(automargin=True), yaxis=dict(automargin=True))
    return fig

def top_usage_chart(df: pd.DataFrame, top_n: int = 10):
    top_usage = df.groupby("Number")["Used Usage"].sum().nlargest(top_n).reset_index()
    fig = px.bar(
        top_usage, x="Number", y="Used Usage", text="Used Usage",
        title=f"Top {top_n} Numbers by Total Used Usage (Seconds)"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis_tickangle=-45, xaxis_type="category", height=600,
                      margin=dict(t=150, b=150), xaxis=dict(automargin=True), yaxis=dict(automargin=True))
    return fig

def usage_distribution_pie(df: pd.DataFrame):
    usage_sum = df[["Billed Usage", "Free Usage", "Chargeable Usage"]].sum()
    fig = px.pie(usage_sum, values=usage_sum.values, names=usage_sum.index, 
                 title="Usage Distribution (Billed / Free / Chargeable)", hole=0.3)
    return fig

def calls_over_time(df: pd.DataFrame):
    df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], format="%d-%b-%y %H:%M:%S")
    calls_per_day = df.groupby(df["Datetime"].dt.date).size().reset_index(name="Call Count")
    fig = px.line(calls_per_day, x="Datetime", y="Call Count", markers=True, 
                  title="Number of Calls Over Time")
    return fig

def total_call_time_over_time(df):
    """
    Plot total call duration over time (per day) based on 'Used Usage'.
    """
    df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], format="%d-%b-%y %H:%M:%S")
    df["Call Duration (min)"] = df["Used Usage"] / 60  # Convert seconds to minutes
    daily_duration = df.groupby(df["Datetime"].dt.date)["Call Duration (min)"].sum().reset_index()
    fig = px.bar(
        daily_duration,
        x="Datetime",
        y="Call Duration (min)",
        text="Call Duration (min)",
        title="Total Call Duration per Day (minutes)"
    )
    fig.update_traces(texttemplate='%{text:.1f}', textposition="outside")
    fig.update_layout(
        xaxis_tickangle=-45,
        height=600,
        margin=dict(t=150, b=150),
        xaxis=dict(automargin=True),
        yaxis=dict(automargin=True)
    )
    return fig
def number_call_summary(df, number: str):
    """
    Generate call summary and plots for a specific number.

    Args:
        df (pd.DataFrame): Call records dataframe
        number (str): Phone number to filter
    Returns:
        dict: Summary stats and Plotly figure
    """
    filtered = df[df["Number"] == number].copy()
    if filtered.empty:
        return {
            "summary": {"Total Calls": 0, "Total Duration (min)": 0, "Average Duration (min)": 0},
            "fig": None
        }

    filtered["Datetime"] = pd.to_datetime(filtered["Date"] + " " + filtered["Time"], format="%d-%b-%y %H:%M:%S")
    filtered["Call Duration (min)"] = filtered["Used Usage"] / 60

    daily_summary = filtered.groupby(filtered["Datetime"].dt.date).agg(
        Calls=("Number", "count"),
        Duration=("Call Duration (min)", "sum")
    ).reset_index()

    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=daily_summary["Datetime"],
        y=daily_summary["Duration"],
        name="Total Call Duration (min)",
        text=daily_summary["Duration"],
        textposition="outside"
    ))
    fig.add_trace(go.Scatter(
        x=daily_summary["Datetime"],
        y=daily_summary["Calls"],
        name="Number of Calls",
        yaxis="y2",
        mode="lines+markers"
    ))

    fig.update_layout(
        title=f"Call Duration and Count for {number}",
        xaxis_title="Date",
        yaxis=dict(title="Duration (min)"),
        yaxis2=dict(title="Number of Calls", overlaying="y", side="right"),
        xaxis_tickangle=-45,
        height=600,
        margin=dict(t=150, b=150)
    )

    summary_stats = {
        "Total Calls": filtered.shape[0],
        "Total Duration (min)": filtered["Call Duration (min)"].sum(),
        "Average Duration (min)": filtered["Call Duration (min)"].mean()
    }

    return {"summary": summary_stats, "fig": fig}