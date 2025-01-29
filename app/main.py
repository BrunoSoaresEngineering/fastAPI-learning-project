import logging
import logging.config

from fastapi import FastAPI, HTTPException

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def read_root():
    try:
        1 / 0
    except Exception as e:
        logging.error(f"An Exception occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred")
