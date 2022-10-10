from fastapi import FastAPI, HTTPException, status, Response, Request
import logging
import boto3, botocore
import json
import pandas as pd
import os, pathlib
from pydantic import BaseModel
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List
import uvicorn


# Defined the schema attributes
class Item(BaseModel):
    loc: str
    message: str
    type: str

# response from schema
class ErrorResponse(BaseModel):
    detail: List[Item]

# method to validate the schema
def error_validation_schema(request: Request, exc: RequestValidationError):
    errors = {
        "details": [
            {
            "location": err["loc"],
            "message": err["msg"],
            "type":    422
            }    
        ] for err in exc.errors()
    }
    err_response = ErrorResponse(**errors)
    return JSONResponse(
        content = jsonable_encoder(err_response.details[0]),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )

# main application
app = FastAPI(
    exception_handlers = { RequestValidationError: error_validation_schema },
    responses = {
        422: {
            "description": "Validation Error",
            "model": ErrorResponse
        }
    }
)

# users current working directory
CWD = pathlib.Path.cwd()

# logs
logging.basicConfig(filename=f"{CWD}/logs/app.log", level=logging.INFO)
logger = logging.getLogger(__name__)

class DynamoDB():
    def __init__(self, dynamodb_resources: str):
        self.dynamodb_resources = dynamodb_resources
        self.table = None

    def describe_table(self, table_name: str):
        """Determine dynamodb table existence
           :param dynamodb_resources: Dynamodb resources
           :param table_name: The table name 
           :return: table name if exists
        """
        try:
            table = self.dynamodb_resources.Table(table_name)
            table.load()
            table_exists = True
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == "ResourceNotFoundException":
                table_exists = False
            else:
                logger.error(
                    f"{table_name} not found! Reason: {error.response['Error']['code']: error.response['Error']['message']}")
                raise
        else:
            self.table = table
        return f"{table}: table_exists"

    def scan_db(self, table_name: str):
        """Scan dynamodb table
           :return: all items in the table
        """
        key_words = {
            # 'FilterExpression': Key('year').between(year_range['first'], year_range['second']),
            # 'ProjectionExpression': "#yr, title, info.rating",
            # 'ExpressionAttributeNames': {"#yr": "year"}
            }        
        extract_data = []

        try:
            done = False
            start_key = None
            while not done:
                if start_key:
                    key_words['ExclusiveStartKey'] = start_key
                table = self.dynamodb_resources.Table(table_name)
                response = table.scan(**key_words)
                extract_data.extend(response.get('Items', []))
                start_key = response.get('LastEvaluateKey', None)
                done = start_key is None
        except botocore.exceptions.ClientError as error:
            logger.error(f"{table_name} could not be scanned, Reason: {error.response['Error']['code']}: {error.response['Error']['message']}")
            raise
        return extract_data

# secret endpoint
@app.get("/secret")
def publish_data(dynamodb_resources: str, table_name: str):
    """
    This is a secret endpoint that
    returns the retrived items from interview_spaces table as a Json file
    """
    dynamodb = DynamoDB(dynamodb_resources)
    table_exists =  dynamodb.describe_table(table_name)
    if not table_exists:
        logger.info(f"View the {table_name} error in the describe function section!")
    
    response =  dynamodb.scan_db(table_name)
    res_json = json.dumps(response)

    # file path, use the current working directory
    CSV_FILE = "result.csv"
    CSV_PATH = os.path.join(CWD, CSV_FILE)

    # convert json to csv
    data_frame = pd.read_json(res_json)
    data_frame.to_csv(CSV_PATH, encoding='utf-8', index=False)
    json_compatible_data_frame = jsonable_encoder(data_frame)
    if not json_compatible_data_frame:
        return error_validation_schema(request, exec)
    return json_compatible_data_frame
    


if __name__ == "__main__":
    publish_data(boto3.resource('dynamodb'), 'interview_spaces')
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    server.run()