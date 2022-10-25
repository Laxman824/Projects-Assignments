/* 
Subtask1 - Task 1 SS
Using homography matrix for perspective correction to get a bird's eye view of the traffic

*/

#include <opencv4/opencv2/opencv.hpp>

using namespace cv;
using namespace std;

struct point{
    vector<Point2f> points;
};

void getMouseClicks(int event,int x,int y, int flags,void* param){

    point* data = (point*) param;
    if(event==EVENT_LBUTTONDOWN){
        if(data->points.size()<4)
            data->points.push_back(Point2f(x,y));
    }
    
}

int main(int argc, char** argv){

    //reading input image passed during runtime 
    Mat img = imread(argv[1]);
    if(!img.data){
        cout<<"Err : Couldnt read the image file. Check the path/extension"<<endl;
        return -1;
    }

    //changing to grayscale
    cvtColor(img,img,COLOR_BGR2GRAY);

    vector<Point2f> img_points;
    vector<Point2f> dest_points;
    vector<Point2f> crp_points;


    //Points start at top-left and go clockwise
    img_points.push_back(Point2f(937,275));
    img_points.push_back(Point2f(1290,267));
    img_points.push_back(Point2f(1535,1047));
    img_points.push_back(Point2f(579,1053));

    cout<<"Click on 4 points on the image (to warp and crop) and press enter"<<endl<<"Top-left first and clockwise"<<endl;

    //Get user input
    /*point data;
    data.points = img_points;
    imshow("Original Frame",img);
    setMouseCallback("Original Frame",getMouseClicks,&data);
    waitKey(0);*/

    //Points start at top-left and go clockwise
    dest_points.push_back(Point2f(472,152));
    dest_points.push_back(Point2f(900,152));
    dest_points.push_back(Point2f(900,930));
    dest_points.push_back(Point2f(472,930));

    //Points start at top-left and go clockwise
    crp_points.push_back(Point2f(0,0));
    crp_points.push_back(Point2f(400,0));
    crp_points.push_back(Point2f(400,800));
    crp_points.push_back(Point2f(0,800));

    Mat img_warped;
    Mat img_cropped;

    //Finding the homography matrix and using it for perspective correction
    Mat h = findHomography(img_points,dest_points);
    warpPerspective(img,img_warped,h,img.size());

    //Finding the homography matrix and using it for perspective correction
    Size size(400,800);
    Mat h2 = findHomography(img_points,crp_points);
    warpPerspective(img,img_cropped,h2,size);

    //Displaying output images to the user
    imshow("Processed Frame",img_warped);
    waitKey(0);

    //Displaying output images to the user
    imshow("Cropped Frame",img_cropped);
    waitKey(0);


    //Saving processes images to disk
    bool write_wrapped = imwrite("./"+string(argv[1]).substr(0,string(argv[1]).find_last_of("."))+"_Warped.jpg", img_warped);
    bool write_cropped = imwrite("./"+string(argv[1]).substr(0,string(argv[1]).find_last_of("."))+"_Cropped.jpg", img_cropped);

    if(!write_wrapped) cout<<"Couldnt save warped image";
    if(!write_cropped) cout<<"Couldnt save cropped image";

    return 0;
}
