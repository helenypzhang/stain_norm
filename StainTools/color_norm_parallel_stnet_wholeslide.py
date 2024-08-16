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
reference_img = utils.read_image('/data1/r20user3/shared_project/Hist2Cell/data/her2st/A1/A1.jpg')
normalizer = stainNorm_Vahadane.Normalizer()
normalizer.fit(reference_img)

# define the function for parallel processing
def norm_image(slide_path):
    # defien the normalized image save path
    normalized_img_save_path = os.path.join(os.path.dirname(slide_path), "norm_" + os.path.basename(slide_path))
    
    # read the image and normalize it
    img = utils.read_image(slide_path)
    normalized_img = normalizer.transform(img)
    
    # save the normalized image
    normalized_img = Image.fromarray(normalized_img)
    normalized_img.save(normalized_img_save_path)


slide_path_list = [path for path in glob.glob("/data1/r20user3/shared_project/Hist2Cell/data/stnet/*/2*.jpg") if not path.endswith('view.jpg')]

pbar = tqdm(slide_path_list) 
Parallel(n_jobs=16)(delayed(norm_image)(slide_path) for slide_path in pbar)