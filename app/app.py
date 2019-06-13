import os
import logging
from flask import Flask
from flask import request
from pymongo import MongoClient
from kubernetes import client, config, watch
from flask_httpauth import HTTPBasicAuth

logger = logging.getLogger('products-microservice')
log_level = os.environ.get('PRODUCTS_MICROSERVICE_LOG_LEVEL','DEBUG')
logger.setLevel(log_level)
logger.info('product-microservice startup')

app = Flask(__name__)
auth = HTTPBasicAuth()

config.load_incluster_config()
kube_api = client.CoreV1Api()
secret_name = os.environ.get("PRODUCT_SERVICE_DB_URI")
logger.debug(f'${secret_name}')
secret = kube_api.get_namespaced_secret(secret_name,namespace)
logger.debug(f'Remove this from production! Remove ${secret}')
logger.debug(f'Read ${secret_name} ${secret.data}')

mongo = MongoClient(secret.data)  

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
    app.run(debug=True,host='0.0.0.0',port='12831')
