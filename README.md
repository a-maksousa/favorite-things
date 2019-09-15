## Favorite Things App

## Descriptiom
The favorite-things-app is an application that allows the user to track their favorite things

## Entity Relationship Diagram

![alt](https://raw.githubusercontent.com/a-maksousa/favorite-things/master/ERM.JPG)

### Setting Up For Local Development

-   Check that python 3 is installed:

    ```
    python --version
    >> Python 3.6.5
    ```

-   Install pipenv:

    ```
    brew install pipenv
    ```

-   Check pipenv is installed:
    ```
    pipenv --version
    ```
-   Install dependencies from requirements.txt file:

    ```
    pip install -r requirements.txt
    ```
-   Activate a virtual environment:

    ```
    source favorites/venv/venv
    ```

-   Create new Database Instance (favoritesdb)

-   Apply migrations:

    ```
    flask db upgrade
    ```
*   Should you make changes to the database models, run migrations as follows

    -   Migrate database:

        ```
        flask db migrate
        ```

    -   Upgrade to new structure:
        ```
        flask db upgrade
        ```

##  Running tests
-   On command line run:
    ```
    python -m unittest
    ```

##  Deployment to AWS Lambda using Zappa
-   Change ROUTES_PREFIX in app\static\js\script.js from "" to "/dev" for Lambda routes

-   Change Connection String for mysql database in config.py to Production

-   Install zappa inside virtual environment:

    ```
    pip install zappa
    ```

-   Initialize project with zappa

    ```
    zappa init
    ```

-   Deploy project with zappa

    ```
    zappa deploy dev
    ```

-   Redeploy updates/changes with zappa

    ```
    zappa update dev
    ```
