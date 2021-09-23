# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

EXPOSE 8080


# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]    