from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from tensorflow.keras.models import load_model
import pinecone
import yaml
import logging

# Load configuration
with open('config/config.yaml') as f:
    config = yaml.safe_load(f)

# Initialize Pinecone
pinecone.init(api_key=config['database']['pinecone']['api_key'],
              environment=config['database']['pinecone']['environment'])
index = pinecone.Index(config['database']['pinecone']['index_name'])

# Load TensorFlow model
model = load_model(config['model']['path'])

router = APIRouter()

class DataInput(BaseModel):
    input_data: list

@router.post("/process")
async def process_data(data: DataInput):
    logging.info("Processing data through TensorFlow model.")
    try:
        # Model inference
        prediction = model.predict([data.input_data]).tolist()

        # Vector database insertion
        logging.info("Inserting data into Pinecone.")
        index.upsert([(str(i), x) for i, x in enumerate(prediction)])

        return {"predictions": prediction}
    except Exception as e:
        logging.error(f"Error processing data: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
