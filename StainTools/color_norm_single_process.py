import os
import time
import csv
import glob
import pandas as pd
import stainNorm_Vahadane
import stain_utils as utils
from PIL import Image
from tqdm import tqdm

# prepare the image path list that need to be normalized
img_path_list = glob.glob("/data1/r20user3/StainTools/data/i*.png")
print(img_path_list)

# prepare the normalizer with the reference histology image
reference_img = utils.read_image('./data/i1.png')
normalizer = stainNorm_Vahadane.Normalizer()
normalizer.fit(reference_img)

# normalize the images one by one and save them into destination path
since = time.time()
for img_path in tqdm(img_path_list):
    # defien the normalized image save path
    normalized_img_save_path = os.path.join("/data1/r20user3/StainTools/data", img_path.split('/')[-1].split('.')[0] + '_normed.png')

    # read the image and normalize it
    img = utils.read_image(img_path)
    normalized_img = normalizer.transform(img)

    # save the normalized image
    normalized_img = Image.fromarray(normalized_img)
    normalized_img.save(normalized_img_save_path)

# print the time cost
time_elapsed = time.time() - since
print('Evaluation completed in {:.0f}m {:.0f}s.'.format(time_elapsed // 60, time_elapsed % 60))