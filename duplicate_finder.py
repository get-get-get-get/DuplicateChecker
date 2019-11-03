#!/usr/bin/env python3
import collections
import hashlib
import os
import pathlib
import queue
import threading


class DuplicateFinder:

    max_threads = 10

    def __init__(self, directory):
        self.directory = str(pathlib.Path(directory))
        self.file_hashes = dict()
        self.duplicates = dict()

    # Thread worker, managed by hash_files
    def check_files(self, files, hashed):

        # Store hash results as namedtuple
        HashedFile = collections.namedtuple("HashedFile", ["hash", "file"])

        while not files.empty():
            file = files.get()
            file_hash = md5sum(file)
            # Store result
            hf = HashedFile(file_hash, file)
            hashed.append(hf)

    # Deletes all duplicates but the one with shortest path
    def delete_duplicates(self):

        # Delete duplicates
        for file_hash, files in self.duplicates.items():
            # Sort by len
            files.sort(key=len)

            # Remove file to be kept
            keep = files.pop(0)
            print(f"KEPT ==> {keep}")
            # Delete each redundant item
            for file in files:
                os.remove(file)
                print(f"DELETED ==> {file}")
            
            # Update self.file_hashes 
            self.file_hashes[file_hash] = [keep]
        
        # Clear duplicates
        self.duplicates.clear()

      

    # Find duplicates in directory
    # Main function
    def find_duplicates(self):

        files = get_files(self.directory)
        print(f"Found {files.qsize()} files")

        # hashed is a list of HashedFile('hash', 'file') tuples
        hashedfiles = self.hash_files(files)
        self.process_hashed_files(hashedfiles)

        # Find where hash matches multiple files
        for file_hash, file_list in self.file_hashes.items():
            if len(file_list) > 1:
                self.duplicates[file_hash] = file_list

        return self.duplicates

    # Get hashes of all files
    def hash_files(self, files):

        # Queue for storing results
        hashed_files = []

        workers = []
        for n in range(self.max_threads):
            # Create thread and add to dictionary (hacky...)
            t = threading.Thread(target=self.check_files,
                                 args=(files, hashed_files,))

            # Run thread
            t.start()
            workers.append(t)

        for worker in workers:
            worker.join()

        return hashed_files

    # Given list of namedtuples (HashedFile('hash', 'file')), adds to self.hashes
    def process_hashed_files(self, hashedfiles):

        for hf in hashedfiles:
            if self.file_hashes.get(hf.hash, False):
                self.file_hashes[hf.hash].append(hf.file)
            else:
                self.file_hashes[hf.hash] = [hf.file]

    # Print duplicates in readable format
    def show_duplicates(self):

        for file_hash, file_paths in self.duplicates.items():
            print(file_hash)
            for file_path in file_paths:
                print("\t%s" % file_path)


# Make Queue of files in directory (recursive)
def get_files(directory):

    files = queue.Queue()
    for basepath, __, filenames in os.walk(directory):
        for file in filenames:
            file_path = str(pathlib.PurePath(os.path.join(basepath, file)))
            files.put(file_path)

    return files


def md5sum(filename):

    h = hashlib.md5()
    b = bytearray(128 * 1024)
    mv = memoryview(b)

    with open(filename, "rb", buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])

    return h.hexdigest()


def main():

    finder = DuplicateFinder(args.directory)
    finder.max_threads = args.threads
    finder.find_duplicates()
    finder.show_duplicates()

    if args.delete:
        finder.delete_duplicates()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "directory",
        help="file to hash"
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete redundant files based on path length (keep shortest). Stupid/dangerous"
    )
    parser.add_argument(
        "-t",
        "--threads",
        default=10,
        type=int,
        help="Threads used for hashing"
    )

    args = parser.parse_args()

    main()
