
####to start please add virtualenv    
`virtualenv -p python3 venv`  
`source venv/bin/activate`  
then install requirements:  
`pip install -r requirements.txt`  

####Celery configurations:  

`redis-server`  
`celery -A tasks worker -n worker1 -c 1`  
`celery -A tasks worker -n worker2 -c 1`    
`celery -A tasks worker -n worker3 -c 1`   

to kill all workers type:  
`ps auxww | grep 'worker' | awk '{print $2}' | xargs kill -9`

####Start flask application:
`flask run`

then visit http://127.0.0.1:5000/ add click the buttons