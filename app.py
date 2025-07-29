import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import re
import json
import requests
import pandas as pd # Import pandas for tabular data display

# Load environment variables from .env file (for local development)
load_dotenv()

# --- Lottie Animation Function (Cleaned & Robust) ---
def load_lottiefile(filepath: str):
    """Loads a Lottie animation JSON from a given filepath (URL or local).
    Returns None silently if loading fails to prevent UI error messages.
    """
    try:
        if filepath.startswith("http"):
            response = requests.get(filepath)
            response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
            return response.json()
        else:
            with open(filepath, "r") as f:
                return json.load(f)
    except Exception: # Catch any exception silently (e.g., FileNotFoundError, JSONDecodeError, requests.exceptions.RequestException)
        return None

# --- Configuration and Model Initialization ---
st.set_page_config(
    page_title="QuizCraft AI", # Cute Gen AI Name
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="auto"
)

# Custom CSS for a modern, AI-look with a Brighter Blueish Theme ("Clean Sky AI")
st.markdown("""
    <style>
    .main {
        background-color: #E0F2F7; /* Very Light Sky Blue background */
        color: #1A2B3C; /* Dark Navy/Charcoal for general text */
        font-family: 'Inter', 'Roboto', sans-serif; /* Modern, clean font */
    }
    /* Styling for text input areas and text areas */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #FFFFFF; /* Pure White for maximum readability */
        color: #1A2B3C; /* Dark text */
        border: 1px solid #ADD8E6; /* Light Steel Blue border */
        border-radius: 8px;
        padding: 10px;
    }
    /* Styling for primary action button */
    .stButton > button {
        background-color: #007BFF; /* Standard Blue for action button */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #0056B3; /* Darker blue on hover */
    }
    /* Styling for expander components */
    .stExpander {
        background-color: #FFFFFF; /* Consistent component background */
        border-radius: 8px;
        border: 1px solid #ADD8E6;
        margin-bottom: 10px;
    }
    .stExpander > div > div > p {
        color: #1A2B3C; /* Dark text for expander content */
    }
    /* Styling for all headings */
    h1, h2, h3, h4, h5, h6 {
        color: #0056B3; /* A slightly darker, professional blue for headings */
    }
    /* Styling for alerts (success, warning, error) */
    .stAlert {
        border-radius: 8px;
    }
    /* Style for the dataframe component */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden; /* Ensures rounded corners apply to content */
    }
    .stDataFrame table {
        background-color: #FFFFFF; /* Consistent component background */
        color: #1A2B3C; /* Dark text for readability */
        border-collapse: collapse;
        width: 100%;
    }
    .stDataFrame th {
        background-color: #007BFF; /* Standard Blue for table headers */
        color: white; /* White text on blue header */
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid #ADD8E6;
    }
    .stDataFrame td {
        padding: 10px;
        border-bottom: 1px solid #ADD8E6;
    }
    .stDataFrame tbody tr:hover {
        background-color: #F0F8FF; /* Very light blue on hover */
    }
    /* Style for tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #FFFFFF; /* Inactive tab background */
        border-radius: 8px 8px 0 0;
        color: #1A2B3C; /* Inactive tab text color */
        font-size: 18px;
        padding: 10px 20px;
        border: 1px solid #ADD8E6;
        border-bottom: none;
    }
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: #F0F8FF; /* Lighter on hover */
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #007BFF; /* Active tab background color */
        color: white; /* Active tab text color */
        border-color: #007BFF;
        border-bottom: 1px solid #007BFF; /* Keep bottom border for active tab */
    }
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #FFFFFF; /* Content panel background */
        border: 1px solid #ADD8E6;
        border-radius: 0 0 8px 8px;
        padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize the Gemini model
@st.cache_resource
def initialize_gemini_model():
    """
    Initializes the Google Gemini Flash model using LangChain.
    Retrieves the API key from environment variables (or Streamlit secrets in deployment).
    """
    try:
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            st.error("GOOGLE_API_KEY environment variable not set. Please set it in your .env file or Streamlit secrets.")
            return None
        
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=google_api_key, temperature=0.8)
        st.success("Gemini model initialized successfully using gemini-1.5-flash!")
        return llm
    except Exception as e:
        st.error(f"Error initializing Gemini model: {e}. Please ensure your API key is valid and check your internet connection.")
        return None

llm = initialize_gemini_model()

# --- Core Logic Functions ---

def split_content(content, max_tokens=2000): 
    """Splits the input content into smaller chunks for LLM processing."""
    words = content.split()
    chunks = []
    current_chunk = []
    current_token_count = 0
    
    for word in words:
        token_count = 1 
        # FIX: Corrected typo from token_token_count to current_token_count
        if current_token_count + token_count <= max_tokens:
            current_chunk.append(word)
            current_token_count += token_count
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_token_count = token_count

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    st.sidebar.info(f"Content split into {len(chunks)} chunk(s).")
    return chunks


def parse_mcq_response(response):
    """Parses the raw text response from the LLM to extract structured MCQ data."""
    if not response or len(response.strip()) == 0:
        return None, "The model's response is empty or invalid."

    lines = response.strip().split("\n")
    formatted_questions = []
    current_question = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue

        question_match = re.match(r"^\d+\.\s*(.*)", line)
        if question_match:
            if current_question and "question_text" in current_question and \
               "options" in current_question and "answer" in current_question and \
               len(current_question["options"]) == 4:
                formatted_questions.append(current_question)
            current_question = {}
            current_question["question_text"] = question_match.group(1).strip()
            current_question["options"] = {}
        
        option_match = re.match(r"^([A-D])\.\s*(.*)", line)
        if option_match and "options" in current_question:
            key, value = option_match.groups()
            current_question["options"][key] = value.strip()
        
        answer_match = re.match(r"^Answer:\s*([A-D])", line, re.IGNORECASE)
        if answer_match:
            if "question_text" in current_question and "options" in current_question:
                current_question["answer"] = answer_match.group(1).upper()
                if len(current_question["options"]) == 4:
                    formatted_questions.append(current_question)
                    current_question = {}

    if current_question and "question_text" in current_question and \
       "options" in current_question and "answer" in current_question and \
       len(current_question["options"]) == 4:
        formatted_questions.append(current_question)

    if not formatted_questions:
        return None, "No valid questions were extracted from the model's response. Raw response was:\n" + response

    final_questions = []
    for idx, q in enumerate(formatted_questions):
        q["question_number"] = idx + 1
        final_questions.append(q)

    return {"questions": final_questions}, None


def generate_mcqs(content):
    """Generates MCQs from the provided content using the Gemini model."""
    if llm is None:
        return {"error": "Gemini model not initialized. Please check API key and configuration."}

    try:
        chunks = split_content(content)
        all_mcqs_raw_list = [] 
        
        for i, chunk in enumerate(chunks):
            prompt = f"""
Generate exactly 3 multiple-choice questions (MCQs) based on the following content.
Each MCQ should have:
1. A question in proper format, starting with a number (e.g., "1. What is...?").
2. Four distinct answer choices labeled as A, B, C, and D.
3. The correct answer labeled as "Answer: (X)" at the end, where X is A, B, C, or D.

Ensure proper formatting, and do NOT include any introductory or concluding remarks, or unnecessary text.
The output should only contain the questions, options, and answers, formatted as described.

Content:
{chunk}

Example of desired format for one MCQ:
1. What is Machine Learning?
   A. A type of AI that learns from data
   B. A software tool for automation
   C. A manual process of decision-making
   D. A type of cloud computing
   Answer: A

Now generate 3 MCQs based on the provided content:
"""
            st.sidebar.text(f"Processing chunk {i+1}/{len(chunks)}...")
            
            response_message = llm.invoke([HumanMessage(content=prompt)])
            response = response_message.content 

            mcq_data, error = parse_mcq_response(response)

            if error:
                st.warning(f"Error parsing response for chunk {i+1}: {error}")
            else:
                all_mcqs_raw_list.append(mcq_data)

        final_mcqs = {"questions": []}
        for chunk_result in all_mcqs_raw_list:
            if "questions" in chunk_result:
                for q in chunk_result["questions"]:
                    final_mcqs["questions"].append(q)

        if not final_mcqs["questions"]:
            return {"error": "No valid MCQs could be generated from the provided content across all chunks. Please try different content."}

        return final_mcqs

    except Exception as e:
        return {"error": f"An error occurred during MCQ generation: {str(e)}. Please check your input and API key."}

# --- Streamlit UI Layout ---

st.title("🧠 QuizCraft AI") # App Title
st.markdown("""
    Generate multiple-choice questions from any text using Google Gemini's powerful AI.
    Perfect for students, teachers, and anyone looking to quickly create quizzes!
""")

# Lottie animation configuration (robust, silent on failure)
lottie_animation_path = "ai_brain_animation.json" # Local file name (download and place this in your project)
lottie_animation_url_fallback = "https://lottie.host/171501b4-1f79-425f-832f-763435164f26/w2C5Q6F05v.json" 

try:
    from streamlit_lottie import st_lottie
    
    st_lottie_animation_json = load_lottiefile(lottie_animation_path)
    if not st_lottie_animation_json: # If local load failed, try URL
        st_lottie_animation_json = load_lottiefile(lottie_animation_url_fallback)

    if st_lottie_animation_json:
        st_lottie(st_lottie_animation_json, height=200, key="ai_brain_animation")
except ImportError:
    st.warning("Install `streamlit-lottie` for animations: `pip install streamlit-lottie`")
except Exception:
    pass # Catch any other unexpected error silently


st.markdown("---")

# --- Tab Bar Implementation ---
tab_generate, tab_about = st.tabs(["Generate MCQs", "About This Project"])

with tab_generate:
    user_content = st.text_area(
        "Paste your content here:",
        height=300,
        placeholder="E.g., 'Machine learning is a subset of artificial intelligence that focuses on the development of algorithms that allow computers to learn from data. Instead of being explicitly programmed, these algorithms enable the machine to identify patterns and make predictions based on the data it has been trained on. Key areas include supervised, unsupervised, and reinforcement learning.'"
    )

    if st.button("Generate MCQs"):
        if not user_content:
            st.warning("Please enter some content to generate MCQs.")
        elif llm is None:
            st.error("Model not initialized. Please ensure your API key is correctly set.")
        else:
            with st.spinner("Generating MCQs... This might take a moment, especially for longer texts."):
                mcq_result = generate_mcqs(user_content)
                
                if "error" in mcq_result:
                    st.error(mcq_result["error"])
                elif mcq_result and mcq_result["questions"]:
                    st.success("MCQs generated successfully!")
                    
                    questions_for_df = []
                    answers_for_df = []
                    for mcq in mcq_result["questions"]:
                        questions_for_df.append({
                            "Q#": mcq['question_number'],
                            "Question": mcq['question_text'],
                            "A": mcq['options'].get('A', ''),
                            "B": mcq['options'].get('B', ''),
                            "C": mcq['options'].get('C', ''),
                            "D": mcq['options'].get('D', '')
                        })
                        answers_for_df.append({
                            "Q#": mcq['question_number'],
                            "Answer": f"{mcq['answer']}. {mcq['options'].get(mcq['answer'], 'N/A')}"
                        })
                    
                    df_questions = pd.DataFrame(questions_for_df)
                    df_answers = pd.DataFrame(answers_for_df)

                    st.subheader("Generated Questions:")
                    st.dataframe(df_questions, hide_index=True, use_container_width=True)

                    with st.expander("Show All Answers"):
                        st.subheader("Answers:")
                        st.dataframe(df_answers, hide_index=True, use_container_width=True)
                    
                else:
                    st.info("No MCQs could be generated. Please try with different content or check the model's response for issues.")

with tab_about:
    st.markdown("### About this Project & Key ML/Generative AI Topics:")
    st.markdown("""
    This application demonstrates the practical application of modern AI capabilities.
    Here are the key Machine Learning and Generative AI concepts and techniques you've learned and applied:

    * **Generative AI**: The core of this project. You are using a **Generative AI model** (Google Gemini) to create new, original content (multiple-choice questions) from provided text. This highlights the ability to leverage pre-trained models for complex content creation tasks.
    * **Large Language Models (LLMs)**: Gemini is a powerful **Large Language Model**. You've learned how to interact with and leverage the capabilities of a pre-trained LLM for a specific task (MCQ generation).
    * **Prompt Engineering**: This project heavily relies on **Prompt Engineering**. You've learned to craft precise and effective instructions (the "prompt") to guide the LLM to generate output in a very specific format (numbered questions, labeled options, explicit answers). This skill is critical for getting desired results from LLMs.
    * **Natural Language Processing (NLP)**:
        * **Text Preprocessing / Chunking**: The `split_content` function demonstrates a basic form of **text preprocessing** by breaking down large input texts into manageable chunks. This is essential for handling documents that exceed an LLM's context window.
        * **Information Extraction**: The `parse_mcq_response` function performs **information extraction** from the LLM's raw text output. By using regular expressions, you're programmatically identifying and structuring specific pieces of information (questions, options, correct answers) from free-form text.
    * **API Integration**: You've gained practical experience in **API integration** by connecting your application to the Google Gemini API via the LangChain framework. This is a crucial skill for building real-world AI applications that consume external services.
    * **Web Application Development & Deployment (Streamlit)**: You've learned to build a user-friendly web interface using Streamlit, which simplifies the process of creating interactive applications and makes **deployment** straightforward. This demonstrates your ability to take an AI model and make it accessible to users.
    * **Error Handling**: The code includes `try-except` blocks and conditional checks to handle potential issues like API key errors, empty responses, or parsing failures, which is vital for building robust applications.

    This project showcases your ability to not just use an AI model, but to engineer a complete solution around it, from data preparation and prompt design to output parsing and user interface development.
    """)