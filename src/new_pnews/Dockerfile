
FROM python:3.12.1-bookworm

WORKDIR /app

RUN wget -O googlechrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt update && apt upgrade -y
RUN apt install -f ./googlechrome.deb -y

RUN pip install selenium webdriver-manager

COPY . .

CMD [ "python", "__main__.py" ]
