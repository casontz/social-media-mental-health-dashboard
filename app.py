import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Social Media and Mental Health Dashboard",
    page_icon="📱",
    layout="wide"
)

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #EAF8FF 0%, #D7F1FF 45%, #F7FCFF 100%);
        color: #000000;
    }

    [data-testid="stSidebar"] {
        background-color: #DFF4FF !important;
    }

    /* Make ALL text dark */
    p, div, span, label, li {
        color: #000000 !important;
    }

    h1, h2, h3 {
        color: #000000 !important;
    }

    .main-title {
        background: linear-gradient(90deg, #6EC6FF, #B983FF, #FF9FCA);
        padding: 28px;
        border-radius: 22px;
        text-align: center;
        color: black;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.12);
        margin-bottom: 20px;
    }

    .main-title h1 {
        font-size: 42px;
        margin-bottom: 8px;
        color: black !important;
    }

    .main-title p {
        font-size: 18px;
        margin: 0;
        color: black !important;
    }

    .section-card {
        background-color: rgba(255,255,255,0.92);
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
        margin-bottom: 18px;
        color: black;
    }

    .small-card {
        background-color: white;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.07);
        text-align: center;
        color: black;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] * {
        color: black !important;
    }

    /* Metrics */
    .stMetric {
        background-color: white;
        padding: 14px;
        border-radius: 14px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.06);
    }

    .stMetric label,
    .stMetric div {
        color: black !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        color: black !important;
        font-weight: bold;
    }

    /* Dataframe text */
    .dataframe {
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Title
# ----------------------------
st.markdown(
    """
    <div class="main-title">
        <h1>📱 Social Media Habits & Mental Health 💭</h1>
        <p>An interactive dashboard exploring how online behaviors relate to depression, sleep, and focus.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Load data
# ----------------------------
df = pd.read_csv("smmh.csv")

df = df.rename(columns={
    "1. What is your age?": "age",
    "2. Gender": "gender",
    "3. Relationship Status": "relationship_status",
    "4. Occupation Status": "occupation_status",
    "6. Do you use social media?": "uses_social_media",
    "7. What social media platforms do you commonly use?": "platforms",
    "8. What is the average time you spend on social media every day?": "daily_social_media_time",
    "9. How often do you find yourself using Social media without a specific purpose?": "purposeless_use",
    "10. How often do you get distracted by Social media when you are busy doing something?": "social_media_distraction",
    "11. Do you feel restless if you haven't used Social media in a while?": "restlessness",
    "12. On a scale of 1 to 5, how easily distracted are you?": "easily_distracted",
    "13. On a scale of 1 to 5, how much are you bothered by worries?": "worry_level",
    "14. Do you find it difficult to concentrate on things?": "concentration_difficulty",
    "15. On a scale of 1-5, how often do you compare yourself to other successful people through the use of social media?": "social_comparison",
    "16. Following the previous question, how do you feel about these comparisons, generally speaking?": "comparison_feelings",
    "17. How often do you look to seek validation from features of social media?": "validation_seeking",
    "18. How often do you feel depressed or down?": "depression_score",
    "19. On a scale of 1 to 5, how frequently does your interest in daily activities fluctuate?": "interest_fluctuation",
    "20. On a scale of 1 to 5, how often do you face issues regarding sleep?": "sleep_issues"
})

time_order = [
    "Less than an Hour",
    "Between 1 and 2 hours",
    "Between 2 and 3 hours",
    "Between 3 and 4 hours",
    "Between 4 and 5 hours",
    "More than 5 hours"
]

palette = ["#FF6B6B", "#FFD93D", "#6BCB77", "#4D96FF", "#B983FF", "#FF9F1C"]

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.title("🎛️ Explore the Data")

st.sidebar.markdown("Use these filters to see how patterns change across groups.")

time_filter = st.sidebar.multiselect(
    "⏰ Daily social media time",
    options=time_order,
    default=time_order
)

gender_filter = st.sidebar.multiselect(
    "👥 Gender",
    options=sorted(df["gender"].dropna().unique()),
    default=sorted(df["gender"].dropna().unique())
)

occupation_filter = st.sidebar.multiselect(
    "🎓 Occupation status",
    options=sorted(df["occupation_status"].dropna().unique()),
    default=sorted(df["occupation_status"].dropna().unique())
)

age_min = int(df["age"].min())
age_max = int(df["age"].max())

age_range = st.sidebar.slider(
    "🎂 Age range",
    min_value=age_min,
    max_value=age_max,
    value=(age_min, age_max)
)

show_data = st.sidebar.checkbox("📄 Show filtered data table", value=False)

filtered_df = df[
    (df["daily_social_media_time"].isin(time_filter)) &
    (df["gender"].isin(gender_filter)) &
    (df["occupation_status"].isin(occupation_filter)) &
    (df["age"].between(age_range[0], age_range[1]))
]

if filtered_df.empty:
    st.warning("⚠️ No data matches these filters. Try selecting more options in the sidebar.")
    st.stop()

# ----------------------------
# Overview Metrics
# ----------------------------
st.markdown("## 🌟 Dashboard Snapshot")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Responses", len(filtered_df))

with m2:
    st.metric("Avg Depression", round(filtered_df["depression_score"].mean(), 2))

with m3:
    st.metric("Avg Sleep Issues", round(filtered_df["sleep_issues"].mean(), 2))

with m4:
    st.metric("Avg Concentration Difficulty", round(filtered_df["concentration_difficulty"].mean(), 2))

if show_data:
    st.markdown("### 📄 Filtered Data Preview")
    st.dataframe(filtered_df)

st.markdown(
    """
    <div class="section-card">
    <h3>🧭 How to Use This Dashboard</h3>
    <p>
    Use the sidebar filters to narrow the survey responses by social media time, gender,
    occupation, and age. Hover over charts to view exact values. The charts update together,
    making it easier to compare mental health patterns across different groups.
    </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Chart settings
# ----------------------------
selection = alt.selection_point(
    fields=["daily_social_media_time"],
    bind="legend"
)

# ----------------------------
# Section 1
# ----------------------------
st.markdown("## ⏰ Daily Social Media Time")

with st.expander("💡 What does this section show?"):
    st.write(
        "These charts compare daily social media time with average depression and sleep issue scores. "
        "They help show whether heavier social media users report higher mental health concerns."
    )

chart1 = alt.Chart(filtered_df).mark_line(
    point=True,
    strokeWidth=5
).encode(
    x=alt.X(
        "daily_social_media_time:N",
        sort=time_order,
        title="Daily Social Media Time",
        axis=alt.Axis(labelAngle=-35)
    ),
    y=alt.Y("mean(depression_score):Q", title="Average Depression Score"),
    color=alt.Color(
        "daily_social_media_time:N",
        scale=alt.Scale(range=palette),
        title="Daily Social Media Time"
    ),
    opacity=alt.condition(selection, alt.value(1), alt.value(0.25)),
    tooltip=[
        alt.Tooltip("daily_social_media_time:N", title="Daily Time"),
        alt.Tooltip("mean(depression_score):Q", title="Avg Depression", format=".2f")
    ]
).add_params(
    selection
).properties(
    title="💭 Average Depression Score by Daily Social Media Time",
    width=650,
    height=400
)

chart2 = alt.Chart(filtered_df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
    x=alt.X(
        "daily_social_media_time:N",
        sort=time_order,
        title="Daily Social Media Time",
        axis=alt.Axis(labelAngle=-35)
    ),
    y=alt.Y("mean(sleep_issues):Q", title="Average Sleep Issues Score"),
    color=alt.Color(
        "daily_social_media_time:N",
        scale=alt.Scale(range=palette),
        legend=None
    ),
    tooltip=[
        alt.Tooltip("daily_social_media_time:N", title="Daily Time"),
        alt.Tooltip("mean(sleep_issues):Q", title="Avg Sleep Issues", format=".2f")
    ]
).properties(
    title="😴 Average Sleep Issues by Daily Social Media Time",
    width=650,
    height=400
)

col1, col2 = st.columns(2)
with col1:
    st.altair_chart(chart1, use_container_width=True)
with col2:
    st.altair_chart(chart2, use_container_width=True)

# ----------------------------
# Section 2
# ----------------------------
st.markdown("## 🪞 Social Comparison & Validation")

with st.expander("💡 What does this section show?"):
    st.write(
        "This section looks at emotional behaviors on social media, especially comparison and validation seeking. "
        "These behaviors may be more meaningful than time spent online alone."
    )

chart3 = alt.Chart(filtered_df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
    x=alt.X("social_comparison:O", title="Social Comparison Score"),
    y=alt.Y("mean(depression_score):Q", title="Average Depression Score"),
    color=alt.Color(
        "social_comparison:O",
        scale=alt.Scale(range=palette),
        legend=None
    ),
    tooltip=[
        alt.Tooltip("social_comparison:O", title="Social Comparison"),
        alt.Tooltip("mean(depression_score):Q", title="Avg Depression", format=".2f")
    ]
).properties(
    title="🪞 Depression Score by Social Comparison Frequency",
    width=650,
    height=400
)

chart4 = alt.Chart(filtered_df).mark_line(
    point=True,
    strokeWidth=5
).encode(
    x=alt.X("validation_seeking:O", title="Validation Seeking Score"),
    y=alt.Y("mean(depression_score):Q", title="Average Depression Score"),
    color=alt.value("#B983FF"),
    tooltip=[
        alt.Tooltip("validation_seeking:O", title="Validation Seeking"),
        alt.Tooltip("mean(depression_score):Q", title="Avg Depression", format=".2f")
    ]
).properties(
    title="💜 Validation Seeking and Average Depression Score",
    width=650,
    height=400
)

col3, col4 = st.columns(2)
with col3:
    st.altair_chart(chart3, use_container_width=True)
with col4:
    st.altair_chart(chart4, use_container_width=True)

# ----------------------------
# Section 3
# ----------------------------
st.markdown("## 🧠 Focus, Restlessness, and Sleep")

with st.expander("💡 What does this section show?"):
    st.write(
        "These charts focus on how social media may relate to attention and sleep. "
        "They compare distraction with concentration difficulty and restlessness with sleep issues."
    )

chart5 = alt.Chart(filtered_df).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
    x=alt.X("social_media_distraction:O", title="Social Media Distraction Score"),
    y=alt.Y("mean(concentration_difficulty):Q", title="Average Concentration Difficulty"),
    color=alt.Color(
        "social_media_distraction:O",
        scale=alt.Scale(range=palette),
        legend=None
    ),
    tooltip=[
        alt.Tooltip("social_media_distraction:O", title="Distraction Score"),
        alt.Tooltip("mean(concentration_difficulty):Q", title="Avg Concentration Difficulty", format=".2f")
    ]
).properties(
    title="🎯 Concentration Difficulty by Social Media Distraction",
    width=650,
    height=400
)

chart6 = alt.Chart(filtered_df).mark_line(
    point=True,
    strokeWidth=5
).encode(
    x=alt.X("restlessness:O", title="Restlessness Without Social Media"),
    y=alt.Y("mean(sleep_issues):Q", title="Average Sleep Issues Score"),
    color=alt.value("#FF9F1C"),
    tooltip=[
        alt.Tooltip("restlessness:O", title="Restlessness"),
        alt.Tooltip("mean(sleep_issues):Q", title="Avg Sleep Issues", format=".2f")
    ]
).properties(
    title="🌙 Sleep Issues by Restlessness Without Social Media",
    width=650,
    height=400
)

col5, col6 = st.columns(2)
with col5:
    st.altair_chart(chart5, use_container_width=True)
with col6:
    st.altair_chart(chart6, use_container_width=True)

# ----------------------------
# Takeaways
# ----------------------------
st.markdown("## 📝 Key Takeaways")

st.markdown(
    """
    <div class="section-card">
    <ul>
        <li>💭 Daily social media time can be compared with depression and sleep issue scores.</li>
        <li>🪞 Social comparison and validation seeking appear useful for exploring emotional well-being.</li>
        <li>🎯 Social media distraction is connected to concentration difficulty.</li>
        <li>🌙 Restlessness without social media may be related to sleep issues.</li>
        <li>🎛️ Filters make it easier to compare different groups of respondents.</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True
)