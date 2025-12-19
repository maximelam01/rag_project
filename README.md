# rag_project
RAG application deploy on the cloud
## link of the application : https://rag-project-162391846946.europe-west1.run.app/


This project is an **educational conversational agent** using **RAG (Retrieval-Augmented Generation)** built with **FastAPI**, **LangChain**, and **OpenAI**. It allows users to ask questions related to political science and get detailed, step-by-step answers from internal documents and external search results. It's an agent who choose which tool use (interal/extenal info)

---

## 🚀 Features

- Conversational agent interface
- Retrieval of relevant internal documents (vector search)
- Optional external search for missing information
- Step-by-step reasoning for explanations
- Maintains a **conversation history** (up to 20 messages)
- Deployed on **GCP Cloud Run** with a public URL

---

## 📦 Tech Stack

- **Backend**: Python, FastAPI, LangChain, OpenAI API
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL (for document storage and vector search)
- **Containerization**: Docker
- **Cloud Deployment**: Google Cloud Run

---

Project: Educational Agent for Political Science Course (RAG + CoT Reasoning)
Our project aims to develop an intelligent agent designed to assist students in
understanding a political science course by answering questions and explaining
complex concepts. The agent will combine an internal knowledge base (course
documents) with external information retrieved from the internet to provide reliable,
complete, and pedagogical explanations.
The system is built around a RAG (Retrieval Augmented Generation) pipeline:
1. The agent first queries the course documents to locate the most relevant
sections.
2. It extracts the necessary information to generate an accurate answer.
3. If the question includes complex terms or if the internal knowledge base lacks
certain definitions, the agent performs external internet searches to retrieve
valid and up-to-date explanations.
To ensure clear and controlled reasoning, we will explicitly integrate Chain of Thought
(CoT). The model will follow structured steps: question analysis, internal retrieval,
identification of missing knowledge, targeted external search, synthesis of all
information, and coherence self-verification.
The agent will be accessible through a Streamlit interface, where users can submit
questions and optionally view the reasoning steps used to produce the answer. The goal
is to create a transparent, reliable, and educational tool adapted to learning concepts
that are often abstract in political science.
Main Features
• Search and retrieval from the course knowledge base (RAG).
• Automatic detection of complex terms and external search for definitions.
• Explicit reasoning through Chain of Thought (CoT).
• Clear and beginner-friendly explanations.
• Light self-correction to reduce errors.
• User-friendly Streamlit interface.
Project Members
• Maxime LAMBERT
• Mathias ROBERT
