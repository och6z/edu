```
$ git clone https://github.com/jrajmundtest/edu.git
$ cd edu
$ python3 -m venv venv
$ source venv/bin/activate
(venv)$ pip install -U pip
(venv)$ pip install wheel eggs
(venv)$ pip install -r requirements

(venv)$ export SECRET_KEY='your secret key'
(venv)$ export DATABASE_URI='mysql+pymysql://mysqluser:mysqlpassword@localhost/mysql_db'
(venv)$ export TEST_DATABASE_URI='mysql+pymysql://mysqluser:mysqlpassword@localhost/mysql_testdb'
(venv)$ export PRODUCTION_DATABASE_URI='mysql+pymysql://mysqluser:mysqlpassword@localhost/mysql_proddb'
(venv)$ export ENVIRONMENT='your environment'

(venv)$ python manage.py db init
(venv)$ python manage.py db migrate
(venv)$ python manage.py db upgrade

(venv)$ flask shell
>>>from app.models import User
>>>from app import db
>>>testuser=User(username="testuser",password="testpassword")
>>>db.session.add(testuser)
>>>db.session.commit()
>>>quit()

(venv)$ python run.py

```



