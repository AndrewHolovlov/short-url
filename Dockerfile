FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update
RUN apt-get upgrade -y

WORKDIR /project

COPY requirements.txt /project
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . /project

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

RUN chmod -R 777 /project