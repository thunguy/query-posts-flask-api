## Installation

To have this app running on your local computer, please follow the below steps:

Inside the project directory, create and activate a virtual environment:
```
$ pip3 install virtualenv
$ virtualenv env
$ source env/bin/activate
```
Install dependencies:
```
(env) $ pip3 install -r requirements.txt
```
Launch server to run Flask app:
```
OPTION 1 (auto reload, preferred):
(env) $ python3 -i app.py

-OR-

OPTION 2 (manual reload):
(env) export FLASK_APP=app.py
(env) flask run -h 0.0.0.0
```
Navigate in web browser or curl in terminal to query the API:
```
1.) 'http://localhost:5000' + '/api/ping'

2.) 'http://localhost:5000' + '/api/posts?tags=' + '&sortBy=' + '&direction='
        tags = required; separate multiple tags with commas
        sortBy = optional; choose one: [id, likes, reads, popularity], otherwise default sort by id
        direction = optional; choose one: [asc, desc], otherwise default direction in ascending order

        EXAMPLE: 'http://localhost:5000/api/posts?tags=health,science,tech&sortBy=popularity&direction=desc'
```
