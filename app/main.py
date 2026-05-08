from fastapi import FastAPI

app = FastAPI(
    title="RAG Document Chatbot Backend",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "RAG Backend Running"
    }