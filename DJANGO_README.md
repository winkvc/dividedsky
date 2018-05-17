# Django Setup

So you want to make some changes to the game! Great! Here's how to get started:

## Prerequisites
- have Python installed
- have some Python package manager, preferably `pip`.
- you have `git` installed

## Virtualenv
Standard practice for Python.

```
$ cd ~/the/path/to/this/repo
$ # load the module venv and run it in directory 'venv'
$ python -m venv venv 
```
maybe you need to load.
also that command is riffed from the python3 version, it might be wrong.

## Requirements

now add in all the requirements from requirements.txt
```
(venv) $ pip install --upgrade pip
(venv) $ pip install -r requirements.txt
```

## Running Django

### Create a server
```
(venv) $ python manage.py runserver
```
Ctrl-C [Linux / Mac] will close the server and return you to the terminal.

### Create a superuser and such.
I think when you just start up you'll get some error. That's OK.
Create yourself a superuser.

```
(venv) $ python manage.py createsuperuser
```
Follow the prompts and such.

Now add all the stuff to the database. [todo: wtf does that mean?]
```
(venv) $ python manage.py migrate
```

### A Django
Congrats! You've arrived at the City of Django, and you've
followed the directions from the train station to the place you're staying.
Now it's time to understand the geography of Django.

[under construction]

talk about:
- the idea of a server
- the layers that everything goes through
  - urls.py
  - views.py
- what sticks around
  - models.py



