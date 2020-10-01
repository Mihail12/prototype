
####to start please add virtualenv    
`virtualenv -p python3 venv`  
`source venv/bin/activate`  
then install requirements:  
`pip install -r requirements.txt`  

####Celery configurations:  

sudo apt-get install supervisor -y 

sudo service supervisor start

`redis-server`  
`supervisord -c /Users/michaelspasenko/PycharmProjects/prototype/celery.conf`

to kill all workers type:  
`ps ax | grep celery | awk '{print $1}' | xargs kill -9`
`ps ax | grep supervisor | awk '{print $1}' | xargs kill -9`


####Start flask application:
`flask run`

then visit http://127.0.0.1:5000/ add click the buttons


For cpu limit you should do:  

wget -O cpulimit.zip https://github.com/opsengine/cpulimit/archive/master.zip  
unzip cpulimit.zip  
cd cpulimit-master  
make  
sudo cp src/cpulimit /usr/bin  

cpulimit -l 50 -p 1234  