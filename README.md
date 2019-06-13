```
                      _            _                                 _          
  _ __  _ __ ___   __| |_   _  ___| |_ ___       ___  ___ _ ____   _(_) ___ ___ 
 | '_ \| '__/ _ \ / _` | | | |/ __| __/ __|_____/ __|/ _ \ '__\ \ / / |/ __/ _ \
 | |_) | | | (_) | (_| | |_| | (__| |_\__ \_____\__ \  __/ |   \ V /| | (_|  __/
 | .__/|_|  \___/ \__,_|\__,_|\___|\__|___/     |___/\___|_|    \_/ |_|\___\___|
 |_|                                                                            
```
---
A simple basic Kubernetes-ready, HTTP based microservice which can 
query and update a collection of products in MongoDB. The service 
is implemented in python and uses:
- Flask
- pymongo
- python-kubernetes

Authentication uses standard username:password HTTP digest.

There is a single default route ``/`` which accepts, `GET`, `POST`, & `DELETE` 
`HTTP` Methods. Refer to app/app.py for the API reference and examples.

This sample software is for educational purposes and not meant for 
production systems. 

## Getting started

```bash
$git clone https://github.com/jasonmimick/products-service
$cd products-service
$kubectl create secret PRODUCTS_SERVICE_MONGODB_URI
"mongodb+srv://products-db-src.cluster.local"
$kubectl apply -f kubernetes/products-service.yaml
