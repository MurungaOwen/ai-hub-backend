## Setup
```py
pip install -r requirements.txt
```
## start server: 
``` py
python manage.py runserver
```

## Api documentation
``` curl
http://localhost:8000/api/v1/docs
```

## Also run
```py
python manage.py seed_courses
```
- This populates db with some courses and Quizzees described [here](lesson\management\commands\seed_courses.py)