# 🧠 MathMind – LLM-Powered Math & Knowledge Assistant

MathMind is an interactive Streamlit application that transforms natural language queries into intelligent solutions. Whether it's solving complex math problems, answering logic-based questions, or searching concepts using Wikipedia — **MathMind combines the power of Groq's Gemma 2 LLM and LangChain Agents** to deliver accurate, step-by-step results.

![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-Framework-blueviolet)
![Built with Groq](https://img.shields.io/badge/Gemma%202-9b--Instruct-yellow?logo=groq)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Features

🔢 **Text to Math Solver**  
Enter natural language math problems. MathMind parses and solves them step-by-step using `LLMMathChain`.

🧠 **Reasoning Engine**  
Handles word problems, logic questions, and arithmetic breakdowns using custom LangChain prompts.

🌐 **Wikipedia Integration**  
Fetch real-time, reliable information from Wikipedia using built-in tools.

🧠 **LangChain Tool Agent**  
Uses LangChain’s `initialize_agent()` to choose between:
- `Calculator` (LLMMathChain)
- `Wikipedia Search`
- `Reasoning Tool` (LLMChain with custom prompt)

💬 **Streamlit Chat UI**  
Clean and interactive chat interface for seamless user experience.

---

## 🧰 Tech Stack

- **LangChain** – Core framework for agents & tools  
- **Groq (Gemma 2-9b-Instruct)** – LLM for blazing-fast inference  
- **Streamlit** – Frontend & user interface  
- **LangChain Tools** – LLMMathChain, WikipediaAPIWrapper, PromptTemplate  
- **Python-dotenv** – For local environment variable handling

---

## 📦 Project Structure

