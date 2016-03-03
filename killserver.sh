echo $(lsof -iTCP:80 | grep LISTEN | awk '{print $2}')
#echo $(lsof -iTCP:80 | awk '{print $2}')
PORT_NUMBER=80
echo "Kill http server"
lsof -iTCP:${PORT_NUMBER} | grep LISTEN | awk '{print $2}' | xargs kill

PORT_NUMBER=443
echo "Kill https server"
lsof -i TCP:${PORT_NUMBER} | grep LISTEN | awk '{print $2}' | xargs kill

PORT_NUMBER=8081
echo "Kill gevent server"
lsof -i TCP:${PORT_NUMBER} | grep LISTEN | awk '{print $2}' | xargs kill

PORT_NUMBER=3000
echo "Kill node.js server"
lsof -i TCP:${PORT_NUMBER} | grep LISTEN | awk '{print $2}' | xargs kill

PORT_NUMBER=444
lsof -i TCP:${PORT_NUMBER} | grep LISTEN | awk '{print $2}' | xargs kill
