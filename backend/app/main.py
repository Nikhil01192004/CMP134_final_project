from fastapi import FastAPI

app = FastAPI(title="Robot Management System")

@app.get("/")
def root():
    return {"message": "Robot Management Backend Running"}