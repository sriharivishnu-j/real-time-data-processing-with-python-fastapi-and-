from fastapi import FastAPI, HTTPException
from app.api import router as api_router
import logging

# Initialize logging
logging.basicConfig(filename='logs/app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI(title="Real-time Data Processing API")

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the Real-time Data Processing API"}
