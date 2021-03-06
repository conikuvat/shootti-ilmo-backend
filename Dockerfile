FROM python:3.6
WORKDIR /usr/src/app
COPY requirements.txt requirements-production.txt /usr/src/app/
RUN groupadd -r shoottikala && useradd -r -g shoottikala shoottikala && \
    pip install --no-cache-dir -r requirements.txt -r requirements-production.txt
COPY . /usr/src/app
RUN env DEBUG=1 python manage.py collectstatic --noinput && \
    python -m compileall -q .
USER shoottikala
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
