# restful-app-python

This is a simple restful python backend that interacts with a local postgres DB.

Requests will allow you to create/read/update/delete movies (CRUD)

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
  1) In commandline, run `fastapi dev app/main.py` - this will start the python backend
  2) Then you can interact via: 
     * Server: http://127.0.0.1:8000
     * Documentation: http://127.0.0.1:8000/docs
         * You can interact using the docs page to execute requests 


_Logs can be viewed in the `app.log` file which will be in the root directory of this project_

## Running tests
Once a poetry shell is active, run `pytest` which will run the tests under the tests directory.

_Noting that you won't need a running postgres instance to run these tests, they will run against an in-memory sqlite DB._

## Pre-commit hooks
This repo uses pre-commit hooks to execute `black` and `flake8` to auto-format python code