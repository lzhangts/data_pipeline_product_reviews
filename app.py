import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/reviews_products_with_sentiment.csv")

df = load_data()

st.set_page_config(
    page_title="Product Reviews Insights",
    layout="wide"
)

st.title("📊 Product Reviews Insights: Sentiment, Ratings & Sales")
st.caption("Powered by ETL Pipeline + DistilBERT Sentiment Model")

# ---------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------
st.sidebar.header("Filters")

# Sentiment filter
sentiments = df["sentiment"].unique().tolist()
sentiment_filter = st.sidebar.multiselect(
    "Sentiment",
    options=sentiments,
    default=sentiments
)

# Category filter (if exists)
if "category" in df.columns:
    categories = df["category"].dropna().unique().tolist()
    category_filter = st.sidebar.multiselect(
        "Category",
        options=categories,
        default=categories
    )
else:
    category_filter = None

# Price range filter (if exists)
if "price" in df.columns:
    min_price, max_price = float(df["price"].min()), float(df["price"].max())
    price_range = st.sidebar.slider(
        "Price Range",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price)
    )
else:
    price_range = None

# ---------------------------------------------------------
# Apply filters
# ---------------------------------------------------------
filtered_df = df.copy()

filtered_df = filtered_df[filtered_df["sentiment"].isin(sentiment_filter)]

if category_filter:
    filtered_df = filtered_df[filtered_df["category"].isin(category_filter)]

if price_range:
    filtered_df = filtered_df[
        (filtered_df["price"] >= price_range[0]) &
        (filtered_df["price"] <= price_range[1])
    ]

# ---------------------------------------------------------
# KPI Metrics
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Reviews", len(filtered_df))

with col2:
    st.metric("Products", filtered_df["product_id"].nunique())

with col3:
    positivity = (filtered_df["sentiment"] == "POSITIVE").mean() * 100
    st.metric("Positivity %", f"{positivity:.1f}%")

with col4:
    st.metric("Avg confidence", f"{filtered_df['confidence'].mean():.2f}")

st.markdown("---")

# ---------------------------------------------------------
# Sentiment Distribution Chart
# ---------------------------------------------------------
st.subheader("Sentiment Distribution")

sent_count = filtered_df["sentiment"].value_counts().reset_index()
sent_count.columns = ["sentiment", "count"]

fig = px.bar(
    sent_count,
    x="sentiment",
    y="count",
    color="sentiment",
    color_discrete_map={"POSITIVE": "#2ecc71", "NEGATIVE": "#e74c3c"},
    title="Sentiment Distribution",
    text="count"
)

fig.update_layout(showlegend=False)
fig.update_traces(textposition="outside")

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# Show data table
# ---------------------------------------------------------
with st.expander("Show underlying data"):
    st.dataframe(filtered_df)