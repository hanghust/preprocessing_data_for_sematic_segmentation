# import matplotlib.pyplot as plt
# # from skimage.util import img_as_ubyte
# # from skimage import io
from skimage.morphology import erosion, dilation
# # from skimage.morphology import black_tophat, skeletonize, convex_hull_image
from skimage.morphology import disk
# from PIL import Image
# import numpy as np
# from skimage.util import img_as_ubyte

import matplotlib.pyplot as plt
from skimage import data
from skimage.util import img_as_ubyte
# from skimage import io

orig_phantom = img_as_ubyte(data.shepp_logan_phantom())
fig, ax = plt.subplots()
ax.imshow(orig_phantom, cmap=plt.cm.gray)

def plot_comparison(original, filtered, filter_name):

    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4), sharex=True,
                                   sharey=True)
    ax1.imshow(original, cmap=plt.cm.gray)
    ax1.set_title('original')
    ax1.axis('off')
    ax2.imshow(filtered, cmap=plt.cm.gray)
    ax2.set_title(filter_name)
    ax2.axis('off')

# image = Image.open('/home/hangnt/hangnt/1102_export_features/amp49_vis/2018_04_0002_000116_prediction.png')
# image = img_as_ubyte(image)
selem = disk(6)
eroded = erosion(orig_phantom, selem)
plot_comparison(orig_phantom, eroded, 'erosion')



