import json

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Set page config
st.set_page_config(page_title="NerdType | Simple Dashboard", layout="wide")

# Choose a color theme (uncomment one of these themes)

# Default Blue Theme
theme = {
    "primary": "#7aa2f7",  # Primary color
    "secondary": "#1f2335",  # Secondary color
    "accent": "#565f89",  # Accent color
    "background": "#24283b",  # Background color
    "text": "#a9b1d6",  # Text color
    "card": "#1f2335",  # Card background
    "header": "#bb9af7",  # Header color
    "success": "#c3e88d",  # Success color
    "warning": "#ff757f",  # Warning color
    "error": "#c53b53",  # Error color
    "chart_colors": [
        "#1976D2",
        "#64B5F6",
        "#0D47A1",
        "#BBDEFB",
        "#2196F3",
    ],  # Chart colors
}

# Custom CSS with the selected theme colors
st.markdown(
    f"""
    <style>
    /* Apply the color theme */
    .main-header {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {theme["primary"]};
        margin-bottom: 1rem;
    }}
    
    .sub-header {{
        font-size: 1.5rem;
        font-weight: 600;
        color: {theme["header"]};
        margin-top: 1.5rem;
    }}
    
    .metric-card {{
        background-color: {theme["card"]};
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid {theme["primary"]};
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
    }}
    
    /* Style alert messages */
    .stAlert {{
        max-width: 578px !important;
    }}
    
    /* Style the overall page */
    .stApp {{
        background-color: {theme["background"]};
    }}
    
    /* Style tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: {theme["card"]};
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        color: {theme["text"]};
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {theme["secondary"]} !important;
        color: {'#FFFFFF' if theme["primary"] != "#FFFFFF" else theme["text"]} !important;
    }}
    
    /* Style metric values */
    [data-testid="stMetricValue"] {{
        color: {theme["primary"]};
        font-weight: bold;
    }}
    
    /* Style metric labels */
    [data-testid="stMetricLabel"] {{
        color: {theme["text"]};
    }}
    
    /* Style the file uploader */
    [data-testid="stFileUploader"] {{
        width: 100% !important;
    }}
    
    /* Style buttons */
    .stButton button {{
        background-color: {theme["primary"]};
        color: {'#FFFFFF' if theme["primary"] != "#FFFFFF" else '#000000'};
        border: none;
    }}
    
    .stButton button:hover {{
        background-color: {theme["secondary"]};
    }}
    
    /* Style text elements */
    p, ol, ul, dl {{
        color: {theme["text"]};
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: {theme["header"]};
    }}
    
    /* Style info boxes */
    .stInfo {{
        background-color: {theme["card"]};
        color: {theme["text"]};
        border-left-color: {theme["primary"]};
    }}
    
    /* Style warning boxes */
    .stWarning {{
        background-color: {theme["card"]};
        color: {theme["text"]};
        border-left-color: {theme["warning"]};
    }}
    
    /* Style error boxes */
    .stError {{
        background-color: {theme["card"]};
        color: {theme["text"]};
        border-left-color: {theme["error"]};
    }}
    
    /* Style success boxes */
    .stSuccess {{
        background-color: {theme["card"]};
        color: {theme["text"]};
        border-left-color: {theme["success"]};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# App header
st.markdown(
    '<div class="main-header">NerdType Dashboard</div>',
    unsafe_allow_html=True,
)


# Load and prepare data
def load_data(uploaded_file):
    try:
        data = json.loads(uploaded_file.getvalue().decode("utf-8"))
        df = pd.DataFrame(data)
        # Convert date strings to datetime
        df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y, %H:%M:%S")
        # Extract just the date part for grouping
        df["day"] = df["date"].dt.date
        # Convert accuracy from string to float
        df["accuracy"] = df["accuracy"].str.rstrip("%").astype(float)
        # Set timeLeft to 0 for entries that don't have it
        if "timeLeft" not in df.columns:
            df["timeLeft"] = 0
        # Handle Zen Mode where there's totalTime instead of timeLeft and score
        if "totalTime" in df.columns:
            # Mark Zen Mode entries
            df["is_zen_mode"] = df["mode"] == "Zen Mode"
            # Fill missing scores with NaN
            if "score" not in df.columns:
                df["score"] = np.nan
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


# Main app layout
st.markdown("## Upload Your Data")
col1, col2 = st.columns([1, 2])
with col1:
    uploaded_file = st.file_uploader(
        "Upload your typing game data (JSON file)",
        type="json",
        key="file_uploader",
        help="Drag and drop a JSON file here or click to browse files",
    )

if uploaded_file is not None:
    # Load the data
    df = load_data(uploaded_file)

    if not df.empty:
        # Overall Performance Metrics
        st.markdown(
            '<div class="sub-header">Overall Performance</div>', unsafe_allow_html=True
        )

        # Create columns for key metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Average WPM", f"{df['wpm'].mean():.1f}")

        with col2:
            st.metric("Average Accuracy", f"{df['accuracy'].mean():.1f}%")

        with col3:
            # Only show average score if not all entries are Zen Mode
            non_zen = df[df["mode"] != "Zen Mode"]
            if not non_zen.empty and "score" in df.columns:
                st.metric("Average Score", f"{non_zen['score'].mean():.0f}")
            else:
                st.metric("Total Sessions", len(df))

        with col4:
            st.metric("Max WPM", f"{df['wpm'].max():.0f}")

        # Performance Trends with Tabs
        st.markdown(
            '<div class="sub-header">Performance Trends</div>', unsafe_allow_html=True
        )

        # Create tabs for different performance metrics
        tab1, tab2, tab3 = st.tabs(
            ["WPM Over Time", "Accuracy Over Time", "Score Over Time"]
        )

        # Ensure the data is sorted by date
        df_time = df.sort_values("date")

        with tab1:
            # Group by day and calculate mean WPM
            daily_wpm = df_time.groupby("day")["wpm"].mean().reset_index()
            daily_wpm["day"] = pd.to_datetime(daily_wpm["day"])

            # Create the Plotly line chart for WPM using theme colors
            fig_wpm = px.line(
                daily_wpm,
                x="day",
                y="wpm",
                title="Average WPM by Day",
                labels={"day": "Date", "wpm": "Words Per Minute"},
                line_shape="linear",
                color_discrete_sequence=[theme["primary"]],
            )

            # Add markers and improve layout
            fig_wpm.update_traces(mode="lines+markers", marker=dict(size=8))
            fig_wpm.update_layout(
                xaxis_title="Date",
                yaxis_title="Words Per Minute (WPM)",
                hovermode="x unified",
                height=500,
                paper_bgcolor=theme["background"],
                plot_bgcolor=theme["background"],
                font=dict(color=theme["text"]),
            )

            # Update grid and axes colors
            fig_wpm.update_xaxes(
                gridcolor="rgba(128,128,128,0.1)", zerolinecolor="rgba(128,128,128,0.2)"
            )
            fig_wpm.update_yaxes(
                gridcolor="rgba(128,128,128,0.1)", zerolinecolor="rgba(128,128,128,0.2)"
            )

            # Add a simple moving average line
            window_size = min(5, len(daily_wpm))
            if window_size > 1:
                daily_wpm["wpm_ma"] = (
                    daily_wpm["wpm"].rolling(window=window_size, min_periods=1).mean()
                )
                fig_wpm.add_trace(
                    go.Scatter(
                        x=daily_wpm["day"],
                        y=daily_wpm["wpm_ma"],
                        mode="lines",
                        line=dict(color=theme["accent"], dash="dash", width=2),
                        name=f"{window_size}-Day Moving Average",
                    )
                )

            st.plotly_chart(fig_wpm, use_container_width=True)

        with tab2:
            # Group by day and calculate mean accuracy
            daily_accuracy = df_time.groupby("day")["accuracy"].mean().reset_index()
            daily_accuracy["day"] = pd.to_datetime(daily_accuracy["day"])

            # Create the Plotly line chart for Accuracy
            fig_accuracy = px.line(
                daily_accuracy,
                x="day",
                y="accuracy",
                title="Average Accuracy by Day",
                labels={"day": "Date", "accuracy": "Accuracy (%)"},
                line_shape="linear",
                color_discrete_sequence=[theme["primary"]],
            )

            # Add markers and improve layout
            fig_accuracy.update_traces(mode="lines+markers", marker=dict(size=8))
            fig_accuracy.update_layout(
                xaxis_title="Date",
                yaxis_title="Accuracy (%)",
                hovermode="x unified",
                height=500,
                paper_bgcolor=theme["background"],
                plot_bgcolor=theme["background"],
                font=dict(color=theme["text"]),
            )

            # Update grid and axes colors
            fig_accuracy.update_xaxes(
                gridcolor="rgba(128,128,128,0.1)", zerolinecolor="rgba(128,128,128,0.2)"
            )
            fig_accuracy.update_yaxes(
                gridcolor="rgba(128,128,128,0.1)", zerolinecolor="rgba(128,128,128,0.2)"
            )

            # Add a trend line
            trend = px.scatter(
                daily_accuracy,
                x="day",
                y="accuracy",
                trendline="ols",
                color_discrete_sequence=[theme["accent"]],
            ).data[1]
            trend.update(
                hovertemplate="Trend: %{y:.1f}%<extra></extra>", name="Trend Line"
            )
            fig_accuracy.add_trace(trend)

            st.plotly_chart(fig_accuracy, use_container_width=True)

        with tab3:
            # Filter out Zen Mode data (which doesn't have scores)
            df_with_score = df_time[df_time["mode"] != "Zen Mode"].copy()

            if not df_with_score.empty and "score" in df_with_score.columns:
                # Group by day and calculate mean score
                daily_score = df_with_score.groupby("day")["score"].mean().reset_index()
                daily_score["day"] = pd.to_datetime(daily_score["day"])

                # Create the Plotly line chart for Score
                fig_score = px.line(
                    daily_score,
                    x="day",
                    y="score",
                    title="Average Score by Day",
                    labels={"day": "Date", "score": "Score"},
                    line_shape="linear",
                    color_discrete_sequence=[theme["primary"]],
                )

                # Add markers and improve layout
                fig_score.update_traces(mode="lines+markers", marker=dict(size=8))
                fig_score.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Score",
                    hovermode="x unified",
                    height=500,
                    paper_bgcolor=theme["background"],
                    plot_bgcolor=theme["background"],
                    font=dict(color=theme["text"]),
                )

                # Update grid and axes colors
                fig_score.update_xaxes(
                    gridcolor="rgba(128,128,128,0.1)",
                    zerolinecolor="rgba(128,128,128,0.2)",
                )
                fig_score.update_yaxes(
                    gridcolor="rgba(128,128,128,0.1)",
                    zerolinecolor="rgba(128,128,128,0.2)",
                )

                # Add a trend line
                trend = px.scatter(
                    daily_score,
                    x="day",
                    y="score",
                    trendline="ols",
                    color_discrete_sequence=[theme["accent"]],
                ).data[1]
                trend.update(
                    hovertemplate="Trend: %{y:.0f}<extra></extra>", name="Trend Line"
                )
                fig_score.add_trace(trend)

                st.plotly_chart(fig_score, use_container_width=True)
            else:
                st.info(
                    "Score data is not available for the selected filters or game modes."
                )

        # Performance by Category - 2 columns layout
        st.markdown(
            '<div class="sub-header">Performance by Category</div>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            # Performance by mode
            if "mode" in df.columns:
                mode_performance = (
                    df.groupby("mode")[["wpm", "accuracy"]].mean().reset_index()
                )
                # Sort by average WPM
                mode_performance = mode_performance.sort_values("wpm", ascending=False)
                # Create the bar chart
                fig_mode = px.bar(
                    mode_performance,
                    x="mode",
                    y="wpm",
                    color="accuracy",
                    title="Average WPM by Game Mode",
                    color_continuous_scale="Viridis",
                    labels={
                        "wpm": "Words Per Minute",
                        "mode": "Game Mode",
                        "accuracy": "Accuracy (%)",
                    },
                )
                fig_mode.update_layout(
                    xaxis_title="Game Mode",
                    yaxis_title="Words Per Minute (WPM)",
                    coloraxis_colorbar_title="Accuracy (%)",
                    height=400,
                    paper_bgcolor=theme["background"],
                    plot_bgcolor=theme["background"],
                    font=dict(color=theme["text"]),
                )

                # Update grid and axes colors
                fig_mode.update_xaxes(
                    gridcolor="rgba(128,128,128,0.1)",
                    zerolinecolor="rgba(128,128,128,0.2)",
                )
                fig_mode.update_yaxes(
                    gridcolor="rgba(128,128,128,0.1)",
                    zerolinecolor="rgba(128,128,128,0.2)",
                )

                st.plotly_chart(fig_mode, use_container_width=True)

        with col2:
            # Performance by word list
            if "wordList" in df.columns:
                wordlist_performance = (
                    df.groupby("wordList")[["wpm", "accuracy"]].mean().reset_index()
                )
                # Sort by average WPM
                wordlist_performance = wordlist_performance.sort_values(
                    "wpm", ascending=False
                )
                # Create the bar chart
                fig_wordlist = px.bar(
                    wordlist_performance,
                    x="wordList",
                    y="wpm",
                    color="accuracy",
                    title="Average WPM by Word List",
                    color_continuous_scale="Viridis",
                    labels={
                        "wpm": "Words Per Minute",
                        "wordList": "Word List",
                        "accuracy": "Accuracy (%)",
                    },
                )
                fig_wordlist.update_layout(
                    xaxis_title="Word List",
                    yaxis_title="Words Per Minute (WPM)",
                    coloraxis_colorbar_title="Accuracy (%)",
                    height=400,
                    paper_bgcolor=theme["background"],
                    plot_bgcolor=theme["background"],
                    font=dict(color=theme["text"]),
                )

                # Update grid and axes colors
                fig_wordlist.update_xaxes(
                    gridcolor="rgba(128,128,128,0.1)",
                    zerolinecolor="rgba(128,128,128,0.2)",
                )
                fig_wordlist.update_yaxes(
                    gridcolor="rgba(128,128,128,0.1)",
                    zerolinecolor="rgba(128,128,128,0.2)",
                )

                st.plotly_chart(fig_wordlist, use_container_width=True)
    else:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.error("Failed to load data. Please check your JSON file format.")
else:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.info("Please upload your typing game data JSON file to begin analysis.")

        # Example of what can be analyzed
        st.markdown(
            """
            ### What insights will this dashboard show?
            
            Once you upload your NerdType data, this dashboard will display:
            
            - Your overall typing performance metrics (average WPM, accuracy, and more)
            - WPM trends over time with a moving average
            - Performance comparison across different game modes
            - Performance comparison across different word lists
            
            Simply upload your typing game data in JSON format to get started!
            """
        )
