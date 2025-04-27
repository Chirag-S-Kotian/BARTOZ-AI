import schedule
import time
import subprocess
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

# Command to run your indexing pipeline (modify if your entrypoint is different)
INDEX_COMMAND = ["python", "rag_pipeline.py"]


def run_indexing():
    logging.info(f"[{datetime.now()}] Running FAISS indexing pipeline...")
    try:
        result = subprocess.run(INDEX_COMMAND, capture_output=True, text=True)
        if result.returncode == 0:
            logging.info(f"Indexing succeeded: {result.stdout}")
        else:
            logging.error(f"Indexing failed: {result.stderr}")
    except Exception as e:
        logging.error(f"Error running indexing: {e}")

# Schedule: run once per day at 2:00 AM (customize as needed)
schedule.every().day.at("02:00").do(run_indexing)

logging.info("Scheduler started. Will run the indexing pipeline daily at 2:00 AM.")

while True:
    schedule.run_pending()
    time.sleep(60)
