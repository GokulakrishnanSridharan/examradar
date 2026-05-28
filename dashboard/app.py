import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.database import get_connection

def load_data():
    conn = get_connection()
    query = """
        SELECT 
            source,
            exam_name,
            apply_last_date,
            exam_date,
            notification_url,
            scraped_at
        FROM exams
        ORDER BY apply_last_date ASC
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# page config
st.set_page_config(
    page_title="ExamRadar",
    page_icon="🎯",
    layout="wide"
)

# title
st.title("🎯 ExamRadar")
st.markdown("**Never miss a government exam deadline again**")
st.divider()

# load data
df = load_data()

# convert dates — keep raw for filtering, formatted for display
df["apply_last_date_raw"] = pd.to_datetime(df["apply_last_date"])
df["exam_date_raw"] = pd.to_datetime(df["exam_date"])
df["apply_last_date"] = df["apply_last_date_raw"].dt.strftime("%d %b %Y")
df["exam_date"] = df["exam_date_raw"].dt.strftime("%d %b %Y")
today = pd.Timestamp.today()

# filtering uses raw dates
upcoming = df[df["apply_last_date_raw"] >= today]
closing_soon = df[
    (df["apply_last_date_raw"] >= today) &
    (df["apply_last_date_raw"] <= today + pd.Timedelta(days=30))
]

# metrics row
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Exams Tracked", len(df))

with col2:
    st.metric("Open for Application", len(upcoming))

with col3:
    st.metric("Closing in 30 Days", len(closing_soon))

st.divider()

st.divider()

# bar chart — exams by source
st.subheader("Exams by Source")
source_counts = df.groupby("source").size().reset_index(name="count")
st.bar_chart(source_counts.set_index("source")["count"])

# filters
st.subheader("Filter Exams")
sources = ["All"] + list(upcoming["source"].unique())
selected_source = st.selectbox("Select Source", sources)

if selected_source != "All":
    filtered_df = upcoming[upcoming["source"] == selected_source]
else:
    filtered_df = upcoming

# calculate days remaining
filtered_df = filtered_df.copy()
filtered_df["days_remaining"] = (filtered_df["apply_last_date_raw"] - today).dt.days

# display table with enhanced information
st.subheader("📋 Open Exams")
st.markdown(f"*Showing {len(filtered_df)} exams open for application*")

display_df = filtered_df[[
    "source",
    "exam_name",
    "apply_last_date",
    "days_remaining",
    "exam_date",
    "notification_url"
]].rename(columns={
    "source": "Source",
    "exam_name": "Exam Name",
    "apply_last_date": "Last Date to Apply",
    "days_remaining": "Days Remaining",
    "exam_date": "Exam Date",
    "notification_url": "Official Link"
})

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# closing soon warning
if len(closing_soon) > 0:
    st.divider()
    st.subheader("⚠️ Closing Soon — Apply Now")
    for _, row in closing_soon.iterrows():
        days_left = (row["apply_last_date_raw"] - today).days
        st.warning(
            f"**{row['exam_name']}** — {days_left} days left to apply | "
            f"[Official Link]({row['notification_url']})"
        )