import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/test")
async def run_test() -> str:
    return "Success"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
