For a quick start on histolgoy image color normalization, here are 4 examples:
- `color_norm_single_process.py`:
    - basic use of the color normalization;
    - for your own use, you can select the `reference image` you want, and define your own list of images need to be normalizaed;
- `color_norm_parallel_process.py`:
    - faster color normalization using multi process; (recommended)
- `color_norm_parallel_brca_patches.py`:
    - use one sample *patch* from `her2st` as reference image;
    - iterate cases in TCGA-BRCA, for every case, normalize images in `patches` folder and store normalized images in `patches_normed` folder;
    - use multi process with 16 workers.
- `color_norm_parallel_stnet_wholeslide.py`:
    - use one sample *whole slide image* from `her2st` as reference image;
    - iterate *whole slide images* in `stnet`, normalize the images and store normalized images as `case_id_norm.png`;
    - use multi process with 16 workers. (Maybe it is better to first normalize the whole slide image, then crop the patches from the normalized whole slide image)

In the examples, I use `stainNorm_Vahadane` method for color normalization, you can also use other 2 methods if you like.



### add white image solution
when there is white image detected, just return the white image, code change in line 57 in `/data1/r20user3/StainTools/stainNorm_Vahadane.py`
```
################################################################################################################
# add this line to avoid the white image error, just return the white image
mask = ut.notwhite_mask(I, thresh=0.8).reshape((-1,))
OD = ut.RGB_to_OD(I).reshape((-1, 3))
OD = OD[mask]
if OD.shape[0] == 0:
    return I
################################################################################################################
```
A simple example in `/data1/r20user3/StainTools/color_norm_parallel_stnet_wholeslide.py`.

### test white background ratio in image
In `/data1/r20user3/StainTools/create_white_img.ipynb`, we can see how to get the ratio of white background of different images, there are some quick start examples.
