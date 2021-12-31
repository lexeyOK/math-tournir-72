FROM python:slim

WORKDIR /math-tournir
ENV FLASK_RUN_HOST=0.0.0.0

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000

COPY . .

RUN flask db init
RUN flask db migrate -m "Initial migration"
RUN flask db upgrade

CMD ["flask", "run"]