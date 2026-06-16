import streamlit as st
import pandas as pd
import plotly.express as px
from utils.predictor import analyze_sentiment

# Set up page configurations
st.set_page_config(page_title="Advanced Sentiment Analytics Dashboard", layout="wide", page_icon="📊")

# --- INITIALIZE STATE VARIABLES ---
# This prevents the app from forgetting the text data when the action button is clicked
if "processed_comments" not in st.session_state:
    st.session_state.processed_comments = []

# --- EXACT CUSTOM CSS TO MATCH IMAGE 2 SPECIFICATIONS ---
st.markdown("""
    <style>
        .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }
        .title-underline { margin: -10px 0 25px 0; border: 0; border-top: 3px solid #1d4ed8; }
        
        .exact-header-block {
            background-color: #e2e8f0 !important; 
            color: #1e293b !important;            
            padding: 10px 14px;
            border-radius: 6px;
            font-size: 1.2rem !important;
            font-weight: bold;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
            border: 1px solid #cbd5e1;
        }

        .stTextArea [data-baseweb="base-input"], .stFileUploader {
            background-color: #ffffff !important;
            border-radius: 6px !important;
        }

        button[data-testid="stBaseButton-primary"] {
            background-color: #0284c7 !important; 
            border-color: #0284c7 !important;
            color: white !important;
            font-weight: 500 !important;
            border-radius: 6px !important;
            height: 42px;
        }
        button[data-testid="stBaseButton-primary"]:hover { background-color: #0369a1 !important; }

        div[data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 10px 12px !important;
        }
        div[data-testid="stMetric"]:nth-of-type(1) { border-top: 4px solid #64748b; } 
        div[data-testid="stMetric"]:nth-of-type(2) { border-top: 4px solid #10b981; } 
        div[data-testid="stMetric"]:nth-of-type(3) { border-top: 4px solid #ef4444; } 
        div[data-testid="stMetric"]:nth-of-type(4) { border-top: 4px solid #f59e0b; } 
    </style>
""", unsafe_allow_html=True)

# Main Title Framework
st.title("📊 Advanced Sentiment Analytics Dashboard")
st.markdown('<div class="title-underline"></div>', unsafe_allow_html=True)

# Layout Setup
col1, col2 = st.columns([1, 1.4], gap="large")

with col1:
    with st.container(border=True):
        st.markdown('<div class="exact-header-block">📝 Data Input Configuration</div>', unsafe_allow_html=True)
        
        input_method = st.radio("Choose input source:", ["Enter comments manually", "Upload a text file"])
        st.markdown("<br>", unsafe_allow_html=True)
        
        current_comments = []
        
        if input_method == "Enter comments manually":
            user_input = st.text_area(
                "Enter comments (one per line):", 
                value="heloo how are you\nTyping second comment...", 
                height=140
            )
            if user_input:
                current_comments = [c.strip() for c in user_input.split("\n") if c.strip()]
        else:
            # FIXED: Streamlit native text processor file reader
            uploaded_file = st.file_uploader("Upload text file (.txt only)", type=["txt"])
            if uploaded_file is not None:
                # Read the incoming byte files securely without breaking variable loops
                text_bytes = uploaded_file.read()
                text_data = text_bytes.decode("utf-8")
                current_comments = [c.strip() for c in text_data.split("\n") if c.strip()]
                
                # Show an alert block confirming successful reading of rows
                st.success(f"📂 Found {len(current_comments)} rows inside the file!")

        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        analyze_clicked = st.button("🚀 Run Sentiment Analysis", use_container_width=True, type="primary")
        
        # Save values to persistent storage on click
        if analyze_clicked and current_comments:
            st.session_state.processed_comments = current_comments

with col2:
    with st.container(border=True):
        st.markdown('<div class="exact-header-block">🎯 Real-Time Analytics</div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

        # Fallback evaluation layer ensuring text blocks process seamlessly
        active_comments = st.session_state.processed_comments if st.session_state.processed_comments else current_comments

        if active_comments:
            results = [analyze_sentiment(c) for c in active_comments]
            df = pd.DataFrame({"Comment": active_comments, "Sentiment": results})
            
            pos_count = sum(df["Sentiment"] == "Positive")
            neg_count = sum(df["Sentiment"] == "Negative")
            neu_count = sum(df["Sentiment"] == "Neutral")
            total_count = len(df)

            # 1. Row of 4 Distinct Bordered KPI Cards
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Analyzed", total_count)
            m2.metric("Positive", pos_count, f"({int(pos_count/total_count*100)}%)" if total_count else "0%")
            m3.metric("Negative", neg_count, f"({int(neg_count/total_count*100)}%)" if total_count else "0%")
            m4.metric("Neutral", neu_count, f"({int(neu_count/total_count*100)}%)" if total_count else "0%")
            
            st.markdown("<hr style='margin: 15px 0; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)

            # 2. Section Navigation Tabs Split Components
            tab1, tab2 = st.tabs(["📊 Interactive Distribution Chart", "📋 Filterable Results Table"])
            
            with tab1:
                chart_df = pd.DataFrame({
                    "Sentiment": ["Positive", "Negative", "Neutral"],
                    "Count": [pos_count, neg_count, neu_count]
                })
                color_map = {"Positive": "#10b981", "Negative": "#ef4444", "Neutral": "#f59e0b"}
                
                fig = px.bar(chart_df, x="Sentiment", y="Count", color="Sentiment", color_discrete_map=color_map, text="Count")
                fig.update_layout(
                    height=220, showlegend=False,
                    margin=dict(l=30, r=20, t=15, b=15),
                    xaxis_title=None, yaxis_title="Count",
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
                )
                fig.update_yaxes(gridcolor='#f1f5f9', dtick=0.5)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            with tab2:
                st.write("Filter entries by sentiment type:")
                selected_sentiment = st.multiselect(
                    "", options=["Positive", "Negative", "Neutral"], default=["Positive", "Negative", "Neutral"], label_visibility="collapsed"
                )
                filtered_df = df[df["Sentiment"].isin(selected_sentiment)]
                st.dataframe(filtered_df, use_container_width=True, hide_index=True)
                
                csv_data = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Results as CSV", data=csv_data,
                    file_name="sentiment_analysis_export.csv", mime="text/csv", use_container_width=True
                )
        else:
            st.info("Please upload a file or type text in the left section to see results.")
