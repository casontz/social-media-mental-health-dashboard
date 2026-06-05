import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Social Media and Mental Health Dashboard",
    layout="wide"
)

st.title("Social Media Habits and Mental Health Dashboard")

st.write(
    "This dashboard explores how social media behaviors relate to depression, "
    "sleep issues, concentration difficulty, and restlessness."
)

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

st.sidebar.header("Dashboard Filters")

time_filter = st.sidebar.multiselect(
    "Select daily social media time:",
    options=time_order,
    default=time_order
)

gender_filter = st.sidebar.multiselect(
    "Select gender:",
    options=sorted(df["gender"].dropna().unique()),
    default=sorted(df["gender"].dropna().unique())
)

filtered_df = df[
    (df["daily_social_media_time"].isin(time_filter)) &
    (df["gender"].isin(gender_filter))
]

st.subheader("Filtered Dataset")
st.write(f"Number of responses shown: {len(filtered_df)}")

selection = alt.selection_point(
    fields=["daily_social_media_time"],
    bind="legend"
)

chart1 = alt.Chart(filtered_df).mark_line(
    point=True,
    strokeWidth=4
).encode(
    x=alt.X("daily_social_media_time:N", sort=time_order, title="Daily Social Media Time"),
    y=alt.Y("mean(depression_score):Q", title="Average Depression Score"),
    color=alt.Color(
        "daily_social_media_time:N",
        scale=alt.Scale(range=palette),
        title="Daily Social Media Time"
    ),
    opacity=alt.condition(selection, alt.value(1), alt.value(0.25)),
    tooltip=[
        "daily_social_media_time",
        alt.Tooltip("mean(depression_score):Q", title="Avg Depression", format=".2f")
    ]
).add_params(
    selection
).properties(
    title="Average Depression Score by Daily Social Media Time",
    width=650,
    height=400
)


chart2 = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X(
        "daily_social_media_time:N",
        sort=time_order,
        title="Daily Social Media Time",
        axis=alt.Axis(labelAngle=-45)
    ),
    y=alt.Y(
        "mean(sleep_issues):Q",
        title="Average Sleep Issues Score"
    ),
    color=alt.Color(
        "daily_social_media_time:N",
        scale=alt.Scale(range=palette),
        legend=None
    ),
    tooltip=[
        "daily_social_media_time",
        alt.Tooltip("mean(sleep_issues):Q", title="Avg Sleep Issues", format=".2f")
    ]
).properties(
    title="Average Sleep Issues by Daily Social Media Time",
    width=650,
    height=400
)

col1, col2 = st.columns(2)
with col1:
    st.altair_chart(chart1, use_container_width=True)
with col2:
    st.altair_chart(chart2, use_container_width=True)

st.write(
    "These two coordinated charts allow users to compare depression and sleep issues "
    "across different daily social media usage groups."
)

chart3 = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X("social_comparison:O", title="Social Comparison Score"),
    y=alt.Y("mean(depression_score):Q", title="Average Depression Score"),
    color=alt.Color(
        "social_comparison:O",
        scale=alt.Scale(range=palette),
        legend=None
    ),
    tooltip=[
        "social_comparison",
        alt.Tooltip("mean(depression_score):Q", title="Avg Depression", format=".2f")
    ]
).properties(
    title="Depression Score by Social Comparison Frequency",
    width=650,
    height=400
)

chart4 = alt.Chart(filtered_df).mark_line(
    point=True,
    strokeWidth=4
).encode(
    x=alt.X("validation_seeking:O", title="Validation Seeking Score"),
    y=alt.Y("mean(depression_score):Q", title="Average Depression Score"),
    color=alt.value("#B983FF"),
    tooltip=[
        "validation_seeking",
        alt.Tooltip("mean(depression_score):Q", title="Avg Depression", format=".2f")
    ]
).properties(
    title="Validation Seeking and Average Depression Score",
    width=650,
    height=400
)

col3, col4 = st.columns(2)
with col3:
    st.altair_chart(chart3, use_container_width=True)
with col4:
    st.altair_chart(chart4, use_container_width=True)

chart5 = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X("social_media_distraction:O", title="Social Media Distraction Score"),
    y=alt.Y("mean(concentration_difficulty):Q", title="Average Concentration Difficulty"),
    color=alt.Color(
        "social_media_distraction:O",
        scale=alt.Scale(range=palette),
        legend=None
    ),
    tooltip=[
        "social_media_distraction",
        alt.Tooltip("mean(concentration_difficulty):Q", title="Avg Concentration Difficulty", format=".2f")
    ]
).properties(
    title="Average Concentration Difficulty by Social Media Distraction",
    width=650,
    height=400
)

chart6 = alt.Chart(filtered_df).mark_line(
    point=True,
    strokeWidth=4
).encode(
    x=alt.X("restlessness:O", title="Restlessness Without Social Media"),
    y=alt.Y("mean(sleep_issues):Q", title="Average Sleep Issues Score"),
    color=alt.value("#FF9F1C"),
    tooltip=[
        "restlessness",
        alt.Tooltip("mean(sleep_issues):Q", title="Avg Sleep Issues", format=".2f")
    ]
).properties(
    title="Restlessness Without Social Media and Sleep Issues",
    width=650,
    height=400
)

col5, col6 = st.columns(2)
with col5:
    st.altair_chart(chart5, use_container_width=True)
with col6:
    st.altair_chart(chart6, use_container_width=True)

st.subheader("Key Takeaways")

st.markdown(
    """
    - Higher daily social media use can be compared with depression and sleep issue scores.
    - Social comparison and validation seeking are useful indicators of emotional well-being.
    - Social media distraction is connected to concentration difficulty.
    - Restlessness without social media may be related to sleep issues.
    """
)