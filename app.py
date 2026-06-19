import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API Key (works locally and on Streamlit Cloud)
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    api_key = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)

# Page Config
st.set_page_config(
    page_title="SWKO Interview",
    page_icon="🎯",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background:#0B1120;
}

.block-container{
    max-width:900px;
    padding-top:2rem;
}

h1{
    text-align:center;
    color:white;
}

[data-testid="stNumberInput"]{
    color:white;
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

# Header
st.title("SWKO Interview")
st.caption("Practice smarter for your next interview.")

# Inputs
col1, col2 = st.columns(2)

with col1:
    role = st.text_input(
        "Role",
        placeholder="AI Engineer, Data Scientist, Frontend Developer"
    )

with col2:
    level = st.selectbox(
        "Experience",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
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

# Generate Questions
if generate:

    if role.strip() == "":
        st.warning("Please enter a role.")
        st.stop()

    prompt = f"""
Generate {questions_count} interview questions for a {level} level {role}.

Include:
1. Technical Questions
2. Project-Based Questions
3. Scenario-Based Questions

Format neatly with numbering.
"""

    try:

        with st.spinner("Generating Questions..."):

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )

        st.markdown("---")
        st.subheader("Interview Questions")

        st.markdown(response.text)

    except Exception as e:

        if "429" in str(e):
            st.error(
                "API limit reached. Please try again later."
            )

        else:
            st.error(f"Error: {e}")
