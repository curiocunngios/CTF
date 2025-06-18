FROM ubuntu:24.10@sha256:102bc1874fdb136fc2d218473f03cf84135cb7496fefdb9c026c0f553cfe1b6d

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y socat && rm -r /var/lib/apt/lists/*

WORKDIR /app
ADD guess-the-number .
ADD flag.txt .
RUN chmod 644 /app/flag.txt

USER ubuntu

CMD ["socat", "TCP-LISTEN:3000,fork,reuseaddr", "EXEC:/app/guess-the-number"]

