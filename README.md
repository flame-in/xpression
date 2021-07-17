# xpression-django

### Django framework for xPression Sentiment Analysis tool
_______________________________________________

* run django server can type the below in cmd

(cd-to-location-of-manage.py)>python manage.py runserver
C:\Users\escla\OneDrive\Desktop\xpression_project\server2.0>python manage.py runserver

or

for specific ip that is in ALLOWED_HOST = ['192.168.18.24:80','127.0.0.1:8000'] in setting.py in sentiment folder
C:\Users\escla\OneDrive\Desktop\xpression_project\server2.0>python manage.py runserver 192.168.18.24:80

________________________________

* .venv -> Virtual Environment
* .vscode -> VSCode settings

* projectname -> sentiment
* app name -> analysis


Start with 
```python

python manage.py runserver
#default port 8000
```
Admin page at localhost:8000/admin\
\
Super user admin account ->\
username = admin\
password = admin
