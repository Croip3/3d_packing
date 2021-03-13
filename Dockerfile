FROM python:3.8.0-buster

WORKDIR /3d_packing
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]
