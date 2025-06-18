FROM nikolaik/python-nodejs:python3.10-nodejs19

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ffmpeg ca-certificates gnupg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV NVM_DIR=/root/.nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash && \
    . "$NVM_DIR/nvm.sh" && \
    nvm install v18 && \
    nvm alias default v18 && \
    nvm use v18 && \
    npm install -g npm && \
    echo ". $NVM_DIR/nvm.sh" >> /root/.bashrc

WORKDIR /app
COPY . /app/

RUN pip3 install --no-cache-dir -U -r requirements.txt
RUN chmod +x /app/start

CMD ["bash", "-c", "source ~/.bashrc && bash start"]
