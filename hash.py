#!/usr/bin/env python3
import hashlib
import os
import pathlib
import queue
import threading



class DuplicateFinder:

    def __init__(self, files=None):
        self.files = queue.Queue(files)
        self.hashes = dict()
        self._lock = threading.Lock()

    
    # Add hash as dictionary key
    def add_hash(self, hash, filepath):

        # Lock execution to prevent concurrency mess (bottleneck?)
        with self._lock:
            # Confirm then add
            if not self.hashes.get(hash, False):
                self.hashes[hash] = [filepath]
            else:
                self.hashes[hash].append(filepath)
    

    # Add filepath to list with hash
    def add_file(self, filepath, hash):
        self.hashes[hash].append(filepath)

            

# Make Queue of files in directory (recursive)
def get_files(directory):

    files = queue.Queue()
    for basepath, __, filenames in os.walk(directory):
        for file in filenames:
            filepath = str(pathlib.PurePath(os.path.join(basepath, file)))
            files.put(filepath)

    return files



def md5sum(filename):

    h = hashlib.md5()
    b = bytearray(128 * 1024)
    mv = memoryview(b)

    with open(filename, "rb", buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    
    return h.hexdigest()



def sha256sum(filename):

    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)

    with open(filename, "rb", buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    
    return h.hexdigest()



def main():
    
    directory = str(pathlib.Path(args.directory))



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "directory",
        help="file to hash"
    )

    args = parser.parse_args()

    main()
