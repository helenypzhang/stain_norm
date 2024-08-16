import os
import time
import csv
import glob
import pandas as pd
import stainNorm_Vahadane
import stain_utils as utils
from PIL import Image
from tqdm import tqdm

# prepare the white image need to be normalized
img = utils.read_image("/data1/r20user3/StainTools/debug_data/white_image.png")

# prepare the normalizer with the reference histology image
reference_img = utils.read_image('/data1/r20user3/StainTools/debug_data/96_19.jpeg')
normalizer = stainNorm_Vahadane.Normalizer()
normalizer.fit(reference_img)

normalized_img = normalizer.transform(img)

# save the original white image image
normalized_img = Image.fromarray(normalized_img)
normalized_img.save('/data1/r20user3/StainTools/debug_data/white_image_normed.png')