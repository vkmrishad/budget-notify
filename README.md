# budget notify

## System dependencies

* [Python: 3.9+](https://www.python.org/downloads/)
* [MySQL: 7+](https://dev.mysql.com/)

## Environment and Package Management
Install [Poetry](https://python-poetry.org/)

    $ pip install poetry
    or
    $ pip3 install poetry

Activate or Create Env

    $ poetry shell

Install Packages from Poetry

    $ poetry install

NB: When using virtualenv, install from [requirements.txt](/budget-notify/requirements.txtquirements.txt) using `$ pip install -r requirements.txt`.
For environment variables follow [sample.env](/budget-notify/sample.envify/sample.env)

## Migrate DB

    $ mysql -u <user> -p <password> <database> < db.sql
    $ mysql -u <user> -p <password> <database> < migrate.sql

## Run 

    $ python cli.py

## Test

    $ pytest tests

