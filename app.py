import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

## Langsmith Tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = 'QA CHATBOT WITH OPENAI'

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant, provide the response to the user queries"),
        ("user","Question:{question}")
    ]
)

# Function to generate response
def generate_response(question,api_key,llm_model,temperature,max_tokens):

    llm = ChatOpenAI(model=llm_model, openai_api_key=api_key, temperature=temperature, max_tokens=max_tokens)
    output_parser = StrOutputParser()
    
    chain = prompt | llm | output_parser

    answer = chain.invoke({'question':question})

    return answer



# Title of page
st.title("Q&A Chatbot with OpenAI")

# Sidebar for different settings
st.sidebar.title("Settings")

## API Key Input
api_key = st.sidebar.text_input("Enter your OPEN API Key" , type="password")

## Select LLM
llm_model = st.sidebar.selectbox("Select an OPEN API MODEL" , ["gpt-4.1","o4-mini","o3"])

## Adjust response parameters
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

# Interface for user input
st.write("Go ahead and ask any question")
user_input = st.text_input("You:")

if user_input:
    response = generate_response(user_input,api_key, llm_model, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please provide the query")



