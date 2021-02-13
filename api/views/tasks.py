from fastapi import Request,status,BackgroundTasks,FastAPI
from fastapi.responses import JSONResponse
import time,csv
from datetime import datetime
from typing import List,Optional
app = FastAPI()
#worker task process

def _run_task(data:Optional[List] = None):
    time.sleep(3)
    keys = data[0].keys()
    with open('data_out.csv', 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file,keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
            
"""
@app.post("/task/run/{name}/{id}")
async def task_run(name:str,id:int,background_tasks :BackgroundTasks):
    background_tasks.add_task(_run_task,name,id)
    return {"message":f"Task {name} ID {id} is being run...\n"}
"""