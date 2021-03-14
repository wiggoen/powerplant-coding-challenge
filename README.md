# Install Python 3 (Python 3.7.3 used in this app)
[python.org](https://www.python.org/)

# Clone repository
```
$ cd path/to/where/you/want/it
$ git clone https://github.com/wiggoen/powerplant-coding-challenge.git
```

# REST API
REST: REpresentational State Transfer

API: Application Programming Interface

# Flask
[Flask](https://flask.palletsprojects.com/en/1.1.x/)

# HTTP Request methods
[HTTP request methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)

# The application
## Make the virtual environment
```
$ cd powerplant-coding-challenge
$ python3 -m venv venv
$ source venv/bin/activate
```

## Install requirements
```
$ pip3 install -r requirements.txt
```

## Running the application
```
$ python3 app.py
```

## POST request
In a new terminal:
```
$ cd powerplant-coding-challenge
Format of CURL request
$ curl --request POST --header "Content-Type: application/json" --data "@path/to/filename.json" http://localhost:port

-X or --request
-H or --header

For example:
$ curl -X POST -H "Content-Type: application/json" --data "@example_payloads/payload1.json" http://127.0.0.1:8888/productionplan

```

## Exit the application
```
CTRL + C
```

## Leave the virtual environment
```
$ deactivate
```
