from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Robot Management System Running"}
