#include <iostream>
#include <strings.h>
#include "opencv2/opencv.hpp"

using namespace cv;

/**
* @param: argv[1] = imagen de prueba
*/
int main(int argc, char ** argv){
    Mat img, postProcess;

    img = imread("/Users/agustin/Workspace/C++/VisionPorComputadora/t2/img/circulo1.pgm", 1);

    cvtColor(img, img, CV_BGR2GRAY);

    /**
    * Otsu threshold.
    * @param 3: threshold value
    * @param 4: max value
    */
    threshold(img, postProcess, 0, 255, THRESH_OTSU);

    imshow("Original", img);
    imshow("PostProcess Otsu", postProcess);

    while(1);
}