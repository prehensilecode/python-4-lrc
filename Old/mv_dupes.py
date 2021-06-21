#!/usr/local/bin/python3
import sys
import os
import shutil
from pathlib import Path

home_dir = Path(os.getenv('HOME'))
destdir = home_dir / 'Tmp' / 'LightRoomDupes' / 'SomeCamera' / 'DefiniteDupes'

print(f'destdir = {destdir}')

with open('somecamera__definite_dupes.txt', 'r') as f:
    for line in f:
        filename = Path(line.strip()).name
        dest = destdir / filename
        shutil.move(line.strip(), dest)

