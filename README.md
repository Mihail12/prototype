
####to start please add virtualenv    
`virtualenv -p python3 venv`  
`source venv/bin/activate`  
then install requirements:  
`pip install -r requirements.txt`  

####Celery configurations:  

`redis-server`  
`celery -A tasks worker -n 1 --logfile=/dev/null`  
`celery -A tasks worker -n 2 --logfile=/dev/null`    
`celery -A tasks worker -n 3 --logfile=/dev/null`   

####Start flask application:
`flask run`

then visit http://127.0.0.1:5000/ add click the buttons