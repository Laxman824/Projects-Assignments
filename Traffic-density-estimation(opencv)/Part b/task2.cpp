/* 
Subtask2- Task 1 - C0P290
Using Background Subtractor and Optical Flow to calculate Queue and Dynamic density of vehicles using traffic camera's video as input
 */


#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/video/background_segm.hpp>

#include <iostream>
#include <fstream>

using namespace cv;
using namespace std;

int c = 0;


int main(int argc, char **argv)
{

    VideoCapture cap(argv[1]);
    if (!cap.isOpened())
    {
        cout << "Err : Couldnt read the video file. Check the path/extension" << endl;
        return -1;
    }

    Mat img = imread("background.png");
    if (!img.data)
    {
        cout << "Err : Couldnt read the image file. Check the path/extension" << endl;
        return -1;
    }

    Ptr<BackgroundSubtractor> backSubt = createBackgroundSubtractorMOG2();

    Mat fgMask;
    Mat img_cropped;
    Mat prev_mask;
    Mat flow;
    Mat frame;
    Mat cropped_frame;
    Mat h;

    float q_density_avg = 0, dy_density_avg = 0;
    float dy_pixels, dy_density, pixels, nonZeroPixels, q_density;

    vector<Point2f> img_points;
    vector<Point2f> crp_points;

    //ofstream MyFile("out.csv");
    ofstream MyTextFile("out.txt");

    cvtColor(img, img, COLOR_BGR2GRAY);

    //cropping background.png to create initial fgMask
    //Points start at top-left and go clockwise
    img_points.push_back(Point2f(937, 275));
    img_points.push_back(Point2f(1290, 267));
    img_points.push_back(Point2f(1535, 1047));
    img_points.push_back(Point2f(579, 1053));
    
    crp_points.push_back(Point2f(0, 0));
    crp_points.push_back(Point2f(400, 0));
    crp_points.push_back(Point2f(400, 800));
    crp_points.push_back(Point2f(0, 800));

    //Finding the homography matrix and using it for perspective correction
    Size size(400, 800);
    Mat h2 = findHomography(img_points, crp_points);
    warpPerspective(img, img_cropped, h2, size);

    backSubt->apply(img_cropped, fgMask,0);

    vector<Point2f> frame_p;
    vector<Point2f> crframe_p;

    while (1)
    {
        bool bSuccess = cap.read(frame);
        if (!bSuccess)
        {
            cout << "Fin" << endl;
            break;
        }

        cvtColor(frame, frame, COLOR_BGR2GRAY);

        frame_p.push_back(Point2f(968, 254));
        frame_p.push_back(Point2f(1308, 260));
        frame_p.push_back(Point2f(1551, 1065));
        frame_p.push_back(Point2f(587, 1065));

        crframe_p.push_back(Point2f(0, 0));
        crframe_p.push_back(Point2f(400, 0));
        crframe_p.push_back(Point2f(400, 800));
        crframe_p.push_back(Point2f(0, 800));

        h = findHomography(frame_p, crframe_p);
        warpPerspective(frame, cropped_frame, h, size);

        backSubt->apply(cropped_frame, fgMask, 0);
        //threshold(fgMask, fgMask, 128, 255, cv::THRESH_BINARY);  

        pixels = fgMask.rows * fgMask.cols;
        nonZeroPixels = countNonZero(fgMask);
        q_density = nonZeroPixels / pixels;
        q_density_avg += q_density;

        if (prev_mask.empty() == false)
        {
            //using Optical Flow to calculate relative displacement of pixels across 2 consecutive frames
            calcOpticalFlowFarneback(prev_mask, cropped_frame, flow, 0.5, 3, 15, 3, 5, 1.2, 0);

            Mat flow_parts[2];
            split(flow, flow_parts);
            Mat magnitude, angle, magn_norm;
            cartToPolar(flow_parts[0], flow_parts[1], magnitude, angle, true);
            normalize(magnitude, magn_norm, 0.0f, 1.0f, NORM_MINMAX);
            angle *= ((1.f / 360.f) * (180.f / 255.f));

            Mat _hsv[3], hsv, hsv8, bgr;
            _hsv[0] = angle;
            _hsv[1] = Mat::ones(angle.size(), CV_32F);
            _hsv[2] = magn_norm;
            merge(_hsv, 3, hsv);
            hsv.convertTo(hsv8, CV_8U, 255.0);
            cvtColor(hsv8, bgr, COLOR_HSV2BGR);
            cvtColor(bgr, bgr, COLOR_BGR2GRAY);


            //imshow("MASK", bgr);
            //waitKey(0);

            dy_pixels = countNonZero(bgr);
            dy_density = dy_pixels / pixels;
            dy_density_avg += dy_density;
        }

        c++;
        cropped_frame.copyTo(prev_mask);


        //writing the averaged queue & dynamic density per second (15 frames)
        if (c % 15 == 0)
        {
            //MyFile << (c / 15) << "," << q_density_avg / 15 << "," << dy_density_avg / 15 << endl;

            MyTextFile << (c / 15) << "," << q_density_avg / 15 << "," << dy_density_avg / 15 << endl;

            cout << (c / 15) << "," << q_density_avg / 15 << "," << dy_density_avg / 15 << endl;

            q_density_avg = 0;
            dy_density_avg = 0;

            
        }
    }

    return 0;
    //MyFile.close();
    MyTextFile.close();
}
