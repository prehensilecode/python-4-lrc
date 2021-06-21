#!/usr/local/bin/python3
import sys
import os
from pathlib import Path
import hashlib
import shutil
import re

home_dir = Path(os.getenv('HOME'))
base_dir = home_dir / 'Pictures' / 'Masters' / 'Camera Roll Some Phone'

checksums = {}
with os.scandir(base_dir) as it:
    for entry in it:
        if entry.is_file():
            with open(entry, 'rb') as photo:
                filehash = hashlib.blake2b()
                filehash.update(photo.read())
                if filehash.hexdigest() not in checksums:
                    checksums[filehash.hexdigest()] = [Path(entry)]
                else:
                    checksums[filehash.hexdigest()].append(Path(entry))

years = ['2018', '2019']
months = range(1, 13)
month_dirs = []
for y in years:
    for month in months:
        d = Path(base_dir) / y / f'{month:02d}'
        if d.is_dir():
            month_dirs.append(Path(base_dir) / y / f'{month:02d}')

for dir in month_dirs:
    with os.scandir(dir) as it:
        for entry in it:
            if entry.is_file():
                with open(entry, 'rb') as photo:
                    filehash = hashlib.blake2b()
                    filehash.update(photo.read())
                    if filehash.hexdigest() not in checksums:
                        checksums[filehash.hexdigest()] = [Path(entry)]
                    else:
                        checksums[filehash.hexdigest()].append(Path(entry))

debug_p = False
definite_dupes = []
dupe_pat = re.compile(r'\ \(\d+\)')
if checksums:
    for k, v in checksums.items():
        if len(v) > 1:
            if debug_p:
                print('DUPE: ', k)
                print('    ', v[0])
                print('    ', v[1])

            if dupe_pat.search(str(v[0])):
                definite_dupes.append(v[0])
            elif dupe_pat.search(str(v[1])):
                definite_dupes.append(v[1])
        else:
            if debug_p:
                print('UNIQ: ', k, v[0])


for d in definite_dupes:
    print(d)
