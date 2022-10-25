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

    backSubt->apply(img_cropped, fgMask, 0);

    vector<Point2f> frame_p;
    vector<Point2f> crframe_p;

    vector<Scalar> colors;
    RNG rng;
    for (int i = 0; i < 100; i++)
    {
        int r = rng.uniform(0, 256);
        int g = rng.uniform(0, 256);
        int b = rng.uniform(0, 256);
        colors.push_back(Scalar(r, g, b));
    }

    vector<Point2f> p0, p1;

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

        vector<Point2f> good_new;
        if (prev_mask.empty() == false)
        {

            goodFeaturesToTrack(prev_mask, p0, 100, 0.3, 7, Mat(), 7, false, 0.04);

            Mat mask = Mat::zeros(prev_mask.size(), prev_mask.type());

            vector<uchar> status;
            vector<float> err;
            TermCriteria criteria = TermCriteria((TermCriteria::COUNT) + (TermCriteria::EPS), 10, 0.03);
            calcOpticalFlowPyrLK(prev_mask, cropped_frame, p0, p1, status, err, Size(15, 15), 2, criteria);

            for (uint i = 0; i < p0.size(); i++)
            {
                // Select good points
                if (status[i] == 1)
                {
                    good_new.push_back(p1[i]);
                    // draw the tracks
                    line(mask, p1[i], p0[i], colors[i], 2);
                    circle(frame, p1[i], 5, colors[i], -1);
                }
            }
            Mat img;
            add(cropped_frame, mask, img);
            threshold(img, img, 150, 255, cv::THRESH_BINARY);

            //imshow("Frame", img);
            //waitKey(1);

            //cvtColor(img, img, COLOR_BGR2GRAY);

            dy_pixels = countNonZero(img);
            dy_density = dy_pixels / pixels;
            dy_density_avg += dy_density;

            p0 = good_new;
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

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(stop - start);

    cout << "Time:" << duration.count() << endl;
    MyTextFile << "Time:" << duration.count() << endl;
    return 0;
    //MyFile.close();
    MyTextFile.close();
}