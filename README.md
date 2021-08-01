# **Greyscaling_with_different_scientific_methods**

## In this repository I plan to shed some light on the different scientific methods developed to convert colored RGB images to greyscaled images and explore their respective codes 

### First lets start with how really we humans perceive colors and how are these colors actually represented in computers

Color fascinates me because it is less about physics than it is about the physiology and psychology of human perception. All our standards are determined by what humans perceive. The range that needs to be covered, the number of channels necessary to represent a color, the resolution with which a color must be specified, and hence the information density and storage requirements, all depend on human retinas and visual cortices.

It also means that, as with everything human, there is a great deal of variability. There are deficiencies like color blindness (I myself experience deuteranomaly, a type of red-green colorblindness) and there are those with unusual abilities, like tetrachromats, who have not three types of color receptors, but four, and can distinguish colors that the rest of us can’t. Because of this, keep in mind that all of the statements we can make about perception are generalizations only, and there will be individual differences.

Although photons vibrate at all frequencies, we have three distinct types of color-sensing cones, each with its characteristic frequency response, a particular color that it responds strongly to. That means that a combination of just three light sources with carefully chosen colors in carefully chosen intensities can make us experience any color that we're capable of seeing in the natural world. 

![image](https://user-images.githubusercontent.com/51722099/127757050-4a8497e7-19cb-481f-8a2e-4ca6e43e1fe3.png)

Each pixel in a screen is a triplet of a red, a green, and a blue light source, but when you look at them from far enough away they are too small for your eye to distinguish, and they look like a single small patch of color. One way to determine which color is produced is to specify the intensity levels of each of the light sources. Since the just noticeable difference (JND) in human perception of color intensity tends to stay in the neighborhood of one part in a hundred, using 256 discrete levels gives enough fine-grained control that color gradients look smooth. 

To recreate an entire image, computers use their reliable trick of simply chopping it up into small pieces. To make high quality images, it's necessary to make the pieces are so small that the human eye has trouble seeing them individually. 

![image](https://user-images.githubusercontent.com/51722099/127757121-44440137-4943-4ca0-9351-4d9581831f5a.png)

The color of each pixel can be represented as a 6-digit hex number or a triple of decimal numbers ranging from 0 to 255. During image processing it's customary to do the latter. For convenience, the red, green, and blue pixel values are separated out into their own arrays. 

A reliable way to read images into Python is with Pillow, an actively maintained fork of the classic Python Image Library or PIL, and Numpy. 
```
import numpy as np
from PIL import Image
img = np.asarray(Image.open("image_filename.jpg"))
```
When reading in a color image, the resulting object img is a three-dimensional Numpy array. The data type is often numpy.uint8, which is a natural and efficient way to represent color levels between 0 and 255. 
In order to facilitate calculations, I find it most convenient to convert the image values to floats between 0 and 1. In python3, the easiest way to do this is to divide by 255: img *= 1/255
Now we have all the image information in a compact collection of numbers. In our array, dimension 0 represents pixel rows, from the top to the bottom of the image. Dimension 1 represents columns from left to right. And dimension 2 represents color channels red, green, and blue, in that order. 

![image](https://user-images.githubusercontent.com/51722099/127757196-4df34088-fddf-44c5-a049-f83af5743f43.png)

special case is the grayscale image, where all three color channels for each pixel have the same value. Because of the repetition, it's more space efficient to store just one color channel, leaving the others implied. A two-dimensional array can also be used for monochrome images of any sort. By definition they have only one color channel. 
 For grayscale images, the result is a two-dimensional array with the number of rows and columns equal to the number of pixel rows and columns in the image. Low numeric values indicate darker shades and higher values lighter shades.
 
 ![image](https://user-images.githubusercontent.com/51722099/127757210-889a3b78-d210-4dcd-aff5-997f57300df3.png)

 An intuitive way to convert a color image 3D array to a grayscale 2D array is, for each pixel, take the average of the red, green, and blue pixel values to get the grayscale value. This combines the lightness or luminance contributed by each color band into a reasonable gray approximation.
```
img = numpy.mean(color_img, axis=2)
```
The axis=2 argument tells numpy.mean() to average values across all three color channels. (axis=0 would average across pixel rows and axis=1 would average across pixel columns.) 

![image](https://user-images.githubusercontent.com/51722099/127757251-a1926806-e4b9-41ee-a6f3-a821fd73efeb.png)

### channel-dependent luminance perception

To our eyes green looks abount ten times brighter than blue. Through many repetitions of carefully designed experiments, psychologists have figured out how different we perceive the luminance or red, green, and blue to be. They have provided us a different set of weights for our channel averaging to get total luminance. 

![image](https://user-images.githubusercontent.com/51722099/127757257-4faded4e-8521-4f15-90ac-4c651778f411.png)

![image](https://user-images.githubusercontent.com/51722099/127757261-57a81638-44f4-4715-b47f-8ab3db99e2a0.png)

### gamma compression

 We are able to see small differences when luminance is low, but at high luminance levels, we are much less sensitive to them. In order to avoid wasting effort representing imperceptible differences at high luminance, the color scale is warped, so that it concentrates more values in the lower end of the range, and spreads them out more widely in the higher end. This is called gamma compression.

To undo the effects of gamma compression before calculating the grayscale luminance, it's necessary to apply the inverse operation, gamma expansion: 

![image](https://user-images.githubusercontent.com/51722099/127757269-2017e5e4-0df2-4cb3-a6c3-adb41409c9be.png)

The benefit of gamma compression is that it gets rid of banding in smoothly varying dark colors, like a photo of the sky at twilight. The downside is that if we want to do anything like adding, subtracting, or averaging bands, we first have to undo the compression and get the luminance back into a linear representation. 

![image](https://user-images.githubusercontent.com/51722099/127757279-cf2ab070-c471-4333-9754-04cbd05f9b1f.png)

There is lightening throughout the image after accounting for gamma compression. It brings the luminance up to be a closer match to that of the original image. Finally, we have a high quality grayscale representation. 

### linear approximation

 The gamma decompresssion and re-compression rack up quite a large computation cost, compared to the weighted averages we were working with before. Sometimes speed is more desirable than accurate-as-possible luminance calculations. For situations like these, there is a linear approximation:

![image](https://user-images.githubusercontent.com/51722099/127757288-21104407-2620-497d-bd8f-7b2d5374e5b9.png)

This lets you get a result that's a little closer to the gamma-compression-corrected version, but without the extra computation time. 

![image](https://user-images.githubusercontent.com/51722099/127757292-ad5a5543-5add-4c79-ab67-8cd29a60972a.png)

 As you can see, the results are not bad at all. They tend to be a little darker, especially through the red mid-range values, but arguably just as good in most practical respects.

This method of calculating luminance is codified in the standard ITU-R BT.601 Studio encoding parameters of digital television for standard 4:3 and wide screen 16:9 aspect ratios. which incidentally was awaded an Emmy in 1983. 

### Which one should I use?

If close is good enough or if you really care about speed, use the linear approximation of gamma correction. This is the approach used by MATLAB, Pillow, and OpenCV.
