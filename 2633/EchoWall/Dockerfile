FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \ 
    apt-get install -y socat && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -M firebird

WORKDIR /app
COPY --chown=root src/EchoWall .
COPY --chown=root src/flag.txt .
RUN chmod 755 /app && chmod 755 EchoWall && chmod 644 flag.txt

USER firebird
CMD ["socat", "TCP-LISTEN:3000,fork,reuseaddr", "EXEC:./EchoWall,stderr"]
EXPOSE 3000
