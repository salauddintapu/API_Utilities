import yaml
import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import Annotated
from pdf2image import convert_from_bytes
from Utils.save_log import LOG
import asyncio

logger = LOG()

#load configuration
data = open('configuration.yaml', 'r')
data = yaml.safe_load(data)

#decode image
def convert_to_img(data):
    arr = np.fromstring(data, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return {'0':img}

#decode pdf
def decode_pdf(data):
    pages={}
    pdf = convert_from_bytes(data)
    for idx, i in enumerate(pdf):
        pages.update({str(idx):cv2.cvtColor(np.asarray(i), cv2.COLOR_RGB2BGR)})
    return pages

#api
app=FastAPI()

counter_lock = asyncio.Lock()
counter = 0

#request validation
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse({'MissingFields':str([i['loc'][1] for i in exc.errors()])})

@app.post('/endpoint')
async def get_predictions(file: UploadFile=File(...),
                          doc_type: Annotated[str, Form()]=None):
    
    #api request counter
    global counter
    async with counter_lock:
        counter += 1
    print('==========req. no.:', counter)
    
    try:
        #image
        if file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            img = convert_to_img(await file.read())

            #call model
            #api functionality starts here

        #pdf
        elif file.filename.lower().endswith('.pdf'):
            pages = decode_pdf(await file.read())

            #call model
            #api functionality starts here
        
        else:
            logger.log_file(error='Unknown image file format or missing file. One of PDF, PNG, JPG, JPEG required.')
            return JSONResponse({'Error':'Unknown image file format or missing file. One of PDF, PNG, JPG, JPEG required.'})
    
    except Exception as e:
        logger.log_file(error=e)
        return JSONResponse({'result': 'error during prediction', 'error': e})

if __name__ == '__main__': 
    uvicorn.run("app:app", host=data['app']['hostname'], port=data['app']['port'])