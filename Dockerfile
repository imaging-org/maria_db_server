FROM python as compiler
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y && apt-get dist-upgrade -y

RUN apt-get install -y python3-dev
RUN apt-get install -y openssl
RUN apt-get install -y libmariadb-dev
RUN apt-get install -y libmariadb3

WORKDIR /app/

RUN python -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install mariadb==1.1.10
RUN pip install -Ur requirements.txt

FROM python:3.11.5-alpine3.18 as runner
WORKDIR /app/
COPY --from=compiler /opt/venv /opt/venv

# Enable venv
ENV PATH="/opt/venv/bin:$PATH"
COPY . /app/
EXPOSE 7171
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]