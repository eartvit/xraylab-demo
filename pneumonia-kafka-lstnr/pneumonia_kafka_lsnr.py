from flask import Flask, request, jsonify
import requests
import logging
import os
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'

access_key = os.environ['AWS_ACCESS_KEY_ID']
secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
region_name = os.environ['region_name']
service_point = os.environ['pneumonia_service_endpoint']

def extract_data(msg):
  bucket_eventName=msg['eventName']
  bucket_name=msg['s3']['bucket']['name']
  bucket_object=msg['s3']['object']['key']
  data = {'bucket_eventName':bucket_eventName, 'bucket_name':bucket_name, 'bucket_object':bucket_object}
  return data  


@app.route("/", methods=["POST"])
def kafka_listener():
  content = request.data
  content = content.decode('utf-8')
  #logging.info(f'Initial payload: {request}')
  #logging.info(f'Extracting kafka message details from request: {content}')
  data = extract_data(content['Records'][0])
  logging.info(f"Extracted data for prediction service: {data}")

  results_OK = True
  ex = None
  
  if 's3:ObjectCreated' in data['bucket_eventName']:
    message = {
        "data":{
            "names":[
                "aws_key_id",
                "aws_key",
                "region_name",
                "bucket_name",
                "file_path_name"
            ],
            "ndarray":[
                [
                    access_key,
                    secret_key,
                    region_name,
                    data['bucket_name'],
                    data['bucket_object']
                ]
            ]
        }
    }
    
    try:    
      resp = requests.post(service_point, json=message)
      logging.info(f"Processed request results: {resp}")
    except Exception as e:
      results_OK = False
      ex = e
      logging.error(f"Prediction service exception: {ex}")
  
  srv_resp = jsonify(success=True)
  if False == results_OK:
    srv_resp = jsonify(ex)
  
  return srv_resp
  

# app.add_url_rule("/", view_funk=kafka_listener, methods=["POST"])

if __name__ == '__main__':
  app.run('0.0.0.0', port=8080)
