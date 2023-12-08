FROM python:3.6-alpine

RUN adduser -D blog

WORKDIR /home/blog

COPY requirements.txt requirements.txt

RUN /bin/sh -c pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY blog.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP blog.py

RUN chown -R blog:blog ./
USER blog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]