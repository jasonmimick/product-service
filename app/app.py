import os
import sys
import logging
from flask import Flask
from flask import request
from pymongo import MongoClient
#from kubernetes import client, config, watch
from flask_httpauth import HTTPBasicAuth

logger = logging.getLogger('products-microservice')
log_level = os.environ.get('PRODUCTS_MICROSERVICE_LOG_LEVEL','DEBUG')
logger.setLevel(log_level)
logger.info('product-microservice startup')
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.debug(f'{os.environ}')

app = Flask(__name__)
auth = HTTPBasicAuth()

ns_file = '/var/run/secrets/kubernetes.io/serviceaccount/namespace'
with open(ns_file,'r') as f:
    namespace = f.read()
logger.info(f'{namespace}')
dburi = os.environ.get('PRODUCTS_SERVICE_DB')
logger.debug( f'Read environment PRODUCTS_SERVICE_DB: {dburi}' )
mongo = MongoClient(dburi)  

#client = MongoClient('example.com',
#                      username="<X.509 derived username>"
#                      authMechanism="MONGODB-X509",
#                      ssl=True,
#                      ssl_certfile='/path/to/client.pem',
#                      ssl_cert_reqs=ssl.CERT_REQUIRED,
#                      ssl_ca_certs='/path/to/ca.pem')
                                 
@auth.verify_password
def verify_password(username, password):
    potential_key = { '_id' : '{}:{}'.format(username,password) }

    valid_key = mongo['kubestore']['apikeys'].find_one( protential_key )
    logger.info(f'verify_password ${key}')
    return valid_key is not None


@app.route('/', methods = ['GET', 'POST', 'DELETE'])
@auth.login_required
def root():
    kube_products = mongo['kubestore']['products']
    if request.method == 'GET':
       query = request.args
       return (200,list(kube_products.find(query)))

    elif request.method == 'POST':
       if not request.is_json:
         return (500,'Content-Type: application/json REQUIRED')
       product = request.get_json() 
       result = kube_products.update_one({ '_id' : product['_id'] }, product, upsert=True)
       return (200, result)
       
    elif request.method == 'DELETE':
       if not request.is_json:
         return (500,'Content-Type: application/json REQUIRED')
       product = request.get_json() 
       result = kube_products.delete_one({ '_id' : product['_id'] })
       return (200, result)
    else:
       return (500, f'Unsupported ${request.method}')

if __name__ == '__main__':
    port = os.environ.get('PRODUCTS_SERVICE_SERVICE_PORT_HTTP')
    logger.info(f'Read PRODUCTS_SERVICE_SERVICE_PORT_HTTP={port}')
    app.run(debug=True,host='0.0.0.0',port=port)
