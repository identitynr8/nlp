This Django project I did for NLP fun. It has 2 applications:

1. "meter", that calculates sentiment score of a text (using VADER tool), and buzz score of a text (using
list of buzz words compiled from different sources);

2. "buzzifier", that is doing what essentially url shorteners are doing, except for it makes not the shortest
url, but the buzzed (http://www.google.com -> http://127.0.0.1:8000/r/business%20equation+agile+disruptive+focus%20on%20speed)

To play with it you should create virtual environment; install python packages in it (from `requirements/base.txt`);
run `bootstrap.py`, and django server in `project/`:

```
python manage.py migrate --settings project.settings.dev.settings
python manage.py runserver --settings project.settings.dev.settings
```

The project is not deployed anywhere now, but here are pictures of it's former glory:
[Buzzmeter](pics/buzzmeter.png)
[Sentiments meter](pics/sentiment_meter.png)
[Buzzifier](pics/buzzifier.png)
 