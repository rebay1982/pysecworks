#!/bin/bash
source venv/bin/activate
exec gunicorn -b :${PORT} --access-logfile - --error-logfile - pysecworks:app
