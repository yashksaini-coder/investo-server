FROM python:3.9-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

ENV GROQ_API_KEY=your_api_key

RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

CMD ["fastapi", "run", "app.py", "--port", "80"]