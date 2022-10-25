Estimation of the queue and dynamic traffic densities at a road crossing using OpenCV.

Utility-Runtime Trade-Off Analysis

For utility-runtime trade-off analysis, we have the following methods/parameters:
Method 1:

Sub-sampling frames -- processing every x frame i.e. process frame N and then frame N+x, and for all intermediate frames just use the value obtained for N - total processing time will reduce, but utility might decrease as intermediate frames values might differ from baseline. Parameter for this method is x, how many frames you drop.


Method2:
Reduce resolution for each frame. Lower resolution frames might be processed faster, but having higher errors. Parameter can be resolution XxY.

Method3: 
Split work spatially across threads (application level pthreads) by giving each thread part of a frame to process. Parameter can be number of threads, if each thread gets one split.



The code takes the source image as input and the user is asked to select four points on the shown image. After selecting four points, the projected image is displayed by performing homography using the user's selected set of points and a seperate set of points already present in the code. Another homography is performed between user's selected points and the four corner of the final cropped image. Corresponding windows are shown for the outputed images.


