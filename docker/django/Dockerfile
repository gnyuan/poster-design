FROM python:3

ARG MYENV
ENV PYTHONUNBUFFERED=1

WORKDIR /backend
COPY ./backend/requirements.txt requirements.txt
RUN python3 -m pip install -i http://192.168.0.79:3141/root/pypi/+simple/ --trusted-host 192.168.0.79 -r requirements.txt

COPY ./backend .
RUN if [ "${MYENV}" = "prod" ]; then \
           echo "prod" && cp conf/docker.py conf/env.py; \
       else \
           echo "dev"; \
       fi

CMD ["daphne", "-b", "0.0.0.0", "-p", "9000", "fuadmin.asgi:application"]
