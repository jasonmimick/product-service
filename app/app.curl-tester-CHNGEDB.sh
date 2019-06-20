set -x
USERNAME=""
APIKEY=""
BASEURL="http://localhost:5000"
#BASEURL="http://product-service"

METHOD=$1
shift; 
DB=$1
shift
COLL=$1
shift
HEADERS="--header \"X-MongoDB-Database: ${DB}\" --header \"X-MongoDB-Collection: ${COLL}\""
echo "testing method (with): ${METHOD} $@"
echo "Sending additional HTTP Headers: ${HEADERS}"
if [ "$METHOD" == "CLEAN" ]; then
  curl -X DELETE ${HEADERS} -u ${USERNAME}:${APIKEY} ${BASEURL}/$@
elif [ "$METHOD" == "GET" ]; then
  curl -X GET ${HEADERS} -u ${USERNAME}:${APIKEY} ${BASEURL}/?$@
elif [ "$METHOD" == "POST" ]; then
  curl -vv -X POST ${HEADERS} -u ${USERNAME}:${APIKEY} -d "$@" ${BASEURL}
elif [ "$METHOD" == "PUT" ]; then
  ID=$1
  shift;
  echo "PUT ID=${ID} args=$@" 
  curl -X PUT ${HEADERS} -u ${USERNAME}:${APIKEY} -d "$@" ${BASEURL}/${ID}
elif [ "$METHOD" == "DELETE" ]; then
  curl -X DELETE ${HEADERS} -u ${USERNAME}:${APIKEY} ${BASEURL}/$@
elif [ "$METHOD" == "DELETE+BODY" ]; then
  curl -vv -X DELETE ${HEADERS} -u ${USERNAME}:${APIKEY} -d "$@" ${BASEURL}
else
  echo "unknown method: ${METHOD}"
fi
