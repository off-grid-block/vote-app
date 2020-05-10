# DEON Service - Voting

This is the repository for an example application deployed on top of the DEON service.

## Getting Started

### Installing pipenv

To install pipenv, use the pip command.

```bash
pip install pipenv
```

### Installing requirements

Clone this repository. Then run the following commands to install the necessary requirements for the voting app:

```bash
# clone this repository
git clone https://github.com/off-grid-block/vote-app.git

# cd into the repository's directory
cd vote-app

# start up the pipenv virtual environment
pipenv shell

# install requirements listed in the Pipfile
pipenv install
```

## Test Deployment

To run the app in a test environment, use the following command inside the cloned directory:

```bash
# activate virtual environment (if not already active)
pipenv shell

# run the server at http://localhost:[port]/
python manage.py runserver [port]
```

## Manage the Website

With the shell active, create a superuser for the website using the following command:
```bash
python manage.py createsuperuser
```

View the admin page at [URL]/admin and log in using the superuser you just created.