
####to start please add virtualenv    
`virtualenv -p python3 venv`  
`source venv/bin/activate`  
then install requirements:  
`pip install -r requirements.txt`  

####Celery configurations:  

`sudo apt-get install rabbitmq-server`
if rabbitmq didnt up try: `sudo rabbitmq-server start`
`celery -A tasks worker`

####RabbitMQ configurations: 

`export PATH=$PATH:/usr/local/sbin`
`sudo rabbitmqctl add_vhost socketio`   
`sudo rabbitmqctl set_permissions -p socketio guest "^.*" ".*" ".*"`  

####Start flask application:
`flask run`

then visit http://127.0.0.1:5000/ add click the button