import argparse, imagehash, time, os
from PIL import Image
from pprint import pprint
from multiprocessing import Pool
from db import Database

from dotenv import load_dotenv, find_dotenv
from pathlib import Path
load_dotenv(verbose=True)

class GuyaEye:

    def __init__(self, **kwargs):
        self.kwargs = kwargs

        self.images = self.kwargs['images']
        self.compare = self.kwargs['compare']
        self.threads = self.kwargs['threads']

        if self.images: self.create_database()
        elif self.compare: self.compare_image()
        else: print('[ ERROR ] Please select either "python src/main.py --images <directory>" or python src/main.py --compare <image>"!')

    def create_database(self):
        s = time.time()
        for dir, subdirs, files in os.walk(self.images):
            for i in range(len(files)): files[i] = os.path.join(self.images, files[i])
            pool = Pool(self.threads)
            
            hashes = pool.map(self.hash_image, files)
            
            self.db = Database()
            self.db.truncate()
            for hash in hashes:
                img, h = hash
                self.db.store_encoding(img, h)
        e = time.time()
        print('[ OK ] Took {:,.2f} seconds, {:,.2f} sec/image'.format(e - s, (e -s ) / len(hashes)))
    
    def compare_image(self):
        self.db = Database()
        l, h = self.hash_image(self.compare)
        res = self.db.compare_encoding(h)
        print(res)

    def hash_image(self, image):
        img = Image.open(image)
        return (image, imagehash.average_hash(img, hash_size=16))

    def compare_hash(self, h1, h2):
        return abs(h1 - h2)

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument('--images', type=str, default=False, help='Load directory of images into a database')
    args.add_argument('--compare', type=str, default=False, help='Compare image to the database')
    args.add_argument('--threads', type=int, default=4, help='Number of threads to use when generating the database')
    args = args.parse_args()

    GuyaEye(**vars(args))