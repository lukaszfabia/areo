FROM python:3.12-silm-bookworm

WORKDIR /api

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "uvicorn", "app:main.py" ]
