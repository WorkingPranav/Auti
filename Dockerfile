FROM python:3.9.1-buster

RUN apt -qq update && apt -qq install -y git ffmpeg

RUN git clone https://github.com/kagutsuchi57/RenameBot /app

WORKDIR /app

RUN pip install -U -r requirements.txt

CMD [ "python", "start.sh" ]
