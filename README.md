
####to start please add virtualenv    
`virtualenv -p python3 venv`  
`source venv/bin/activate`  
then install requirements:  
`pip install -r requirements.txt`  

####Celery configurations:  

sudo apt-get install supervisor -y 

sudo service supervisor start

`redis-server`  
`supervisord -c /Users/michaelspa/PycharmProjects/prototype/celery.conf`

supervisorctl start  
supervisorctl stop

to kill all workers type:  
`ps ax | grep celery | awk '{print $1}' | xargs kill -9`
`ps ax | grep supervisor | awk '{print $1}' | xargs kill -9`


####Start flask application:
`flask run`

then visit http://127.0.0.1:5000/ add click the buttons


For cpu limit you should do:  

apt-get install cpulimit

cpulimit -l 20 -p 1234  