import os
import glob
from joblib import Parallel
from tqdm import tqdm
import stainNorm_Vahadane
import stain_utils as utils
from PIL import Image
from joblib import delayed
os.environ['KMP_WARNINGS'] = 'off'

# prepare the normalizer with the reference histology image
reference_img = utils.read_image('./data/i1.png')
normalizer = stainNorm_Vahadane.Normalizer()
normalizer.fit(reference_img)

# define the function for parallel processing
def norm_image(img_path):
    # defien the normalized image save path
    normalized_img_save_path = os.path.join("/data1/r20user3/StainTools/data", img_path.split('/')[-1].split('.')[0] + '_normed.png')

    # read the image and normalize it
    img = utils.read_image(img_path)
    normalized_img = normalizer.transform(img)

    # save the normalized image
    normalized_img = Image.fromarray(normalized_img)
    normalized_img.save(normalized_img_save_path)

# prepare the image path list that need to be normalized
img_path_list = glob.glob("/data1/r20user3/StainTools/data/i*.png")
pbar = tqdm(img_path_list)

# normalize the images in parallel and save them into destination path, here use 4 parallel processes
# for faster processing, you can change the n_jobs to 8, 16, 32
Parallel(n_jobs=4)(delayed(norm_image)(img_path) for img_path in pbar)