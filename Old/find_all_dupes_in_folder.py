#!/usr/local/bin/python3
import sys
import os
from pathlib import Path
import hashlib
import shutil


home_dir = Path(os.getenv('HOME'))
base_dir = home_dir / 'Pictures' / 'Masters' / 'Camera Roll Some Camera')

years = ['2018', '2019']
months = range(1, 13)
month_dirs = []
for y in years:
    for month in months:
        d = Path(base_dir) / y / f'{month:02d}'
        if d.is_dir():
            month_dirs.append(Path(base_dir) / y / f'{month:02d}')

#for d in month_dirs:
#    print(d, d.is_dir())

dupes_maybe = []
with os.scandir(base_dir) as it:
    for entry in it:
        if entry.is_file():
            #print(entry.name, entry.path)

            for dir in month_dirs:
                potential_dupe = dir / entry.name
                if potential_dupe.is_file():
                    dupes_maybe.append(potential_dupe)


checksums = {}
for d in dupes_maybe:
    checksums[d.name] = []

    p1 = base_dir / d.name
    p2 = d

    if p1.is_file():
        with open(p1, 'rb') as photo:
            filehash = hashlib.blake2b()
            filehash.update(photo.read())
            checksums[d.name] = [(p1, filehash.hexdigest())]
    else:
        print(f'ERROR: {p1} does not exist')

    if p2.is_file:
        with open(p2, 'rb') as photo:
            filehash = hashlib.blake2b()
            filehash.update(photo.read())
            if checksums[d.name]:
                checksums[d.name].append((p2, filehash.hexdigest()))
            else:
                checksums[d.name] = (p2, filehash.hexdigest())
    else:
        print(f'ERROR: {p2} does not exist')

do_move_p = False

if do_move_p:
    dest_dir = home_dir / 'Tmp' / 'LightRoomDupes' / 'SomeCamera'
    print('')
    for k, v in checksums.items():
        # print(k, v)
        if len(v) == 2:
            if v[0][1] == v[1][1]:
                print(f'IDENTICAL FILES: {k} - {v[0][0], v[1][0]}')
                shutil.move(v[0][0], dest_dir / k)

