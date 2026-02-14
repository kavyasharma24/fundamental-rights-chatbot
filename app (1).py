# -*- coding: utf-8 -*-
"""
Fundamental Rights Chatbot - Hugging Face Spaces Deployment
"""

# Import all required libraries
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from transformers import pipeline
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
import gradio as gr
import os

print("✓ All libraries imported successfully!")

# Load the PDF file
loader = PyPDFLoader("part3.pdf")  # PDF should be in the same directory
documents = loader.load()
print(f"✓ Loaded {len(documents)} pages from the PDF")

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=150,
    separators=["\n\n", "\n", ". ", " ", ""],
    length_function=len
)
docs = text_splitter.split_documents(documents)
print(f"✓ Created {len(docs)} text chunks")

# Load embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
print("✓ Embedding model loaded")

# Create vector store
vectorstore = FAISS.from_documents(docs, embedding_model)
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)
print("✓ Vector store created")

# Load language model
pipe = pipeline(
    "text2text-generation",
    model="google/flan-t5-large",
    max_new_tokens=512,
    temperature=0.3,
    do_sample=True,
    top_p=0.9,
    repetition_penalty=1.2
)
llm = HuggingFacePipeline(pipeline=pipe)
print("✓ Language model loaded")

# Context formatter
def format_docs(docs):
    """Format retrieved documents with clear structure"""
    formatted_chunks = []
    for i, doc in enumerate(docs, 1):
        content = doc.page_content.strip()
        content = ' '.join(content.split())
        formatted_chunks.append(f"[Context {i}]\n{content}\n")
    return "\n".join(formatted_chunks)

# Create prompt template
prompt = ChatPromptTemplate.from_template(
    """You are a legal assistant specializing in Indian Constitutional Law, specifically Part III on Fundamental Rights.

Use the following context from the Constitution of India to answer the question accurately and thoroughly.

Context:
{context}

Question: {question}

Instructions for your answer:
- Provide complete and detailed information
- When listing items (like freedoms or rights), number them clearly (1., 2., 3., etc.)
- Quote directly from the Constitution when relevant
- If the question asks about a specific article, include the article text
- Be comprehensive - don't truncate your response
- If the information is not in the context, state that clearly

Detailed Answer:"""
)

# Build the RAG chain
rag_chain = (
    {
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

print("✓ RAG chain ready!")

# Chat function
def chat(question):
    """Enhanced chat function with error handling"""
    try:
        if not question or not question.strip():
            return "Please enter a question."
        
        question = question.strip()
        response = rag_chain.invoke(question)
        response = response.strip()
        
        if len(response) < 50:
            response += "\n\n(Note: If this answer seems incomplete, try rephrasing your question or asking for more details.)"
        
        return response
    except Exception as e:
        return f"An error occurred: {str(e)}\n\nPlease try rephrasing your question."

# Create Gradio interface
interface = gr.Interface(
    fn=chat,
    inputs=gr.Textbox(
        lines=3,
        placeholder="Ask about Fundamental Rights (e.g., 'What are the freedoms under Article 19?')...",
        label="Your Question"
    ),
    outputs=gr.Textbox(
        label="Answer",
        lines=10
    ),
    title="📚 Fundamental Rights Chatbot",
    description="""
    Ask questions about Part III of the Indian Constitution (Fundamental Rights).
    
    **Tips for better answers:**
    - Be specific about article numbers if you know them
    - Ask about rights, freedoms, or protections
    - For lists, explicitly ask for "all freedoms" or "all rights"
    
    **Example questions:**
    - What is Article 21?
    - List all six freedoms in Article 19
    - What does Article 14 guarantee?
    - Explain the Right against Exploitation
    """,
    examples=[
        ["What is Article 21?"],
        ["What are the six freedoms guaranteed by Article 19?"],
        ["What is Article 17?"],
        ["Explain the Right to Equality"],
        ["What does Article 22 say about arrests?"]
    ],
    theme=gr.themes.Soft()
)

# Launch the interface
if __name__ == "__main__":
    interface.launch()
