# 🧠 QuizCraft AI

![QuizCraft AI Logo/Banner](https://placehold.co/600x200/0A192F/E6F1FF?text=QuizCraft+AI) 
*(You can replace this placeholder with a custom banner or logo for your app!)*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_STREAMLIT_APP_URL_HERE)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Overview

**QuizCraft AI** is an intelligent web application designed to effortlessly generate multiple-choice questions (MCQs) from any given text. Leveraging the power of Google's state-of-the-art Gemini Large Language Model, it's a perfect tool for students, educators, and content creators looking to quickly create quizzes and test comprehension.

Say goodbye to manual question creation – simply paste your content, and let QuizCraft AI do the rest!

## 🚀 Features

* **AI-Powered MCQ Generation:** Generates relevant and diverse MCQs from arbitrary text content.
* **Google Gemini Integration:** Utilizes the advanced `gemini-1.5-flash` model for high-quality question generation.
* **Structured Output:** Presents questions with four distinct options and a clear answer key in a user-friendly tabular format.
* **Interactive Answers:** Answers are hidden by default and can be revealed with a single click, perfect for self-testing.
* **Clean & Modern UI:** Built with Streamlit, featuring a sleek "Brighter Deep Ocean" blueish theme for an intuitive user experience.
* **Responsive Design:** Adapts seamlessly to various screen sizes (desktop, tablet, mobile).
* **Robust Error Handling:** Provides clear feedback for API issues, input problems, or generation failures.

## 💡 How It Works

QuizCraft AI combines several cutting-edge technologies to deliver its functionality:

1.  **Text Preprocessing:** The input content is intelligently split into smaller chunks to efficiently interact with the LLM's token limits.
2.  **Prompt Engineering:** A carefully crafted prompt guides the Gemini model to generate MCQs in a precise, structured format.
3.  **Generative AI (Gemini):** The core AI engine that understands the input text and generates new, relevant questions and options.
4.  **Information Extraction (NLP):** Regular expressions are used to parse the LLM's raw text output, extracting questions, options, and answers into a structured format.
5.  **API Integration (LangChain):** The application communicates with the Google Gemini API using the LangChain framework, simplifying the interaction with the LLM.
6.  **Web Interface (Streamlit):** Streamlit provides the interactive frontend, allowing users to easily input text and view generated quizzes.

## 🛠️ Tech Stack

* **Python**: Core programming language.
* **Google Gemini 1.5 Flash**: The Large Language Model (LLM) for generative capabilities.
* **LangChain**: Framework for interacting with LLMs and building AI applications.
* **Streamlit**: Python framework for building and deploying interactive web applications.
* **Pandas**: For efficient data manipulation and tabular display of MCQs.
* **Requests**: For handling HTTP requests (e.g., Lottie animations).
* **python-dotenv**: For secure management of API keys in local development.
* **streamlit-lottie**: For integrating dynamic Lottie animations.

## 🌐 Live Demo

Experience QuizCraft AI live on Streamlit Community Cloud:

👉 **[Launch QuizCraft AI App](YOUR_STREAMLIT_APP_URL_HERE)** 👈

*(Remember to replace `YOUR_STREAMLIT_APP_URL_HERE` with the actual URL after deployment.)*

## ⚙️ Local Setup and Installation

To run QuizCraft AI on your local machine, follow these steps:

1.  **Clone the repository (or download the files):**
    ```bash
    git clone [https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git)
    cd YOUR_REPO_NAME
    ```
    *(Replace `YOUR_GITHUB_USERNAME` and `YOUR_REPO_NAME`)*

2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows (Command Prompt):
    venv\Scripts\activate.bat
    # On Windows (PowerShell):
    .\venv\Scripts\Activate.ps1
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Obtain a Google Gemini API Key:**
    * Go to [Google AI Studio](https://aistudio.google.com/) to generate your `GOOGLE_API_KEY`.

5.  **Set your API Key securely:**
    * Create a file named `.env` in the root of your project directory (the same folder as `app.py`).
    * Add your API key to this file in the following format:
        ```
        GOOGLE_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"
        ```
        *(Replace `YOUR_ACTUAL_GEMINI_API_KEY_HERE` with your key. **Do not share this file or commit it to GitHub!**)*

6.  **Optional: Download Lottie Animation (for local reliability):**
    * Go to [LottieFiles.com](https://lottiefiles.com/), search for an animation (e.g., "brain," "AI"), download its "Lottie JSON," and save it as `ai_brain_animation.json` in your project root. This ensures the animation loads even if the public URL changes.

7.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    Your browser should automatically open the app at `http://localhost:8501`.

## 📈 Future Improvements

* **More Input Options:** Allow uploading PDF/DOCX files or fetching content from URLs.
* **Customizable MCQ Count:** Let users specify the exact number of MCQs they want.
* **Quiz Mode:** Implement an interactive quiz where users can select answers and get immediate feedback.
* **Download Options:** Enable downloading MCQs in various formats (e.g., PDF, JSON, text).
* **Difficulty Levels:** Allow users to specify the desired difficulty of questions.
* **User Feedback Loop:** Implement a system to collect user feedback on question quality to potentially fine-tune the model or prompt.

## 🤝 Contributing

Feel free to fork this repository, open issues, or submit pull requests. Any contributions are welcome!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.