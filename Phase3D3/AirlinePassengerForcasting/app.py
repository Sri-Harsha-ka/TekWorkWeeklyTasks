import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
 
from src.data_loader import DataLoader
from src.forcast import Forecaster
from src.evaluation import Evaluator
 
# ------------------------------------------------
# Page Configuration & Custom CSS
# ------------------------------------------------

 
st.set_page_config(
    page_title="Airline Passenger Forecaster",
    page_icon="✈️",
    layout="wide"
)
 
# Custom CSS for a minimalist dark look
st.markdown("""
    <style>
    :root {
        --bg: #0b0f14;
        --panel: #11161d;
        --panel-2: #151b23;
        --border: #243041;
        --text: #f4f7fb;
        --muted: #a8b3c2;
        --blue: #3b82f6;
        --green: #22c55e;
    }

    html, body, [class*="css"], .stApp {
        background-color: var(--bg);
        color: var(--text);
    }

    .main {
        background-color: var(--bg);
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .section-shell {
        background: linear-gradient(180deg, var(--panel) 0%, var(--panel-2) 100%);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1.25rem 1.25rem 0.75rem 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.22);
    }

    .section-title {
        margin: 0 0 0.4rem 0;
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        color: var(--text);
    }

    .section-subtitle {
        margin: 0 0 0.75rem 0;
        color: var(--muted);
        font-size: 0.92rem;
    }

    .hero-card {
        background: radial-gradient(circle at top left, rgba(59, 130, 246, 0.16), transparent 40%),
                    linear-gradient(180deg, var(--panel) 0%, var(--panel-2) 100%);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f141b 0%, #0b0f14 100%);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] * {
        color: var(--text);
    }

    .stMarkdown, .stCaption, p, label, span, h1, h2, h3, h4, h5, h6 {
        color: var(--text);
    }

    .stCaption {
        color: var(--muted);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
        border-bottom: 1px solid var(--border);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--muted);
        border-radius: 0.75rem 0.75rem 0 0;
        padding: 0.65rem 1rem;
    }

    .stTabs [aria-selected="true"] {
        color: var(--text);
        background: var(--panel);
        border: 1px solid var(--border);
        border-bottom: 1px solid var(--panel);
    }

    .stMetric {
        background: linear-gradient(180deg, var(--panel) 0%, var(--panel-2) 100%);
        border: 1px solid var(--border);
        padding: 1rem;
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
    }

    [data-testid="stDataFrame"] {
        background-color: var(--panel);
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    div.stButton > button:first-child,
    div[data-testid="stDownloadButton"] > button {
        color: white;
        width: 100%;
        border: 1px solid transparent;
        border-radius: 10px;
        height: 3em;
        font-weight: 600;
        transition: transform 0.15s ease, box-shadow 0.15s ease, background-color 0.15s ease;
    }

    div.stButton > button:first-child {
        background: linear-gradient(135deg, #2563eb 0%, var(--blue) 100%);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.22);
    }

    div[data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, #16a34a 0%, var(--green) 100%);
        box-shadow: 0 8px 20px rgba(34, 197, 94, 0.22);
    }

    div.stButton > button:first-child:hover,
    div[data-testid="stDownloadButton"] > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.28);
    }

    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div,
    .stSlider [data-baseweb="slider"] {
        background-color: var(--panel);
        color: var(--text);
        border-color: var(--border);
    }

    .stAlert {
        background-color: var(--panel);
        color: var(--text);
        border: 1px solid var(--border);
    }
    </style>
    """, unsafe_allow_html=True)
 
# ------------------------------------------------
# Data & Header
# ------------------------------------------------

from pathlib import Path

BASE_DIR = Path(__file__).parent

csv_path = BASE_DIR / "data" / "airline-passengers.csv"
 
loader = DataLoader(csv_path)
df = loader.load_data()
 
st.markdown('<div class="hero-card">', unsafe_allow_html=True)
st.title("✈️ Airline Passenger Analysis & Forecasting")
st.caption("Predicting global travel trends using Recurrent Neural Networks (RNN)")
hero_cols = st.columns(3)
hero_cols[0].metric("Dataset Rows", len(df))
hero_cols[1].metric("First Month", str(df.index.min().date()))
hero_cols[2].metric("Last Month", str(df.index.max().date()))
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-shell">', unsafe_allow_html=True)
st.markdown('<p class="section-title">Forecast Controls</p>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">Move the horizon slider here in the main layout. No sidebar needed.</p>', unsafe_allow_html=True)
control_col1, control_col2 = st.columns([2, 1])
with control_col1:
    future_months = st.slider("Forecast Horizon (Months)", 1, 24, 12)
