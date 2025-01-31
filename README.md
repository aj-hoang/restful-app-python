# restful-app-python

This is a simple restful python backend that interacts with a local postgres DB.

Requests will allow you to create/read/update/delete movies (CRUD)

* Automated tests
* Input sanitation
* Error Handling
* Observability

## Prerequisites

* Python 3.10+
* Poetry 1.8
* Local postgres - I've made a simplifying assumption that one has a local instance of postgres running

* Run the following
  1) `poetry config virtualenvs.in-project true` 
  2) Then run `poetry install` 
  3) This will create a virtual environment within the project which will allow VSCode to detect the venv and thus the dependencies for this project when developing.
  4) run `poetry build` and this will build the zip + .whl files in the `dist/` directory


## Running the python backend
Once a poetry shell is active, do the following:
  1) Ensure you have a postgres instance running.
  1) In commandline, run `fastapi dev src.main.py` - this will start the python backend
  2) Then you can interact via: 
     * Server: http://127.0.0.1:8000
     * Documentation: http://127.0.0.1:8000/docs

## Running tests
Once a poetry shell is active, run `pytest` which will run the tests under the tests directory