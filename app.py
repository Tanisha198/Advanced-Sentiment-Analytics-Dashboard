import streamlit as st
import matplotlib.pyplot as plt
from utils.predictor import analyze_sentiment

st.set_page_config(page_title="Sentiment Analysis", layout="wide")

st.title("Sentiment Prediction Dashboard")
st.write("Analyze the sentiment of your comments — Positive, Negative, or Neutral!")

input_method = st.radio("Choose input method:", ["Enter comments manually", "Upload a text file"])

comments = []

if input_method == "Enter comments manually":
    user_input = st.text_area("Enter comments (one per line):")
    if user_input:
        comments = user_input.split("\n")

else:
    uploaded_file = st.file_uploader("Upload .txt file")
    if uploaded_file:
        text_data = uploaded_file.read().decode("utf-8")
        comments = text_data.split("\n")

if st.button("Analyze Sentiments"):
    if not comments:
        st.warning("Please enter or upload comments!")
    else:
        results = [analyze_sentiment(c) for c in comments]

        st.subheader("Sentiment Results")
        for c, r in zip(comments, results):
            st.write(f"**{c} → {r}**")

        # Chart
        labels = ["Positive", "Negative", "Neutral"]
        values = [results.count("Positive"), results.count("Negative"), results.count("Neutral")]

        fig, ax = plt.subplots()
        # Different colors for each column
        colors = ["green", "red", "orange"]   # Positive, Negative, Neutral

        ax.bar(labels, values, color=colors)
        ax.set_title("Sentiment Distribution")

        st.pyplot(fig)



