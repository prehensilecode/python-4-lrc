#!/usr/local/bin/python3
import sys
import os
import hashlib
from pathlib import Path


def main():
    hash_dict = {}
    home_dir = Path(os.getenv('HOME'))
    pdir = home_dir / 'Pictures' / 'Masters' / 'Some Camera'
    photos = [x for x in pdir.iterdir() if (x.is_file() and x.name != '.DS_Store')]

    for p in photos:
        with open(p, 'rb') as photo:
            filehash = hashlib.blake2b()
            while chunk := photo.read(8192):
                filehash.update(chunk)
            hash_dict[p.name] = [(p, filehash.hexdigest())]

    with open('lrc_some_camera_201901_already_exist.txt', 'r') as f:
        for line in f:
            photofile = Path(line.strip())
            with open(photofile, 'rb') as photo:
                filehash = hashlib.blake2b()
                while chunk := photo.read(8192):
                    filehash.update(chunk)

            if photofile.name in hash_dict:
                hash_dict[photofile.name].append((photofile, filehash.hexdigest()))
            else:
                hash_dict[photofile.name] = [(photofile, filehash.hexdigest())]

    for k, v in hash_dict.items():
        if len(v) == 2:
            print(k, v)
        else:
            print('NO DUPE', k, v)


if __name__ == '__main__':
    main()
