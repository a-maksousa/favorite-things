## Favorite Things App

## Descriptiom
The favorite-things-app is an application that allows the user to track their favorite things

## Entity Eelationship Diagram

![alt](https://raw.githubusercontent.com/a-maksousa/favorite-things/master/ERM.JPG)

### Setting Up For Local Development

-   Check that python 3 is installed:

    ```
    python --version
    >> Python 3.7.0
    ```

-   Install pipenv:

    ```
    brew install pipenv
    ```

-   Check pipenv is installed:
    ```
    pipenv --version
    >> pipenv, version 2018.10.13
    ```
-   Install dependencies from requirements.txt file:

    ```
    pip install -r requirements.txt
    ```
-   Activate a virtual environment:

    ```
    pipenv shell
    ```

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
## Local Deployment to AWS Lambda using Zappa

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
