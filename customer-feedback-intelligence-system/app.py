import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import DataLoader
from services.sentiment_service import SentimentService
from services.keyword_service import KeywordService
from services.topic_service import TopicService
from services.report_service import ReportService


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Customer Feedback Intelligence System",
    layout="wide"
)

st.title("🧠 Customer Feedback Intelligence System")

st.markdown("""
Upload customer feedback CSV and get:
- Sentiment Analysis (Transfer Learning)
- Keyword Extraction (TF-IDF Feature Extraction)
- Topic Discovery (Clustering + Auto Naming)
- Business Insights Dashboard
""")


# =========================
# INIT SERVICES
# =========================
data_loader = DataLoader()
sentiment_service = SentimentService()
keyword_service = KeywordService()
topic_service = TopicService()
report_service = ReportService()


# =========================
# FILE UPLOAD
# =========================
uploaded_file = st.file_uploader(
    "Upload CSV file with 'feedback' column",
    type=["csv"]
)

if uploaded_file:

    try:
        df = data_loader.load_csv(uploaded_file)

        st.success("File loaded successfully!")

        st.subheader("📄 Data Preview")
        st.dataframe(df.head())

    except Exception as e:
        st.error(str(e))
        st.stop()


    # =========================
    # ANALYSIS BUTTON
    # =========================
    if st.button("🚀 Analyze Feedback"):

        # =========================
        # SENTIMENT ANALYSIS
        # =========================
        st.subheader("Sentiment Analysis")

        sentiments = []

        for text in df["feedback"]:
            result = sentiment_service.analyze(text)
            sentiments.append(result)

        df["sentiment"] = [s["label"] for s in sentiments]


        # =========================
        # TOPIC DETECTION
        # =========================
        st.subheader("Topic Discovery")

        df["topic"] = topic_service.discover_topics(
            df["feedback"].tolist()
        )


        # =========================
        # BUSINESS SUMMARY
        # =========================
        summary = report_service.generate_summary(df)


        # =========================
        # KPI METRICS
        # =========================
        st.subheader("📊 Overview Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Feedback", summary["total_feedback"])
        col2.metric("Positive Feedback", summary["positive_feedback"])
        col3.metric("Negative Feedback", summary["negative_feedback"])


        # =========================
        # 3-COLUMN CHART ROW
        # =========================
        st.subheader("📊 Analytics Dashboard")

        col1, col2, col3 = st.columns(3)

        # -------------------------
        # SENTIMENT CHART
        # -------------------------
        with col1:
            st.markdown("### 📈 Sentiment")

            sentiment_counts = df["sentiment"].value_counts().reset_index()
            sentiment_counts.columns = ["sentiment", "count"]

            fig1 = px.bar(
                sentiment_counts,
                x="sentiment",
                y="count",
                color="sentiment",
                text="count",
                title="Sentiment Breakdown"
            )

            st.plotly_chart(fig1, use_container_width=True)


        # -------------------------
        # KEYWORDS CHART (PX ONLY)
        # -------------------------
        with col2:
            st.markdown("### 🔑 Keywords")

            keywords = keyword_service.extract(
                df["feedback"].tolist(),
                top_n=10
            )

            keyword_df = pd.DataFrame(
                keywords,
                columns=["keyword", "score"]
            )

            fig2 = px.bar(
                keyword_df,
                x="keyword",
                y="score",
                text="score",
                title="Top Keywords (TF-IDF)"
            )

            st.plotly_chart(fig2, use_container_width=True)


        # -------------------------
        # TOPIC CHART
        # -------------------------
        with col3:
            st.markdown("### 🧠 Topics")

            topic_counts = df["topic"].value_counts().reset_index()
            topic_counts.columns = ["topic", "count"]

            fig3 = px.bar(
                topic_counts,
                x="topic",
                y="count",
                text="count",
                title="Topic Clusters"
            )

            st.plotly_chart(fig3, use_container_width=True)


        # =========================
        # DETAILED TABLE
        # =========================
        st.subheader("📄 Detailed Analysis Table")

        st.dataframe(
            df[[
                "feedback",
                "sentiment",
                "topic"
            ]]
        )

else:
    st.info("Upload a CSV file to begin analysis.")