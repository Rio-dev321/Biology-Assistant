
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Biology Study Assistant",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Biology Study Assistant")
st.write(
    "Enter a Biology topic and get its definition, "
    "complete explanation, examples, and a diagram."
)

st.info("Designed for students, including Class 10 learners.")

# API key from Streamlit Secrets
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = None

if not api_key:
    st.warning(
        "Please add your Groq API key in "
        "Streamlit Cloud → App Settings → Secrets."
    )
    st.stop()

client = Groq(api_key=api_key)

topic = st.text_input(
    "Enter your Biology topic",
    placeholder="Example: Photosynthesis"
)

language = st.selectbox(
    "Choose explanation language",
    ["English", "Roman Urdu", "English + Roman Urdu"]
)

level = st.selectbox(
    "Choose your study level",
    ["Class 10", "Class 9", "Beginner", "Advanced"]
)

if st.button("Generate Study Notes", type="primary"):
    if not topic.strip():
        st.warning("Please enter a Biology topic first.")
    else:
        prompt = f"""
        You are Biology Study Assistant, a helpful Biology tutor.

        Topic: {topic}
        Student level: {level}
        Language: {language}

        Create accurate, student-friendly study notes with these
        headings:

        1. Topic Introduction
        2. Complete Definition
        3. Detailed Explanation
        4. Important Points
        5. Examples from Daily Life
        6. A simple labeled diagram
        7. Diagram explanation
        8. Short Summary
        9. Five Practice Questions

        For the diagram, use a clear text-based diagram with labels
        or a simple flowchart. Explain each important label.
        Keep the content organized and easy to understand.
        If a topic is outside Biology, politely ask for a Biology topic.
        """

        try:
            with st.spinner("Preparing your Biology study notes..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an accurate, helpful Biology "
                                "teacher. Use clear headings and "
                                "student-friendly explanations."
                            )
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.4,
                    max_completion_tokens=4000
                )

                answer = response.choices[0].message.content

            st.success("Your study notes are ready!")
            st.markdown(answer)

            st.download_button(
                "Download Study Notes",
                data=answer,
                file_name="biology_study_notes.md",
                mime="text/markdown"
            )

        except Exception as e:
            st.error(
                "The AI could not generate notes. "
                "Please check your Groq API key and try again."
            )
            st.caption(f"Error details: {e}")
