from fastapi import FastAPI

from api.routes import router

app = FastAPI(title="Document RAG", version="0.1.0")
app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "RAG app is running"}
