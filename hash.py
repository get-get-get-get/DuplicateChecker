#!/usr/bin/env python3
import hashlib



def sha256sum(filename):

    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)

    with open(filename, "rb", buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    
    return h.hexdigest()
          




def main():
    print(sha256sum(args.file))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "file",
        help="file to hash"
    )

    args = parser.parse_args()

    main()
