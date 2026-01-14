from fastapi import FastAPI

app = FastAPI(title="Memocha")

@app.get("/health")
def health_check():
    return {"status": "ok"}