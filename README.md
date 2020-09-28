

celery -A tasks worker


sudo apt-get install rabbitmq-server
sudo rabbitmqctl add_vhost socketio  
rabbitmqctl set_permissions -p socketio guest "^.*" ".*" ".*"  