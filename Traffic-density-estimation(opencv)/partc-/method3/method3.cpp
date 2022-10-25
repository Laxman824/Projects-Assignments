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

#include <pthread.h>

using namespace cv;
using namespace std;
using namespace std::chrono;

//ofstream MyFile("out.csv");
ofstream MyTextFile("out.txt");
float q_density_avg = 0;
vector<Mat> fgMask;
Mat mask;

void *myBackgroundSubtractor(void *threadarg);
vector<Mat> subdivide(Mat img, int rowDivisor, int colDivisor);

Ptr<BackgroundSubtractor> backSubt = createBackgroundSubtractorMOG2();

struct thread_data
{
    Mat frame;
    int n;
};

int main(int argc, char **argv)
{
    auto start = high_resolution_clock::now();
    int c = 0;
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

    Mat img_cropped;
    Mat frame;

    float dy_pixels, dy_density, pixels, nonZeroPixels, q_density;

    vector<Point2f> img_points;
    vector<Point2f> crp_points;

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

    backSubt->apply(img_cropped, mask, 0);

    fgMask = subdivide(mask, 2, 2);

    while (1)
    {
        bool bSuccess = cap.read(frame);

        if (!bSuccess)
        {
            cout << "Fin" << endl;
            break;
        }
        else
        {

            vector<Point2f> frame_p;
            vector<Point2f> crframe_p;
            Size size(400, 800);

            Mat cropped_frame;

            Mat h;

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

            vector<Mat> img_blocks = subdivide(cropped_frame, 2, 2);
            pthread_t threads[4];
            struct thread_data td[4];

            for (int i = 0; i < 4; i++)
            {
                td[i].frame = img_blocks.at(i);
                td[i].n = i;
                pthread_create(&threads[i], NULL, myBackgroundSubtractor, (void *)&td[i]);

                pthread_join(threads[i], NULL);
            }

            c++;
            //writing the averaged queue & dynamic density per second (15 frames)
            if (c % 15 == 0)
            {
                //MyFile << (c / 15) << "," << q_density_avg / 15 << "," << dy_density_avg / 15 << endl;

                MyTextFile << (c / 15) << "," << q_density_avg / 60 << endl;

                cout << (c / 15) << "," << q_density_avg / 60 << endl;

                q_density_avg = 0;
            }
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

void *myBackgroundSubtractor(void *threadarg)
{
    struct thread_data *my_data;
    my_data = (struct thread_data *)threadarg;

    //imshow("f", my_data->frame);
    //waitKey(0);
    //imshow("f", fgMask.at(my_data->n));
    //waitKey(0);

    backSubt->apply(my_data->frame, fgMask.at(my_data->n), 0);
    //threshold(fgMask, fgMask, 128, 255, cv::THRESH_BINARY);

    float pixels,
        nonZeroPixels, q_density;

    pixels = fgMask.at(my_data->n).rows * fgMask.at(my_data->n).cols;
    nonZeroPixels = countNonZero(fgMask.at(my_data->n));
    q_density = nonZeroPixels / pixels;
    q_density_avg += q_density;

    return NULL;
}

vector<Mat> subdivide(Mat img, int rowDivisor, int colDivisor)
{
    vector<Mat> img_blocks;
    if (!img.data || img.empty())
        cerr << "Problem Loading Image" << endl;

    Mat maskImg = img.clone();

    if (img.cols % colDivisor == 0 && img.rows % rowDivisor == 0)
    {
        for (int y = 0; y < img.cols; y += img.cols / colDivisor)
        {
            for (int x = 0; x < img.rows; x += img.rows / rowDivisor)
            {
                img_blocks.push_back(img(Rect(y, x, (img.cols / colDivisor), (img.rows / rowDivisor))).clone());
                rectangle(maskImg, Point(y, x), Point(y + (maskImg.cols / colDivisor) - 1, x + (maskImg.rows / rowDivisor) - 1), CV_RGB(255, 0, 0), 1);

                //imshow("Image", maskImg);
                //waitKey(0);
            }
        }
    }
    else
    {
        cout << "incorrect split" << endl;
    }

    return img_blocks;
}