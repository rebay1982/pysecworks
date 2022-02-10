FROM python:slim

RUN useradd pysecworks

WORKDIR /home/pysecworks

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY pysecworks.py config.py app.db entrypoint.sh ./
RUN chmod +x entrypoint.sh

ENV FLASK_APP pysecworks.py
ENV PORT 5000

RUN chown -R pysecworks:pysecworks ./
USER pysecworks

ENTRYPOINT ["./entrypoint.sh"]
