import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from pydantic import BaseModel
from dotenv import load_dotenv

# LangChain
from langchain_community.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain_community.utilities import SerpAPIWrapper
from langchain.schema import Document

load_dotenv()

# -------------------
# Configuration DB
# -------------------
PG_CONNECTION_STRING = (
    f"postgresql+psycopg2://"
    f"{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}"
    f"@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}"
    f"/{os.getenv('PG_DB')}"
)

TABLE_NAME = "documents"


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str

class ChatRequest(BaseModel):
    question: str
    history: list[ChatMessage]


# -------------------
# Embeddings et vectordb
# -------------------
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectordb = PGVector(
    connection_string=PG_CONNECTION_STRING,
    embedding_function=embeddings,
    collection_name=TABLE_NAME
)

# -------------------
# Recherche interne
# -------------------
def retrieve_relevant_chunks(question: str, k: int = 5):
    docs = vectordb.similarity_search(query=question, k=k*2)
    unique_docs = []
    seen_texts = set()
    for doc in docs:
        if doc.page_content not in seen_texts:
            unique_docs.append(doc)
            seen_texts.add(doc.page_content)
        if len(unique_docs) >= k:
            break
    return unique_docs

def format_chunks(chunks):
    return "\n\n".join([doc.page_content for doc in chunks])

# -------------------
# Recherche externe
# -------------------
serp = SerpAPIWrapper()  # nécessite SERPAPI_API_KEY dans .env

def external_search(query: str):
    results = serp.run(query)
    return results

# -------------------
# CoT + synthèse
# -------------------
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

cot_prompt = PromptTemplate(
    input_variables=["history","question", "chunks", "external_info"],
    template="""
Tu es un assistant pédagogique pour un cours de science politique. Tu ne dois utiliser que les informations fournies des sources internes et externes pour répondre à la question. Tu dois spécifié quand les infos proviennent des documents internes ou de la recherche externe.

Historique de la conversation :
{history}

Question : {question}

Documents internes pertinents :
{chunks}

Informations externes (si certains termes sont complexes ou absents) :
{external_info}

Raisonnement étape par étape :
1. Analyse la question.
2. Identifie les termes ou concepts manquants ou complexes.
3. Explique chaque terme complexe en utilisant les infos internes et externes.
4. Génère toujours une réponse complète et pédagogique en faisant une explication avec les infos internes.
5. Génère toujours une réponse complète et pédagogique en faisant une explication avec les infos externes.
6. Synthétise les deux explications pour fournir une réponse finale claire et concise.
7. Vérifie la cohérence de ta réponse.
8. Indique la provenance des informations utilisées (internes ou externes).

Réponse finale :
"""
)

cot_chain = LLMChain(llm=llm, prompt=cot_prompt)

def format_history(history):
    return "\n".join(
        [f"{m.role.upper()}: {m.content}" for m in history]
    )

def answer_question(question: str, history: list, k: int = 5):
    relevant_chunks = retrieve_relevant_chunks(question, k)
    chunks_text = format_chunks(relevant_chunks)
    external_info = external_search(question)

    history_text = format_history(history)

    response = cot_chain.invoke({
        "history": history_text,
        "question": question,
        "chunks": chunks_text,
        "external_info": external_info
    })

    return response["text"]


# -------------------
# FastAPI
# -------------------
app = FastAPI()

# CORS pour frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Serve frontend statique
app.mount("/static", StaticFiles(directory="frontend"), name="static")
@app.get("/")
async def serve_index():
    return FileResponse("frontend/index.html")

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(req: ChatRequest):
    answer = answer_question(
        question=req.question,
        history=req.history
    )
    return {"answer": answer}

