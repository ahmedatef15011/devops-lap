from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Simple API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
