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
reference_img = utils.read_image('/home/peter/Desktop/stain_norm/WSI_Normalizer/eg/standard.jpg')
normalizer = stainNorm_Vahadane.Normalizer()
normalizer.fit(reference_img)
print("finish normalizer fitting")


# define the function for parallel processing
def norm_image(img_path, save_folder_path):
    # defien the normalized image save path
    normalized_img_save_path = os.path.join(save_folder_path, img_path.split('/')[-1].split('.')[0] + '.jpeg')
    #/mnt/pathology/Histology/Annotation_new/tiles_512_20X_WhiteIsTumor_noOverlap_calibrate_Filtered/Images/CHS003-WSI02/*.jpeg

    # read the image and normalize it
    img = utils.read_image(img_path)
    normalized_img = normalizer.transform(img)
    
    # save the normalized image
    normalized_img = Image.fromarray(normalized_img)
    normalized_img.save(normalized_img_save_path)


# slide_patch_path_list = glob.glob("/data1/r20user3/shared_project/Hist2Cell/data/brca/*/patches_mag10_thre25/")
slide_patch_path_list = glob.glob("/mnt/pathology/Histology/Annotation_new/tiles_512_20X_WhiteIsTumor_noOverlap_calibrate_Filtered/Images/*/")
print("finish path list generation")

for slide_patch_path in slide_patch_path_list:
    # prepare the image path list that need to be normalized
    img_path_list = glob.glob(slide_patch_path+"*.jpeg")
    pbar = tqdm(img_path_list)

    # prepare the save folder path `patches_normed`
    # save_folder_path = os.path.join(os.path.dirname(os.path.dirname(slide_patch_path)), "patches_mag10_thre25_normed")
    save_folder_path = os.path.join('/mnt/pathology/Histology/Annotation_new/tiles_512_20X_WhiteIsTumor_noOverlap_calibrate_Filtered_Normed/Images', 
    slide_patch_path.split('/')[-2])

    os.mkdir(save_folder_path)
    
    # normalize the images in parallel and save them into destination path, here use 16 parallel processes
    print("Generating: " + save_folder_path)
    Parallel(n_jobs=16)(delayed(norm_image)(img_path, save_folder_path) for img_path in pbar)
