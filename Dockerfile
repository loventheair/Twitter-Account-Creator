FROM python:3.9

WORKDIR /app

COPY ./requirments.txt /app

RUN python -m pip install -r requirments.txt

COPY . /app/

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]