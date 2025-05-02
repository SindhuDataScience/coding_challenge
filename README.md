# Coding Challenge App

A skeleton flask app to use for a coding challenge.

## Install:

You can use a virtual environment (conda, venv, etc):
```
conda env create -f environment.yml
source activate user-profiles
```
or
```
python3 -m venv venv
venv\Scripts\activate
```

Or just pip install from the requirements file
```
pip install -r requirements.txt
```

## Running the code
```
python3 run.py
```

### Spin up the service

```
# start up local server
python -m run
```

### Making Requests

```
curl -i "http://127.0.0.1:5000/health-check"
```
Or go to browser and type the url with the endpoint:
Ex: http://localhost:5000/profiles/mailchimp/mailchimp
http://localhost:5000/health-check

### Run the tests

Set PATH first. Ex: set PYTHONPATH=C:\coding_challenge;%PYTHONPATH%
```
#
pytest tests/test_profile_service.py
```

## What'd I'd like to improve on...

This project I worked on is a good start to build an API with essential code for endpoints, loggers for catching errors and some basic testcases. There is lot of scope for improvement as mentioned below:

-> Include custom exceptions for API errors that can provide the right reasons in case of failures
-> Add more testcases to cover all the edge case scenarios
-> Add credentials to API calls to enhance security
-> Use Asynchronous requests if need be 
-> Code Modularity can be improved for better maintenance of the project

