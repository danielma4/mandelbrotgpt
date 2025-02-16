FROM python:3.10

#system deps 
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

#django commands
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "MathEQGPT.wsgi:application"]