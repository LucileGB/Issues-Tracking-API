# P10_Lucile_GARRIGOUX: Issue Tracking System

Django Rest Framework-based API focusing on project issues tracking.

##  Installation

First, download the repository and unzip it where preferred.

Then, use the command line interface to navigate into the project directory and create
your virtual environment.

**To set a virtual environment if you don't have one already**, use the command
line interface and type the following:

```pip install venv```

Then, if on Windows:

```python -m venv venv```

If on Unix or MacOS:

```python3 -m venv venv```

Once your virtual environment is activated, you can launch it with the following command:

On Windows:

```venv\Scripts\activate.bat```

On Unix or MacOS :

```source venv/bin/activate```

**Once your virtual environment is installed and activated**, you can install the required
modules with the following command:

```pip install -r requirements.txt```

Then, initialize the database:

```python manage.py migrate```

You are now ready to run the app.

## Usage

Once your virtual environment is activated and, ensure you are in the project_10 directory
and type the following to launch the local server:

```python manage.py runserver```

You can know start to explore the API using any API application of your choice (Postman, Insomnia...).

The complete endpoints documentation is available [here](https://documenter.getpostman.com/view/18129706/UV5f7DdD).

Please note that the database is local.
