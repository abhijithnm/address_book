#ADDRESS BOOK APPLICATION

##introduction

This application is to save addresses with coordinates, and to retrive based on the distance

##getting started

Create an evironment in your machine

###For linux follow steps below:-

    - enter into project folder
    - open terminal
    - sudo apt install python3-virtualenv
    - irtualenv address_env
    - source address_env/bin/activate

###If you are using some other os(follow steps mentioned in the given link.

(https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
For installing reqired libraries

    - pip3 install -r requirements.py

###For starting the project:-

    - uvicorn address_book.main:app --reload

###Use below swagger docs for accessing CRUD API’s

    -> http://127.0.0.1:8000/docs#/

###Available API’s

    - Create address  http://127.0.0.1:8000/create-address/
    - Get all address  http://127.0.0.1:8000/get-address/
    - Get address using id  http://127.0.0.1:8000/get-address-by-id/{address_id}
    - Update address using id http://127.0.0.1:8000/update-address/{address_id}
    - Delete address using id  http://127.0.0.1:8000/delete-address/{address_id}
    - Get address with coordinate and distance  http://127.0.0.1:8000/search-address/