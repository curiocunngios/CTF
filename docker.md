# Getting libc from docker

## If there's the version 
```
FROM ubuntu:20.04
```
`docker run -it --rm -v $(pwd):/chal --platform linux/amd64 <image version>`

Example: `docker run -it --rm -v $(pwd):/chal --platform linux/amd64 ubuntu:20.04`

- The parameter `–v $(pwd):/chal` will “link” your local folder to `/chal` file in the container

`cp /lib/x86_64-linux-gnu/libc.so.6 /chal`

- `/lib/x86_64-linux-gnu/libc.so.6` is the  common libc.so.6 file path 

## If there's a hash 

```
FROM ubuntu@sha256:145bacc9db29ff9c9c021284e5b7b22f1193fc38556c578250c926cf3c883a13
```

`docker run -it -v $PWD:/mnt --rm ubuntu@sha256:<hash> bash`


# Building the docker environment

`docker image build -t pwn .`

## Running the docker container (challenge container)

`sudo docker run --name pwn_debug -p 1337:3000 -it pwn`

## Debugging with pwntools 

- install pwntools in the docker environment

```py
from pwnlib.util.misc import run_in_new_terminal
r = remote('127.0.0.1', <local_port>)
sleep(0.1)

pid = pidof(<process_name>)[0]
script = '''
'''
run_in_new_terminal(f'gdb -p {pid} -ex {script}')
```


### By installing pwndbg inside docker
Modify the dockfile with the following and build it 
```docker
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
```

### Executing a script inside the docker environment
```
# First, copy your exploit script into the container
docker cp solve.py container_name:/app/

# Using it 
sudo docker exec -it pwn_debug python3 /app/solve.py
```

