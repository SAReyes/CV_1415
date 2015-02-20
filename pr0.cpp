#include "opencv2/highgui/highgui.hpp"

using namespace cv;
int main( int argc, char** argv ) {
    VideoCapture cap(0);

    if(!cap.isOpened())
        return -1;

    namedWindow("webcam");

    for(;;)
    {
        Mat frame;
        cap >> frame;
        imshow("webcam", frame);
        if(waitKey(50) >= 0) break;
    }

    return 0;
}