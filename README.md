# simple-video-editor

## 01. What is this ?

This is a very simple video editor app.  

## 02. Contents

- app
  - models
  - templates
  - views

## 03. Get Started

At first : install necessary packages.  

    pip install -r ./setup/requirements.txt

Second : create db before run.

    python

    >>> from app import create_app
    >>> from app.models.db_manager import db_manager
    >>> app = create_app()
    >>> db_manager.init_db(app)
    >>> with app.app_context():
    ...     db_manager.create_db()
    ...
    >>> exit()

Third : Set the master administrator mail address and password to .env file.

    MASTER_ADMIN_MAIL=<<your e-mail address>>
    MASTER_ADMIN_PASSWORD=<<your password>>

Fourth : run.

    python run.py

Then, access following url:  

[ThisWebAppPage - http://localhost:5100](http://localhost:5100)  

That's it. Enjoy!  
