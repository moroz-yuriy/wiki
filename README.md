## Want to use this project?

## Installation
1. Fork/Clone
    ``` 
    git clone https://github.com/ymoroz-da/wiki.git 
    ```
1. Create and activate a virtualenv
    ```
    cd  wiki
    python -m venv env
    source env/bin/activate
    ```
   
1. Install the requirements
    ```
    pip install -r requirements.txt
    ```
1. Create a Postgres database
    ```
    $ psql
    # CREATE DATABASE wiki;
    CREATE DATABASE
    # \q
    ```
1. Apply the migrations
    ```
    python manage.py migrate
    ```
1. Run the server
    ```
    python manage.py runserver 8000
    ```
### Optional 
    Run tests
    ```
    python manage.py test -v 3
    ```
## API documentation 
    http://127.0.0.1:8000/docs/
    
## Browsable API interface
    http://127.0.0.1:8000/api/v1/wiki/
    
# Enjoy.