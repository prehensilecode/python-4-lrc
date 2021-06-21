#!/usr/local/bin/python3.9
import sys
import os
from pathlib import Path
import hashlib
import pickle

debug_p = False

home_dir = Path(os.getenv('HOME'))
base_dir = home_dir / '/Pictures/Masters/'

ds_store = '.DS_Store'

masters_dir = Path(home_dir) / 'Pictures' / 'Masters'
hash_index = {}
for root, dirs, files in os.walk(masters_dir):
    if debug_p:
        print('root', root)
        print('dirs', dirs)
        print('files', files)
        print('')

    if files:
        for f in files:
            file_path = Path(root) / f
            with open(file_path, 'rb') as photo:
                filehash = hashlib.blake2b()
                filehash.update(photo.read())
                if filehash.hexdigest() not in hash_index:
                    hash_index[filehash.hexdigest()] = [Path(file_path)]
                else:
                    hash_index[filehash.hexdigest()].append(Path(file_path))

for k, v in hash_index.items():
    if len(v) > 1:
        print('DUPE: ', k, v)

with open('all_photo_hashes.pickle', 'wb') as f:
    pickle.dump(hash_index, f)
