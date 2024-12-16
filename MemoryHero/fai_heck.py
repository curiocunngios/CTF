from hashlib import sha3_512


def forward(flag: str):
    data = flag.encode()
    for _ in range(16):
        data = sha3_512(data).digest()
    return data


def main():
    flag = input("Flag? ")
    if (
        forward(flag).hex()
        != "caea3d616441a086f78ef8e99ecbbbd450ae1fea5220470d922e1840ff58700eb5f087fc3e5feebe337c9102ed1491f37599b97982f33c649afcc0c0b35e5b9a"
    ):
        print("TwT")
        return
    print("UwU")


if __name__ == "__main__":
    main()
