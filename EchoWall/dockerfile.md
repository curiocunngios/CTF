Ah, I understand better now. There are two different scenarios here:

1. What you were doing first (getting libc files):
```bash
sudo docker run -it --rm -v $(pwd):/chal --platform linux/amd64 ubuntu:22.04
```
This just creates a temporary container to access Ubuntu 22.04's files/libc.

2. What the other person is suggesting (running the challenge locally):
If you have the challenge files and a Dockerfile from the CTF, you can:

```bash
# Build the challenge environment
sudo docker build -t echowall .    # assuming you're in directory with Dockerfile

# Run ("spin up") the challenge locally
sudo docker run -p 1337:1337 -it echowall    # adjust port as needed
```

Then you can test your exploit locally by connecting to localhost:1337 before trying it on the remote server.

But if you weren't given a Dockerfile with the challenge, you can't do the second part. You can only use Docker to get the matching libc version as you were doing originally.

Do you have a Dockerfile in your challenge files? If not, stick with just using Docker to get the libc files.