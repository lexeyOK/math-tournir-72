FROM python:3.8

WORKDIR /math-tournir

COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000
run flask routes
CMD [ "python3 -m flask run" ]