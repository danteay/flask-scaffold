# ------------------ Prepare Python environment ------------------ #

FROM python:3.9

ARG stage="dev"
ARG port="8000"
ARG aws_key
ARG aws_secret
ARG aws_region

ENV APP_NAME="lift-pass"
ENV STAGE=${stage}
ENV PORT=${port}
ENV AWS_ACCESS_KEY_ID=${aws_key}
ENV AWS_SECRET_ACCESS_KEY=${aws_secret}
ENV AWS_DEFAULT_REGION=${aws_region}

# ---------------  CONFIGURING NGINX  ------------------ #

RUN apt-get -y update && apt-get -y install nginx supervisor ruby && gem install erb

RUN rm /etc/nginx/sites-enabled/default
COPY nginx/site.conf.erb /site.conf.erb
RUN erb /site.conf.erb > /etc/nginx/sites-available/site.conf

RUN ln -s /etc/nginx/sites-available/site.conf /etc/nginx/sites-enabled/site.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN mkdir -p /var/log/supervisor
COPY nginx/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# --------------- FINISH NGINX CONFIG ------------------ #

ADD src /app/src
ADD data /app/data
COPY requirements.txt /app/requirements.txt
COPY app.py /app/app.py
COPY nginx/entrypoint.sh /app/entrypoint.sh

WORKDIR /app

RUN mkdir logs
RUN pip3 install --upgrade pip
RUN pip3 install gunicorn gevent
RUN pip3 install -r requirements.txt

EXPOSE ${port}

CMD sh /app/entrypoint.sh