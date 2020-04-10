# Stereo Vision: 3D Reconstruction from 2D Images

Many complex tasks in computer vision involve obtaining three-dimensional coordinates of an object. This project uses mathematical relationships along with various software tools to create a 3D image from two 2D images. 

## Theory

The motivation for computer stereo vision comes from stereopsis, which is how human eyes perceive depth. Through the left and right eyes, humans see the same object in slightly different ways; this is due to the effect of parallax, where the apparent position of an object changes based on the angle of the line of sight. With the distance between two eyes and the displacement of the object position in each eye, trigonometry and ratios can be used to gain depth. 

To obtain a 3D image using computer stereo vision, one must have access to two, flat 2D images as well as calibration values for the cameras with which the images were obtained. Two cameras, positioned a known distance apart, mimic the human eyes; they capture the same scene, which are offset due to the difference in line of sight. The binocular disparity (further referred to as "disparity"), is defined as the pixel distance of the same image point in the two images:

_**d** = xl - xr_ 

where _xl_  and _xr_
are the pixel x-coordinate of the image point in the left and right images, respectively. Assuming that the object is located at __P(x, y, z)__ as defined in Figure 1, the following proportionality relationships can be applied to calculate the z-coordinate, or the depth:

__Left image__:	_x / z = xl / f_

__Right image__: 	_(x - b) / z = xr / f_

where _b_ is the distance between the two cameras, and _f_ refers to the focal length of the cameras. Combining these two equations, the _z_ can be calculated:

_**z**= (b * f) / (xl - xr)_

The most important task comes in calculating the disparity between each point in the two images. A very useful technique that can be used to obtain disparity is region matching. The process involves creating a window around each pixel in the left image, and finding a window in the right image which matches it the most closely. Here, it is assumed that the two cameras were positioned at identical heights, which eliminates the need for pixels outside of the row to be examined during this step. The resulting matrix of disparity values allows for a complete 3D reconstruction of the image using x-, y-, and z-coordinates.

(see References)

![Proportionality Diagram](https://user-images.githubusercontent.com/46095808/78978830-74865100-7acf-11ea-935b-0fc11ce33a37.png)

## Process

The left and right images were obtained from the 2014 Middlebury Stereo Dataset.

(see References) 

![image_left](https://github.com/youngseok-seo/stereo-vision/blob/master/data/images/im0.png)

### Pre-processing

The original images were 2864 x 1924, with RGB values. The image was downloaded and converted to grayscale with the Python Pillow image processing library. As the resolution was quite high, the image was resized to ⅛ of the original dimensions to drastically reduce runtime. For further analysis, the intensity values were used to create a NumPy array. A _Process_ class was created to handle these procedures (see `process.py`). 

### Calculating Disparity

The __Sum of Absolute Differences (SAD)__ approach was applied to calculate the difference between each pixel inside the two windows (left and right). The pixel in the right image whose window has the smallest SAD value was considered to be the matching pixel, and the distance to that pixel was taken as the disparity. 
 
The SAD method was selected over other methods (e.g. correlation coefficient) for higher accuracy as well as enhanced runtime. The `data/images/calib.txt` file included in the images' source folder provided a conservative search range for region matching (_ndisp_), which was scaled down proportionally to the resized image. As the points in the right image generally displayed a shift in the negative x-direction, the range was chosen as __[- (ndisp * scale_factor), 0]__. The possibility of searching in both positive and negative directions was explored, but resulted in extended runtime and more noise. 

![raw_plot](https://github.com/youngseok-seo/stereo-vision/blob/master/data/output/250p_SAD_disp_raw_MPL.png)

### Post-processing

The resulting plot contained areas of noise and discontinuities, which called for a set of post-processing procedures. 

The noisy pixels were assumed to originate from the "flat" areas, where the disparity values were spiking due to most SAD values being very similar. In order to capture and "denoise" these values, the following steps were introduced:

__Denoising by mode__:
1. Check if the pixel's disparity value exceeds a threshold (>25).
2. If the pixel meets the above criteria, create a relatively large window around the pixel.
3. Calculate the mode (most common value) in the window, and assign it to the pixel.

In order to account for the discontinuous regions among pixels, the following method was utilized for every pixel:

__Smoothing by average__: 

Inside a small window, the average disparity value was calculated. This was compared to the disparity of the pixel in the center, and if the difference was greater than 5 units, the average value was assigned to the pixel. This created a "smoothing" effect, allowing for a more gradual change between two regions.

Furthermore, in order to remove any extraneous noise pixels unaffected by the mode and average methods, all pixels with disparity larger than a threshold was set to a fixed value. This allowed for more distinction between the points of interest during testing as well. 

__After Thresholding__:

![thresh_plot](https://github.com/youngseok-seo/stereo-vision/blob/master/data/output/250p_SAD_disp_thresh_MPL.png)

__After Thresholding and Smoothing__:

![avg_thresh_plot](https://github.com/youngseok-seo/stereo-vision/blob/master/data/output/250p_SAD_disp_avg_thresh_MPL.png)

__After Thresholding, Smoothing, and Denoising__:

![mode_avg_thresh_plot](https://github.com/youngseok-seo/stereo-vision/blob/master/data/output/250p_SAD_disp_mode_avg_thresh_MPL.png)

The set of post-processing procedures can be executed repeatedly to obtain better images.

__After 3 Iterations__:

![3_plot](https://github.com/youngseok-seo/stereo-vision/blob/master/data/output/250p_3layer.png)

__After 5 Iterations__:

![5_plot](https://github.com/youngseok-seo/stereo-vision/blob/master/data/output/250p_5layer.png)

### Obtaining Depth

The following formula, an adaptation of the equation shown in __Theory__ to match the constants listed in `data/images/calib.txt`, can used to calculate the depth value for each pixel.

_**z** = (b * f) / (disparity + doffs)_

## Results

The resulting coordinate values, as well as the RGB values from the original resized image, were collected in a .txt file (see `data/output/`). The information was entered into Cloud Compare, an open source point cloud reconstruction software. 

![gif](https://github.com/youngseok-seo/stereo-vision/blob/master/3D.gif)

## Execution

```
python3 stereo.py
```

## References

https://www.cse.usf.edu/~r1k/MachineVisionBook/MachineVision.files/MachineVision_Chapter11.pdf

http://vision.middlebury.edu/stereo/data/scenes2014/

