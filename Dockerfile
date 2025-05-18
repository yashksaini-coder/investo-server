FROM python:3.11-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 4000

CMD ["fastapi", "run", "app.py", "--port", "4000"]