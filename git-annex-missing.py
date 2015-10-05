"""A simple script to check whether the content of a directory is
already inside git-annex. Warning: this is spaghetti code.
"""

import os
import hashlib


if __name__ == '__main__':

    annex_dir = '~/annex/'
    target_dir = '/tmp/'

    counter = 0
    hashes = {}

    print("Building the list of hashes in the annex_dir")
    for root, dirs, files in os.walk(annex_dir):
        if '.git' in root:
            continue  # exclude .git dir

        for file in sorted(files):
            filename = os.path.join(root, file)
            realname = os.path.realpath(filename)
            try:
                hash = os.path.basename(realname).split('-')[3].split('.')[0]
            except IndexError:
                print("Cannot find hash of %s , %s" % (filename, realname))
                continue

            if len(hash) != 64:
                print filename, hash
            else:
                # # check hash
                # if os.path.exists(filename):
                #     hash_computed = hashlib.sha256(open(realname).read()).hexdigest()
                #     if hash_computed != hash:
                #         print "HASH MISMATCH:", filename, hash, hash_computed
                #         stop

                if hash not in hashes:
                    hashes[hash] = filename
                # else:
                #     if 'archives' not in filename and 'archives' not in hashes[hash]:
                #         print('Duplicate entry: %s is also %s' % (filename, hashes[hash]))

                counter += 1
            if (counter % 1000) == 0:
                print counter

    print("Done.")
    print("Found %s different hashes" % len(hashes))
    print("")
    print("Checking the desired directory: %s" % target_dir)
    assert(os.path.exists(target_dir))
    for root, dirs, files in os.walk(target_dir):
        for file in sorted(files):
            filename = os.path.join(root, file)
            realname = os.path.realpath(filename)
            if os.path.exists(filename):
                hash_computed = hashlib.sha256(open(realname).read()).hexdigest()
                if hash_computed in hashes:
                    # print("%s in git-annex" % realname)
                    pass
                else:
                    print("%s NOT in git-annex" % realname)
