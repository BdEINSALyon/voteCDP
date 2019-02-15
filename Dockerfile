FROM python:3.6
EXPOSE 8000

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . /app
ENV DATABASE_URL postgres://cdp@db/cdp
ENV SECRET_KEY ''
ENV DJANGO_ENV 'prod'
ENV MAILGUN_URL ''
ENV MAILGUN_KEY ''
ENV FROM_EMAIL ''
ENV RETURN_LINK ''
ENV OPENING="Tue May 29 00:01:00 GMT+2 2018"
ENV CLOSING="Mon Jun 4 23:59:00 GMT+2 2018"
RUN chmod +x bash/run-prod.sh
CMD bash/run-prod.sh