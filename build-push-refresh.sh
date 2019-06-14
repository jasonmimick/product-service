docker build -t quay.io/jason_mimick/products-service .
docker push quay.io/jason_mimick/products-service
kubectl delete -f products-service.yaml
sleep 20
kubectl create -f products-service.yaml

