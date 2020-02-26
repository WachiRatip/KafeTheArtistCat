FROM python:3.7.6

WORKDIR /work

ARG LINE_CHANNEL_ACCESS_TOKEN 
ARG LINE_CHANNEL_SECRET

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

COPY /app ./

CMD [ "python", "./app.py" ]