FROM python:3.8.1

ENV PYTHONUNBUFFERED 1
WORKDIR /app

#RUN python3 -m venv /opt/ENV

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

#RUN /opt/ENV/bin/pip install pip --upgrade && \
#    /opt/ENV/bin/pip install -r requirements.txt && \
#    chmod +x entrypoint.sh

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]

#CMD ["/app/entrypoint.sh"]

