import gradio as gr
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Initialize the OLLAMA chat model
ollama = ChatOllama(model="llama3")

# Define a chat prompt template
prompt_template = "Tell me a short joke about {topic}"

# Create a LangChain pipeline with the chat prompt, OLLAMA, and output parser
pipeline = ChatPromptTemplate.from_template(prompt_template) | ollama | StrOutputParser()

# Define the chatbot function
def chatbot(topic):
    # Invoke the LangChain pipeline with the specified topic
    response = pipeline.invoke({"topic": topic})
    return response

# Create a Gradio interface for the chatbot
interface = gr.Interface(fn=chatbot, inputs="text", outputs="text", title="Chatbot with LangChain")
interface.launch()
