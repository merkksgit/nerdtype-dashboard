import json

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

# Set page config
favicon = Image.open("./images/logo-no-keyboard-blue-bg-32x32.png")
st.set_page_config(page_title="NerdType | Dashboard", layout="wide", page_icon=favicon)

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
    ],
}

st.markdown(
    f"""
    <style>
    /* Apply the color theme */
    .main-header {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {theme["primary"]};
        margin-bottom: 1rem;
        text-align: center;
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

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("./images/logo-text-link.png")

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


# Main app layoutcol1, col2, col3 = st.columns([1, 1, 1])
st.markdown('<div style="text-align: center;"><h2>Upload Your Data</h2></div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
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

                # WPM vs Accuracy Scatter Plot
        st.markdown(
            '<div class="sub-header">WPM vs Accuracy Analysis</div>', unsafe_allow_html=True
        )
        st.markdown(
            '<p style="color: #565f89; font-style: italic; margin-bottom: 1rem;">Shows the relationship between your typing speed and accuracy across different game modes. Look for your optimal balance point where high speed meets high accuracy.</p>',
            unsafe_allow_html=True
        )
        
        # Create scatter plot - simplified version to avoid validation errors
        fig_scatter = px.scatter(
            df,
            x="accuracy",
            y="wpm",
            color="mode",
            title="WPM vs Accuracy by Game Mode",
            labels={
                "accuracy": "Accuracy (%)",
                "wpm": "Words Per Minute",
                "mode": "Game Mode"
            },
            color_discrete_sequence=theme["chart_colors"]
        )
        
        fig_scatter.update_layout(
            xaxis_title="Accuracy (%)",
            yaxis_title="Words Per Minute (WPM)",
            height=500,
            paper_bgcolor=theme["background"],
            plot_bgcolor=theme["background"],
            font=dict(color=theme["text"]),
        )
        
        # Update grid and axes colors
        fig_scatter.update_xaxes(
            gridcolor="rgba(128,128,128,0.1)", zerolinecolor="rgba(128,128,128,0.2)"
        )
        fig_scatter.update_yaxes(
            gridcolor="rgba(128,128,128,0.1)", zerolinecolor="rgba(128,128,128,0.2)"
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)

        # Games Played Activity Graph
        st.markdown(
            '<div class="sub-header">Daily Activity Heatmap</div>', unsafe_allow_html=True
        )
        st.markdown(
            '<p style="color: #565f89; font-style: italic; margin-bottom: 1rem;">Activity calendar showing your daily typing practice consistency. Darker green squares indicate more games played that day.</p>',
            unsafe_allow_html=True
        )
        
        # Create daily activity data
        daily_activity = df.groupby("day").size().reset_index(name="games_played")
        daily_activity["day"] = pd.to_datetime(daily_activity["day"])
        
        # Create a complete date range to show gaps
        date_range = pd.date_range(
            start=daily_activity["day"].min(),
            end=daily_activity["day"].max(),
            freq="D"
        )
        
        # Create complete dataframe with all dates
        complete_dates = pd.DataFrame({"day": date_range})
        activity_complete = complete_dates.merge(daily_activity, on="day", how="left")
        activity_complete["games_played"] = activity_complete["games_played"].fillna(0)
        
        # Add calendar information
        activity_complete["week_start"] = activity_complete["day"] - pd.to_timedelta(activity_complete["day"].dt.dayofweek, unit="d")
        activity_complete["day_of_week"] = activity_complete["day"].dt.dayofweek
        activity_complete["week_number"] = ((activity_complete["day"] - activity_complete["day"].min()).dt.days // 7)
        activity_complete["date_str"] = activity_complete["day"].dt.strftime("%Y-%m-%d")
        activity_complete["month_label"] = activity_complete["day"].dt.strftime("%b")
        
        fig_activity = go.Figure()
        
        # Define color scale based on games played
        max_games = activity_complete["games_played"].max()
        
        def get_color_intensity(games_played, max_games):
            if games_played == 0:
                return "#161b22"  # Dark background for no activity
            elif games_played <= max_games * 0.25:
                return "#0e4429"  # Light green
            elif games_played <= max_games * 0.5:
                return "#006d32"  # Medium green
            elif games_played <= max_games * 0.75:
                return "#26a641"  # Bright green
            else:
                return "#39d353"  # Brightest green
        
        # Add the heatmap squares
        colors = [get_color_intensity(games, max_games) for games in activity_complete["games_played"]]
        
        fig_activity.add_trace(go.Scatter(
            x=activity_complete["day_of_week"],
            y=activity_complete["week_number"],
            mode="markers",
            marker=dict(
                size=15,
                color=colors,
                symbol="square",
                line=dict(width=1, color="#21262d")
            ),
            text=activity_complete["date_str"] + "<br>Games: " + activity_complete["games_played"].astype(int).astype(str),
            hovertemplate="<b>%{text}</b><extra></extra>",
            showlegend=False
        ))
        
        fig_activity.update_layout(
            title=f"Daily Typing Activity ({activity_complete['day'].min().strftime('%b %Y')} - {activity_complete['day'].max().strftime('%b %Y')})",
            xaxis=dict(
                title="",
                tickmode="array",
                tickvals=[0, 1, 2, 3, 4, 5, 6],
                ticktext=["Mon", "", "Wed", "", "Fri", "", "Sun"],
                showgrid=False,
                zeroline=False
            ),
            yaxis=dict(
                title="",
                showticklabels=False,
                showgrid=False,
                zeroline=False,
                autorange="reversed"  # Show recent weeks at top
            ),
            height=max(200, len(activity_complete["week_number"].unique()) * 20 + 80),
            paper_bgcolor=theme["background"],
            plot_bgcolor=theme["background"],
            font=dict(color=theme["text"]),
            margin=dict(l=20, r=20, t=60, b=40)
        )
        
        st.plotly_chart(fig_activity, use_container_width=True)
        
        # Add activity statistics
        col1, col2, col3, col4 = st.columns(4)
        
        total_days = len(activity_complete)
        active_days = len(activity_complete[activity_complete["games_played"] > 0])
        total_games = activity_complete["games_played"].sum()
        avg_games_per_active_day = activity_complete[activity_complete["games_played"] > 0]["games_played"].mean()
        
        with col1:
            st.metric("Total Days", total_days)
        with col2:
            st.metric("Active Days", f"{active_days} ({active_days/total_days*100:.1f}%)")
        with col3:
            st.metric("Total Games", f"{total_games:.0f}")
        with col4:
            st.metric("Avg Games/Active Day", f"{avg_games_per_active_day:.1f}" if not pd.isna(avg_games_per_active_day) else "0")

        # Performance Heatmap
        st.markdown(
            '<div class="sub-header">Performance Calendar Heatmap</div>', unsafe_allow_html=True
        )
        st.markdown(
            '<p style="color: #565f89; font-style: italic; margin-bottom: 1rem;">Calendar view of your daily average WPM performance. Each square represents a day, with color intensity showing your typing speed that day.</p>',
            unsafe_allow_html=True
        )
        
        # Create daily performance data
        daily_performance = df.groupby("day").agg({
            "wpm": "mean",
            "accuracy": "mean"
        }).reset_index()
        daily_performance["day"] = pd.to_datetime(daily_performance["day"])
        daily_performance["date_str"] = daily_performance["day"].dt.strftime("%Y-%m-%d")
        daily_performance["weekday"] = daily_performance["day"].dt.day_name()
        daily_performance["week_number"] = daily_performance["day"].dt.isocalendar().week
        daily_performance["day_of_week"] = daily_performance["day"].dt.dayofweek
        
        # Create a proper calendar-style heatmap
        if len(daily_performance) > 1:
            # Create week-based layout
            min_week = daily_performance["week_number"].min()
            daily_performance["week_from_start"] = daily_performance["week_number"] - min_week
            
            fig_heatmap = go.Figure(data=go.Scatter(
                x=daily_performance["day_of_week"],
                y=daily_performance["week_from_start"],
                mode="markers",
                marker=dict(
                    size=25,
                    color=daily_performance["wpm"],
                    colorscale="Viridis",
                    showscale=True,
                    colorbar=dict(title="Average WPM"),
                    symbol="square",
                    line=dict(width=1, color="white")
                ),
                text=daily_performance["date_str"] + "<br>WPM: " + daily_performance["wpm"].round(2).astype(str) + "<br>Accuracy: " + daily_performance["accuracy"].round(2).astype(str) + "%",
                hovertemplate="<b>%{text}</b><extra></extra>",
                showlegend=False
            ))
            
            fig_heatmap.update_layout(
                title="Daily Performance Calendar Heatmap (Average WPM)",
                xaxis=dict(
                    title="Day of Week",
                    tickmode="array",
                    tickvals=[0, 1, 2, 3, 4, 5, 6],
                    ticktext=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                    showgrid=False
                ),
                yaxis=dict(
                    title="Week",
                    showgrid=False,
                    autorange="reversed"  # Show most recent weeks at top
                ),
                height=max(300, len(daily_performance["week_from_start"].unique()) * 50 + 100),
                paper_bgcolor=theme["background"],
                plot_bgcolor=theme["background"],
                font=dict(color=theme["text"]),
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            # Fallback for single day data
            fig_heatmap = go.Figure(data=go.Scatter(
                x=daily_performance["day"],
                y=[1] * len(daily_performance),
                mode="markers",
                marker=dict(
                    size=30,
                    color=daily_performance["wpm"],
                    colorscale="Viridis",
                    showscale=True,
                    colorbar=dict(title="Average WPM"),
                    symbol="square"
                ),
                text=daily_performance["date_str"] + "<br>WPM: " + daily_performance["wpm"].round(2).astype(str) + "<br>Accuracy: " + daily_performance["accuracy"].round(2).astype(str) + "%",
                hovertemplate="<b>%{text}</b><extra></extra>",
                showlegend=False
            ))
            
            fig_heatmap.update_layout(
                title="Daily Performance Timeline (Average WPM)",
                xaxis_title="Date",
                yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
                height=200,
                paper_bgcolor=theme["background"],
                plot_bgcolor=theme["background"],
                font=dict(color=theme["text"]),
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)

        # Learning Curves Analysis - 2 columns layout
        st.markdown(
            '<div class="sub-header">Learning Curves Analysis</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="color: #565f89; font-style: italic; margin-bottom: 1rem;">Track your improvement over time across different word lists and game modes. Rolling averages smooth out session-to-session variation to show clear progress trends.</p>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            # Learning Curve by Word List
            if "wordList" in df.columns:
                # Create learning curves for each word list
                fig_learning_wordlist = go.Figure()
                
                df_sorted = df.sort_values("date")
                
                for i, word_list in enumerate(df["wordList"].unique()):
                    wordlist_data = df_sorted[df_sorted["wordList"] == word_list].copy()
                    
                    if len(wordlist_data) > 1:  # Only show if there's more than one data point
                        # Add session number for this word list
                        wordlist_data["session_number"] = range(1, len(wordlist_data) + 1)
                        
                        # Calculate rolling average
                        window_size = min(3, len(wordlist_data))
                        wordlist_data["wpm_rolling"] = wordlist_data["wpm"].rolling(
                            window=window_size, min_periods=1
                        ).mean()
                        
                        fig_learning_wordlist.add_trace(go.Scatter(
                            x=wordlist_data["session_number"],
                            y=wordlist_data["wpm_rolling"],
                            mode="lines+markers",
                            name=word_list,
                            line=dict(color=theme["chart_colors"][i % len(theme["chart_colors"])]),
                            hovertemplate=f"<b>{word_list}</b><br>Session: %{{x}}<br>WPM: %{{y:.2f}}<extra></extra>"
                        ))
                
                fig_learning_wordlist.update_layout(
                    title="Learning Curve by Word List",
                    xaxis_title="Session Number",
                    yaxis_title="Words Per Minute (WPM)",
                    height=400,
                    paper_bgcolor=theme["background"],
                    plot_bgcolor=theme["background"],
                    font=dict(color=theme["text"]),
                )
                
                fig_learning_wordlist.update_xaxes(
                    gridcolor="rgba(128,128,128,0.1)",
                    zerolinecolor="rgba(128,128,128,0.2)",
                )
                fig_learning_wordlist.update_yaxes(
                    gridcolor="rgba(128,128,128,0.1)",
                    zerolinecolor="rgba(128,128,128,0.2)",
                )
                
                st.plotly_chart(fig_learning_wordlist, use_container_width=True)

        with col2:
            # Learning Curve by Game Mode
            if "mode" in df.columns:
                # Create learning curves for each game mode
                fig_learning_mode = go.Figure()
                
                df_sorted = df.sort_values("date")
                
                for i, mode in enumerate(df["mode"].unique()):
                    mode_data = df_sorted[df_sorted["mode"] == mode].copy()
                    
                    if len(mode_data) > 1:  # Only show if there's more than one data point
                        # Add session number for this mode
                        mode_data["session_number"] = range(1, len(mode_data) + 1)
                        
                        # Calculate rolling average
                        window_size = min(3, len(mode_data))
                        mode_data["wpm_rolling"] = mode_data["wpm"].rolling(
                            window=window_size, min_periods=1
                        ).mean()
                        
                        fig_learning_mode.add_trace(go.Scatter(
                            x=mode_data["session_number"],
                            y=mode_data["wpm_rolling"],
                            mode="lines+markers",
                            name=mode,
                            line=dict(color=theme["chart_colors"][i % len(theme["chart_colors"])]),
                            hovertemplate=f"<b>{mode}</b><br>Session: %{{x}}<br>WPM: %{{y:.2f}}<extra></extra>"
                        ))
                
                fig_learning_mode.update_layout(
                    title="Learning Curve by Game Mode",
                    xaxis_title="Session Number",
                    yaxis_title="Words Per Minute (WPM)",
                    height=400,
                    paper_bgcolor=theme["background"],
                    plot_bgcolor=theme["background"],
                    font=dict(color=theme["text"]),
                )
                
                fig_learning_mode.update_xaxes(
                    gridcolor="rgba(128,128,128,0.1)",
                    zerolinecolor="rgba(128,128,128,0.2)",
                )
                fig_learning_mode.update_yaxes(
                    gridcolor="rgba(128,128,128,0.1)",
                    zerolinecolor="rgba(128,128,128,0.2)",
                )
                
                st.plotly_chart(fig_learning_mode, use_container_width=True)

        # Score Analysis
        st.markdown(
            '<div class="sub-header">Score Analysis</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="color: #565f89; font-style: italic; margin-bottom: 1rem;">Comprehensive scoring insights including efficiency analysis and personal best progression. Score efficiency reveals the optimal balance of speed vs accuracy for maximum points.</p>',
            unsafe_allow_html=True
        )
        
        # Filter out entries without scores (like Zen Mode)
        df_with_scores = df[df["score"].notna() & (df["score"] > 0)].copy()
        
        if not df_with_scores.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Score Efficiency Analysis (Score per WPM)
                df_with_scores["score_per_wpm"] = df_with_scores["score"] / df_with_scores["wpm"]
                
                fig_efficiency = px.scatter(
                    df_with_scores,
                    x="wpm",
                    y="score_per_wpm",
                    color="accuracy",
                    title="Score Efficiency Analysis (Score per WPM)",
                    labels={
                        "wpm": "Words Per Minute",
                        "score_per_wpm": "Score per WPM",
                        "accuracy": "Accuracy (%)"
                    },
                    color_continuous_scale="Viridis"
                )
                
                fig_efficiency.update_layout(
                    height=400,
                    paper_bgcolor=theme["background"],
                    plot_bgcolor=theme["background"],
                    font=dict(color=theme["text"]),
                )
                
                fig_efficiency.update_xaxes(
                    gridcolor="rgba(128,128,128,0.1)",
                    zerolinecolor="rgba(128,128,128,0.2)",
                )
                fig_efficiency.update_yaxes(
                    gridcolor="rgba(128,128,128,0.1)",
                    zerolinecolor="rgba(128,128,128,0.2)",
                )
                
                st.plotly_chart(fig_efficiency, use_container_width=True)
            
            with col2:
                # Score vs WPM scatter plot
                fig_score_wpm = px.scatter(
                    df_with_scores,
                    x="wpm",
                    y="score",
                    color="mode",
                    title="Score vs WPM Relationship",
                    labels={
                        "wpm": "Words Per Minute",
                        "score": "Score",
                        "mode": "Game Mode"
                    },
                    color_discrete_sequence=theme["chart_colors"]
                )
                
                fig_score_wpm.update_layout(
                    height=400,
                    paper_bgcolor=theme["background"],
                    plot_bgcolor=theme["background"],
                    font=dict(color=theme["text"]),
                )
                
                fig_score_wpm.update_xaxes(
                    gridcolor="rgba(128,128,128,0.1)",
                    zerolinecolor="rgba(128,128,128,0.2)",
                )
                fig_score_wpm.update_yaxes(
                    gridcolor="rgba(128,128,128,0.1)",
                    zerolinecolor="rgba(128,128,128,0.2)",
                )
                
                st.plotly_chart(fig_score_wpm, use_container_width=True)
            
            # High score progression over time
            df_scores_sorted = df_with_scores.sort_values("date")
            df_scores_sorted["session_number"] = range(1, len(df_scores_sorted) + 1)
            df_scores_sorted["personal_best"] = df_scores_sorted["score"].cummax()
            
            fig_score_progression = go.Figure()
            
            # Add individual scores
            fig_score_progression.add_trace(go.Scatter(
                x=df_scores_sorted["session_number"],
                y=df_scores_sorted["score"],
                mode="markers",
                name="Session Scores",
                marker=dict(
                    color=theme["accent"],
                    size=6,
                    opacity=0.6
                ),
                hovertemplate="Session %{x}<br>Score: %{y:.0f}<extra></extra>"
            ))
            
            # Add personal best progression line
            fig_score_progression.add_trace(go.Scatter(
                x=df_scores_sorted["session_number"],
                y=df_scores_sorted["personal_best"],
                mode="lines",
                name="Personal Best Progression",
                line=dict(
                    color=theme["primary"],
                    width=3
                ),
                hovertemplate="Session %{x}<br>Personal Best: %{y:.0f}<extra></extra>"
            ))
            
            fig_score_progression.update_layout(
                title="Score Progression Over Time",
                xaxis_title="Session Number",
                yaxis_title="Score",
                height=400,
                paper_bgcolor=theme["background"],
                plot_bgcolor=theme["background"],
                font=dict(color=theme["text"]),
            )
            
            fig_score_progression.update_xaxes(
                gridcolor="rgba(128,128,128,0.1)",
                zerolinecolor="rgba(128,128,128,0.2)",
            )
            fig_score_progression.update_yaxes(
                gridcolor="rgba(128,128,128,0.1)",
                zerolinecolor="rgba(128,128,128,0.2)",
            )
            
            st.plotly_chart(fig_score_progression, use_container_width=True)
            
        else:
            st.info("No score data available to display. Score analysis requires non-Zen Mode sessions.")

        # Performance Consistency Analysis
        st.markdown(
            '<div class="sub-header">Performance Consistency Analysis</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="color: #565f89; font-style: italic; margin-bottom: 1rem;">Measures how consistent your performance is across different game mode and word list combinations. Higher consistency scores indicate more predictable and stable typing performance.</p>',
            unsafe_allow_html=True
        )
        
        # Calculate consistency metrics
        consistency_stats = df.groupby(["mode", "wordList"]).agg({
            "wpm": ["mean", "std", "count"],
            "accuracy": ["mean", "std"]
        }).reset_index()
        
        # Flatten column names
        consistency_stats.columns = ["mode", "wordList", "wpm_mean", "wpm_std", "session_count", "accuracy_mean", "accuracy_std"]
        
        # Filter out combinations with less than 3 sessions
        consistency_stats = consistency_stats[consistency_stats["session_count"] >= 3]
        
        if not consistency_stats.empty:
            # Calculate consistency score (lower std = higher consistency)
            consistency_stats["consistency_score"] = 100 / (1 + consistency_stats["wpm_std"])
            consistency_stats["combo"] = consistency_stats["mode"] + " - " + consistency_stats["wordList"]
            
            # Sort by consistency score
            consistency_stats = consistency_stats.sort_values("consistency_score", ascending=False)
            
            # Create consistency chart
            fig_consistency = go.Figure()
            
            # Add consistency bars
            fig_consistency.add_trace(go.Bar(
                name="Consistency Score",
                x=consistency_stats["combo"],
                y=consistency_stats["consistency_score"].round(2),
                marker_color=theme["primary"],
                hovertemplate="<b>%{x}</b><br>Consistency: %{y:.2f}<br>Sessions: " + consistency_stats["session_count"].astype(str) + "<br>WPM Std: " + consistency_stats["wpm_std"].round(2).astype(str) + "<extra></extra>"
            ))
            
            fig_consistency.update_layout(
                title="Performance Consistency by Mode & Word List (Higher = More Consistent)",
                xaxis_title="Game Mode - Word List",
                yaxis_title="Consistency Score",
                height=400,
                paper_bgcolor=theme["background"],
                plot_bgcolor=theme["background"],
                font=dict(color=theme["text"]),
                xaxis=dict(tickangle=45)
            )
            
            fig_consistency.update_xaxes(
                gridcolor="rgba(128,128,128,0.1)",
                zerolinecolor="rgba(128,128,128,0.2)",
            )
            fig_consistency.update_yaxes(
                gridcolor="rgba(128,128,128,0.1)",
                zerolinecolor="rgba(128,128,128,0.2)",
            )
            
            st.plotly_chart(fig_consistency, use_container_width=True)
        else:
            st.info("Not enough data for consistency analysis (need at least 3 sessions per mode-wordlist combination)")

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
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.error("Failed to load data. Please check your JSON file format.")
else:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
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
