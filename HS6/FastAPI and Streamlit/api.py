from fastapi import FastAPI

app = FastAPI()

@app.get('/healthcheck')
def healthCheck():
    return {"message" : "The Backend is responding"}