with control_col2:
    st.info("Use the slider to change the prediction window for the RNN model.")
st.markdown('</div>', unsafe_allow_html=True)
 
# ------------------------------------------------
# Metrics & Overview Tabs
# ------------------------------------------------
 
st.markdown('<div class="section-shell">', unsafe_allow_html=True)
st.markdown('<p class="section-title">Model Snapshot</p>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">Quick performance indicators before you inspect the data or generate a forecast.</p>', unsafe_allow_html=True)
snapshot_cols = st.columns(3)

with snapshot_cols[0]:
    st.metric("Forecast Horizon", f"{future_months} months")

with snapshot_cols[1]:
    st.metric("Timeline Span", f"{len(df)} points")

with snapshot_cols[2]:
    st.metric("Latest Passengers", f"{int(df['Passengers'].iloc[-1])}")

st.markdown('</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🚀 Model Performance", "🔎 Exploratory Data Analysis"])
 
with tab1:
    st.subheader("Model Accuracy Metrics")
    mae, mse, rmse = Evaluator().evaluate()
   
    m1, m2, m3 = st.columns(3)
    m1.metric("Mean Absolute Error (MAE)", f"{mae:.2f}", delta_color="inverse")
    m2.metric("Mean Squared Error (MSE)", f"{mse:.2f}", delta_color="inverse")
    m3.metric("Root Mean Squared Error (RMSE)", f"{rmse:.2f}", delta_color="inverse")
 
with tab2:
    col_a, col_b = st.columns([1, 2])
   
    with col_a:
        st.subheader("Raw Data")
        st.dataframe(df, height=350)
   
    with col_b:
        st.subheader("Historical Trend")
        fig = px.line(df, x=df.index, y="Passengers",
                      template="plotly_dark",
                      color_discrete_sequence=['#3b82f6'])
        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f4f7fb')
        )
        st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-shell">', unsafe_allow_html=True)
st.markdown('<p class="section-title">Forecast Workspace</p>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">Generate the future projection and review the output in a two-panel layout.</p>', unsafe_allow_html=True)
 
# ------------------------------------------------
# Forecasting Section
# ------------------------------------------------
 
st.header("🔮 Generate Future Forecast")
 
if st.button("Run RNN Model"):
    with st.spinner("Analyzing temporal patterns..."):
        forecaster = Forecaster()
        future = forecaster.forecast(future_months)
       
        last_date = df.index[-1]
        future_dates = pd.date_range(
            start=last_date + pd.DateOffset(months=1),
            periods=future_months,
            freq="MS"
        )
 
        forecast_df = pd.DataFrame({
            "Month": future_dates,
            "Predicted Passengers": future.flatten()
        })
 
    st.success(f"Successfully generated forecast for {future_months} months!")
 
    # Layout for Results
    res_col1, res_col2 = st.columns([1, 2])
 
    with res_col1:
        st.subheader("Forecasted Values")
        st.dataframe(forecast_df, use_container_width=True)
       
        csv = forecast_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="forecast_results.csv",
            mime="text/csv"
        )
 
    with res_col2:
        st.subheader("Combined Projection")
       
        # Create a combined chart with Plotly
        fig_combined = go.Figure()
       
        # Historical Data
        fig_combined.add_trace(go.Scatter(
            x=df.index, y=df["Passengers"],
            name="Historical", line=dict(color="#94a3b8", width=2)
        ))
       
        # Forecasted Data
        fig_combined.add_trace(go.Scatter(
            x=forecast_df["Month"], y=forecast_df["Predicted Passengers"],
            name="Forecast", line=dict(color="#22c55e", width=3, dash='dot')
        ))
       
        fig_combined.update_layout(
            template="plotly_dark",
            hovermode="x unified",
            margin=dict(l=0, r=0, t=30, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f4f7fb')
        )
        st.plotly_chart(fig_combined, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)