/* 
Subtask2- Task 1 - C0P290. Semester 2, 2020-21
Using Background Subtractor and Optical Flow to calculate Queue and Dynamic density of vehicles using traffic camera's video as input

Authors - Harshita(2019CS10357) & Om Krishna(2019CS10272)
*/

#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/video/background_segm.hpp>

#include <iostream>
#include <fstream>
#include <chrono>

using namespace cv;
using namespace std;
using namespace std::chrono;

int c = 0;

int main(int argc, char **argv)
{

    auto start = high_resolution_clock::now();
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

    float parameter = stof(argv[2]);

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
    img_points.push_back(Point2f(937 * parameter, 275 * parameter));
    img_points.push_back(Point2f(1290 * parameter, 267 * parameter));
    img_points.push_back(Point2f(1535 * parameter, 1047 * parameter));
    img_points.push_back(Point2f(579 * parameter, 1053 * parameter));

    crp_points.push_back(Point2f(0 * parameter, 0 * parameter));
    crp_points.push_back(Point2f(400 * parameter, 0 * parameter));
    crp_points.push_back(Point2f(400 * parameter, 800 * parameter));
    crp_points.push_back(Point2f(0 * parameter, 800 * parameter));

    //Finding the homography matrix and using it for perspective correction
    Size size(400 * parameter, 800 * parameter);
    Mat h2 = findHomography(img_points, crp_points);
    warpPerspective(img, img_cropped, h2, size);

    backSubt->apply(img_cropped, fgMask, 0);

    vector<Point2f> frame_p;
    vector<Point2f> crframe_p;

    while (1)
    {
        bool bSuccess = cap.read(frame);
        if (!bSuccess)
        {
            break;
        }

        cvtColor(frame, frame, COLOR_BGR2GRAY);

        resize(frame, frame, Size(), parameter, parameter);

        frame_p.push_back(Point2f(968 * parameter, 254 * parameter));
        frame_p.push_back(Point2f(1308 * parameter, 260 * parameter));
        frame_p.push_back(Point2f(1551 * parameter, 1065 * parameter));
        frame_p.push_back(Point2f(587 * parameter, 1065 * parameter));

        crframe_p.push_back(Point2f(0 * parameter, 0 * parameter));
        crframe_p.push_back(Point2f(400 * parameter, 0 * parameter));
        crframe_p.push_back(Point2f(400 * parameter, 800 * parameter));
        crframe_p.push_back(Point2f(0 * parameter, 800 * parameter));

        h = findHomography(frame_p, crframe_p);
        warpPerspective(frame, cropped_frame, h, size);

        backSubt->apply(cropped_frame, fgMask, 0);
        //threshold(fgMask, fgMask, 128, 255, cv::THRESH_BINARY);

        pixels = fgMask.rows * fgMask.cols;
        nonZeroPixels = countNonZero(fgMask);
        q_density = nonZeroPixels / pixels;
        q_density_avg += q_density;

        c++;
        cropped_frame.copyTo(prev_mask);

        //writing the averaged queue & dynamic density per second (15 frames)
        if (c % 15 == 0)
        {
            //MyFile << (c / 15) << "," << q_density_avg / 15 << "," << dy_density_avg / 15 << endl;

            MyTextFile << (c / 15) << "," << q_density_avg / 15 << endl;

            cout << (c / 15) << "," << q_density_avg / 15 << endl;

            q_density_avg = 0;
        }
    }

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(stop - start);

    cout << "Time:" << duration.count() << endl;
    MyTextFile << "Time:" << duration.count() << endl;

    return 0;
    //MyFile.close();
    MyTextFile.close();
}