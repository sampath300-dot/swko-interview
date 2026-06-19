import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

st.set_page_config(
    page_title="SWKO Interview",
    layout="wide"
)

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background:#0B1120;
}

.block-container{
    max-width:900px;
    padding-top:2rem;
}

[data-testid="InputInstructions"]{
    display:none;
}

.hero{
    text-align:center;
    margin-bottom:30px;
}

.hero-title{
    font-size:58px;
    font-weight:700;
    color:white;
}

.hero-subtitle{
    font-size:18px;
    color:#94A3B8;
    margin-top:10px;
}

div[data-testid="stButton"] > button{
    width:100%;
    height:55px;
    border-radius:12px;
    font-size:17px;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-title">
        SWKO Interview
    </div>

    <div class="hero-subtitle">
        Practice smarter for your next interview.
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    role = st.text_input(
        "Role",
        placeholder="AI Engineer, Data Scientist, Frontend Developer",
        label_visibility="collapsed"
    )

with col2:
    level = st.selectbox(
        "Experience",
        ["Beginner", "Intermediate", "Advanced"]
    )

questions_count = st.number_input(
    "Number of Questions",
    min_value=5,
    max_value=25,
    value=10,
    step=1
)

generate = st.button(
    "Generate Interview Questions",
    use_container_width=True
)

if generate:

    if role.strip() == "":
        st.warning("Please enter a role.")
        st.stop()

    prompt = f"""
Generate {questions_count} interview questions for a {level} level {role}.

Include:
- Technical Questions
- Project Questions
- Scenario Based Questions

Format neatly with numbering.
"""

    try:

        with st.spinner("Generating Questions..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )

        st.markdown("## Interview Questions")

        with st.container(border=True):
            st.markdown(response.text)

    except Exception as e:

        if "429" in str(e):
            st.error(
                "Daily API limit reached. Please try again later."
            )
        else:
            st.error(f"Error: {e}")

if st.button("Clear"):
    st.rerun()
