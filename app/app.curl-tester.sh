set -x
USERNAME=""
APIKEY=""
BASEURL="http://localhost:5000"
#BASEURL="http://product-service"

METHOD=$1
shift; 
echo "testing method (with): ${METHOD} $@"
if [ "$METHOD" == "CLEAN" ]; then
  curl -X DELETE -u ${USERNAME}:${APIKEY} ${BASEURL}/$@
elif [ "$METHOD" == "GET" ]; then
  curl -X GET -u ${USERNAME}:${APIKEY} ${BASEURL}/?$@
elif [ "$METHOD" == "POST" ]; then
  curl -vv -X POST -u ${USERNAME}:${APIKEY} -d "$@" ${BASEURL}
elif [ "$METHOD" == "PUT" ]; then
  ID=$1
  shift;
  echo "PUT ID=${ID} args=$@" 
  curl -X PUT -u ${USERNAME}:${APIKEY} -d "$@" ${BASEURL}/${ID}
elif [ "$METHOD" == "DELETE" ]; then
  curl -X DELETE -u ${USERNAME}:${APIKEY} ${BASEURL}/$@
elif [ "$METHOD" == "DELETE+BODY" ]; then
  curl -vv -X DELETE -u ${USERNAME}:${APIKEY} -d "$@" ${BASEURL}
else
  echo "unknown method: ${METHOD}"
fi
