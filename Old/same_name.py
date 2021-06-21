#!/usr/local/bin/python3
import sys
import os
from pathlib import Path
import hashlib
import shutil

photo_list = []
counter = 0
with open('lrc_some_camera_201901_already_exist.txt', 'r') as f:
    for line in f:
        counter += 1
        photo = Path(line.strip())
        photo_name = photo.name
        photo_list.append((photo_name, photo))

print(counter, len(photo_list))
print('')

counts = {}
for p in photo_list:
    if p[0] in counts:
        counts[p[0]] += 1
    else:
        counts[p[0]] = 1
    print(p)

print('')

print(f'len(counts) = {len(counts)}')
chksums = {}
home_dir = Path(os.getenv('HOME'))
base_dir = home_dir / 'Pictures' / 'Masters' / 'Camera Roll Some Camera'
month_dir = base_dir / '2019' / '01'
for k, v in counts.items():
    if v > 1:
        print(k, v)

        p1 = base_dir / k
        p2 = month_dir / k

        if p1.is_file():
            with open(p1, 'rb') as photo:
                filehash = hashlib.blake2b()
                filehash.update(photo.read())
                chksums[k] = [filehash.hexdigest()]
        else:
            print(f'ERROR: {p1} does not exist')

        if p2.is_file():
            with open(p2, 'rb') as photo:
                filehash = hashlib.blake2b()
                filehash.update(photo.read())
                chksums[k].append(filehash.hexdigest())
        else:
            print(f'ERROR: {p2} does not exist')


dupe_dir = home_dir / 'Tmp' / 'LightRoomDupes' / 'SomeCamera' / '2019' / '01'
for k, v in chksums.items():
    print(k, v)
    if v[0] == v[1]:
        print(f'Moving {base_dir / k} to {dupe_dir / k}')
        shutil.move(base_dir / k, dupe_dir / k)

