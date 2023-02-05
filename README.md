# budget notify

![example workflow](https://github.com/vkmrishad/budget-notify/actions/workflows/black.yml/badge.svg?branch=main)
![example workflow](https://github.com/vkmrishad/budget-notify/actions/workflows/test.yml/badge.svg?branch=main)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

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

