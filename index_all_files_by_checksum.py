#!/usr/local/bin/python3.9
import sys
import os
from pathlib import Path
import hashlib
import pickle

# index_all_files_by_checksum.py - walks the LrC Masters directory and
#     calculates hash for all files (photos)
# Copyright (C) 2021  David Chin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

debug_p = False


def main():
    global debug_p

    # Lightroom Classic's masters folder
    home_dir = Path(os.getenv('HOME'))
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
                if f != '.DS_Store':
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


if __name__ == '__main__':
    main()
