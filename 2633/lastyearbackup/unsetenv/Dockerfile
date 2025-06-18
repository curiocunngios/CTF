FROM ubuntu@sha256:145bacc9db29ff9c9c021284e5b7b22f1193fc38556c578250c926cf3c883a13

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    socat \
    git \
    gdb \
    python3 \
    python3-pip \
    python3-dev \
    wget \
    make \
    && rm -r /var/lib/apt/lists/*

# Install pwndbg
RUN cd /opt \
    && git clone https://github.com/pwndbg/pwndbg \
    && cd pwndbg \
    && ./setup.sh

RUN echo "source /opt/pwndbg/gdbinit.py" > ~/.gdbinit

RUN apt-get install -y python3-pwntools

RUN apt-get update && apt-get install -y socat gdbserver

# Start your binary with gdbserver
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"gdbserver localhost:12345 ./spawn"

WORKDIR /app
ADD unsetenv .
ADD spawn .
ADD flag.txt .
RUN chmod -R 755 /app && chmod 000 /app/flag.txt && chmod u+s /app/spawn

RUN for s in $(tail -n +2 /etc/shells); do rm -f $s; done



USER ubuntu

CMD ["socat", "TCP-LISTEN:3000,fork,reuseaddr", "EXEC:/app/spawn"]
