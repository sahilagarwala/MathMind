import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import Tool
from langchain.callbacks import StreamlitCallbackHandler

# Load environment variable
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Set up Streamlit page
st.set_page_config(page_title="Text to Math Problem Solver", page_icon="🧮")
st.title("Text To Math Problem Solver Using Google Gemma 2")

# Check API key
if not groq_api_key:
    st.error("🚫 Please set your GROQ_API_KEY in the .env file.")
    st.stop()

# Initialize LLM
llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# -------------------- TOOL 1: Calculator --------------------
math_chain = LLMMathChain.from_llm(llm=llm)
calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="Solves direct mathematical expressions like 34 * (5 + 2)."
)

# -------------------- TOOL 2: Wikipedia --------------------
wikipedia_wrapper = WikipediaAPIWrapper()
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia_wrapper.run,
    description="Fetches general knowledge from Wikipedia."
)

# -------------------- TOOL 3: Reasoning Tool --------------------
reasoning_prompt = PromptTemplate(
    input_variables=["question"],
    template="""
You are a smart assistant solving real-world logic and math word problems. Follow these steps:
1. Extract all quantities and operations from the question.
2. Perform the steps in order.
3. Clearly state the final answer.

Example 1:
Q: I had 3 pens. I bought 2 more and gave away 1. How many pens do I have?
A:
- Start with 3 pens.
- Bought 2 → 3 + 2 = 5
- Gave away 1 → 5 - 1 = 4
Final Answer: 4 pens

Example 2:
Q: I bought 12 apples and ate 3. Then I bought 6 more. How many apples do I have?
A:
- Bought 12 apples
- Ate 3 → 12 - 3 = 9
- Bought 6 → 9 + 6 = 15
Final Answer: 15 apples

Now solve:
Q: {question}
A:
"""
)
reasoning_chain = LLMChain(llm=llm, prompt=reasoning_prompt)
reasoning_tool = Tool(
    name="Reasoning Tool",
    func=reasoning_chain.run,
    description="Solves real-world word problems with logical steps."
)

# -------------------- TOOL ROUTER (Classifier) --------------------
tool_router_prompt = PromptTemplate(
    input_variables=["question"],
    template="""
Classify the user's question into one of the following:
- "math" → for direct arithmetic expressions (e.g., 34 * (5 + 2))
- "reasoning" → for logic-based word problems (e.g., I had 4 apples...)
- "wiki" → for factual/general questions (e.g., Who is Einstein?)

Return only one word: math, reasoning, or wiki.

Question: {question}
Classification:
"""
)
tool_selector = LLMChain(llm=llm, prompt=tool_router_prompt)

# -------------------- Session State --------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a Math assistant! Ask me a question."}
    ]

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# -------------------- User Input --------------------
question = st.text_area("Enter your question:")

if st.button("Find My Answer"):
    if question:
        with st.spinner("Thinking..."):
            st.session_state["messages"].append({"role": "user", "content": question})
            st.chat_message("user").write(question)

            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)

            tool_type = tool_selector.run({"question": question}).strip().lower()
            st.info(f"🔧 Tool selected: **{tool_type}**")

            if tool_type == "math":
                response = calculator.run(question)
            elif tool_type == "reasoning":
                response = reasoning_tool.run(question)
            elif tool_type == "wiki":
                response = wikipedia_tool.run(question)
            else:
                response = "Sorry, I couldn't classify your question type."

            st.session_state["messages"].append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)
            st.success(response)
    else:
        st.warning("Please enter a question.")
