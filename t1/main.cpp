#include <iostream>
#include "opencv2/opencv.hpp"

#define NORMAL_MODE 0
#define CONTRAST_G_B_MODE 1
#define CLAHE_MODE 2
#define HISTOGRAM_EQ_MODE 3
#define DISTORTION_MODE 4
#define POSTER_RT_MODE 5
#define ALIEN_HSV_MODE 6
#define ALIEN_YCrCB_MODE 7
#define MEAN_SHIFT_FILTER 8

#define NUM_1 -79
#define NUM_2 -78
#define NUM_3 -77
#define NUM_4 -76
#define NUM_5 -75
#define NUM_6 -74

using namespace cv;
using namespace std;

/**
* muestra el histograma del canal L de mat en la ventana s
* código usado de:
* http://docs.opencv.org/doc/tutorials/imgproc/histograms/histogram_calculation/histogram_calculation.html
*/
void imshow_hist(string s, Mat &mat);

/**
* Ajusta el contraste aplicando
* CLAHE (Contrast Limited Adaptive Histogram Equlization)
* sobre el canal L
*/
void contrast_clahe(Mat &src, Mat &dst, Ptr<CLAHE> &clahe);

/**
* Ecualiza el histograma de src usando equalizeHist de OpenCV
*/
void equalize_hist(Mat &src, Mat &dst);

/**
* Ajusta el contraste con la ecuación dst = gain*src + bias en el canal L
* de la fuente
*/
void contrast_gain_bias(Mat &src, Mat &dst, double gain, double bias);

/**
* Reubica la posición de los pixeles de src en x e y aplicando una
* distorción radial
* https://moodle2.unizar.es/add/pluginfile.php/550343/mod_resource/content/2/3.Procesamiento.pptx.pdf#page=35
*/
void reallocate_map(Mat &src, Mat &x, Mat &y, float cx, float cy, float k);

/**
* Aplica el efecto de poster a tiempo real
*/
void poster_rt(Mat &src, Mat &dst, int div);

/**
* Aplica el efecto alien en el espacio de color hsv
*/
void alien_hsv(Mat &src, Mat &dst, uchar hcolor);

void alien_ycrcb(Mat &src, Mat &dst, uchar cr_color, uchar cb_color);

int main(int argc, char **argv) {
    int mode = NORMAL_MODE;
    int key = -1;
    Mat frame, processed;
    Mat_<Vec3b>::iterator it, itend;

    VideoCapture capture(0);
    if (!capture.isOpened()) {
        return -1;
    }

    namedWindow("camera", WINDOW_AUTOSIZE);
    namedWindow("camera processed", WINDOW_AUTOSIZE);
    namedWindow("histogram", WINDOW_NORMAL);
    namedWindow("histogram processed", WINDOW_NORMAL);

    Ptr<CLAHE> clahe = createCLAHE();
    int poster_div = 1, level = 1;
    double clahe_clip_limit = 0.5, contrast_gain = 1.0, contrast_bias = 0.0, swr = 1, cwr = 1;
    char text[256];
    float distortion_k = 0.0;
    uchar hcolor = 120, cr_color = 255, cb_color = 0;
    while (true) {
        capture >> frame;
        imshow("camera", frame);
        imshow_hist("histogram", frame);

        if (mode == NORMAL_MODE) {
            processed = frame;
            sprintf(text, "[NO FILTER] swr=%.2f cwr=%.2f lvl=%d", swr, cwr, level);
        }
        else if (mode == CONTRAST_G_B_MODE) {
            contrast_gain_bias(frame, processed, contrast_gain, contrast_bias);
            sprintf(text, "[CONTRAST] gain=%.2f bias=%.2f", contrast_gain, contrast_bias);
        }
        else if (mode == HISTOGRAM_EQ_MODE) {
            equalize_hist(frame, processed);
            sprintf(text, "[HISTOGRAM EQ]");
        }
        else if (mode == DISTORTION_MODE) {
            Mat map_x, map_y;
            processed.create(frame.size(), frame.type());
            map_x.create(frame.size(), CV_32FC1);
            map_y.create(frame.size(), CV_32FC1);
            reallocate_map(frame, map_x, map_y, frame.cols / 2, frame.rows / 2, distortion_k);
            remap(frame, processed, map_x, map_y, CV_INTER_LINEAR, BORDER_CONSTANT, Scalar(0, 0, 0));
            sprintf(text, "[DISTORTION] k=%e", distortion_k);
        }
        else if (mode == POSTER_RT_MODE) {
            poster_rt(frame, processed, poster_div);
            sprintf(text, "[POSTER] div=%d", poster_div);
        }
        else if (mode == ALIEN_HSV_MODE) {
            alien_hsv(frame, processed, hcolor);
            sprintf(text, "[A_HSV] hue_color=%d", hcolor);
        }
        else if (mode == ALIEN_YCrCB_MODE) {
            alien_ycrcb(frame, processed, cr_color, cb_color);
            sprintf(text, "[A_YCrCB] cr=%d cb=%d", cr_color, cb_color);
        }
        else if (mode == MEAN_SHIFT_FILTER) {
            pyrMeanShiftFiltering(frame, processed, swr, cwr, level);
            sprintf(text, "[MEAN SHIFT] swr=%.2f cwr=%.2f lvl=%d", swr, cwr, level);
        }
        else { // CLAHE_MODE
            clahe->setClipLimit(clahe_clip_limit);
            contrast_clahe(frame, processed, clahe);
            sprintf(text, "[CLAHE] clip limit=%.2f", clahe->getClipLimit());
        }


        imshow_hist("histogram processed", frame);
        putText(frame, text, Point(10, 20), FONT_HERSHEY_PLAIN, 1.5, CV_RGB(0, 255, 0), 2);
        imshow("camera processed", frame);


        if ('q' == (key = char(waitKey(1))))
            break;
        else if ('c' == key) {
            if (mode == CONTRAST_G_B_MODE) {
                mode = CLAHE_MODE;
            } else {
                mode = CONTRAST_G_B_MODE;
            }
        }
        else if ('p' == key) {
            mode = POSTER_RT_MODE;
        }
        else if ('h' == key) {
            mode = HISTOGRAM_EQ_MODE;
        }
        else if ('n' == key) {
            mode = NORMAL_MODE;
        }
        else if ('d' == key) {
            mode = DISTORTION_MODE;
        }
        else if ('a' == key) {
            if (mode == ALIEN_YCrCB_MODE)
                mode = ALIEN_HSV_MODE;
            else
                mode = ALIEN_YCrCB_MODE;
        }
        else if ('m' == key) {
            mode = MEAN_SHIFT_FILTER;
        }
        else if (mode == CLAHE_MODE) {
            if (NUM_4 == key)
                clahe_clip_limit += 0.5;
            else if (NUM_1 == key)
                clahe_clip_limit = clahe_clip_limit == 0.5 ? 0.5 : clahe_clip_limit - 0.5;
        }
        else if (mode == CONTRAST_G_B_MODE) {
            if (NUM_4 == key)
                contrast_gain += 0.05;
            else if (NUM_1 == key)
                contrast_gain -= 0.05;
            else if (NUM_5 == key)
                contrast_bias += 5;
            else if (NUM_2 == key)
                contrast_bias -= 5;
        }
        else if (mode == DISTORTION_MODE) {
            if (NUM_4 == key)
                distortion_k += 0.0000001;
            else if (NUM_1 == key)
                distortion_k -= 0.0000001;
        }
        else if (mode == POSTER_RT_MODE) {
            if (NUM_4 == key)
                poster_div *= 2;
            else if (NUM_1 == key)
                poster_div = poster_div == 1 ? 1 : poster_div / 2;
        }
        else if (mode == ALIEN_HSV_MODE) {
            if (NUM_1 == key) {
                hcolor = 0;
            }
            else if (NUM_2 == key) {
                hcolor = 120;
            }
            else if (NUM_3 == key) {
                hcolor = 240;
            }
        }
        else if (mode == ALIEN_YCrCB_MODE) {
            if (NUM_1 == key) {
                cr_color = 0;
                cb_color = 255;
            }
            else if (NUM_2 == key) {
                cr_color = 255;
                cb_color = 0;
            }
            else if (NUM_3 == key) {
                cr_color = 25;
                cb_color = 25;
            }
        }
        else if (NUM_1 == key) {
            swr = swr == 1 ? 1 : swr - 1;
        }
        else if (NUM_4 == key) {
            swr += 1;
        }
        else if (NUM_2 == key) {
            cwr = cwr == 1 ? 1 : cwr - 1;
        }
        else if (NUM_5 == key) {
            cwr += 1;
        }
        else if (NUM_3 == key) {
            level = level == 1 ? 1 : level - 1;
        }
        else if (NUM_6 == key) {
            level += 1;
        }
    }

    capture.release();
    destroyAllWindows();
    return 0;
}

void alien_ycrcb(Mat &src, Mat &dst, uchar cr_color, uchar cb_color) {
    Mat YCrCb;
    Mat_<Vec3b>::iterator it, itend;
    uchar Cr, Cb, Y;

    cvtColor(src, YCrCb, CV_BGR2YCrCb);

    it = YCrCb.begin<Vec3b>();
    itend = YCrCb.end<Vec3b>();
    for (; it != itend; ++it) {
        Y = (*it)[0];
        Cr = (*it)[1];
        Cb = (*it)[2];
        //Si es el color de la piel
        if ((Y > 80) && (Cr > 135) && (Cr < 180) && (Cb > 85) && (Cb < 135)) {
            (*it)[1] = cr_color;
            (*it)[2] = cb_color;
        }
    }
    cvtColor(YCrCb, dst, CV_YCrCb2BGR);
}

void alien_hsv(Mat &src, Mat &dst, uchar hcolor) {
    Mat hsv;
    Mat_<Vec3b>::iterator it, itend;
    uchar h, s, v;

    cvtColor(src, hsv, CV_BGR2HSV);

    it = hsv.begin<Vec3b>();
    itend = hsv.end<Vec3b>();
    for (; it != itend; ++it) {
        h = (*it)[0];
        s = (*it)[1];
        v = (*it)[2];
        //Si es el color de la piel
        if ((h > 0) && (h < 20) && (s > 40) && (s < 150) && (v > 60) && (v < 255)) {
            (*it)[0] = hcolor;
            (*it)[1] = 212;
        }
    }
    cvtColor(hsv, dst, CV_HSV2BGR);

}

void poster_rt(Mat &src, Mat &dst, int div) {
    Mat YCrCb_img;
    vector<Mat_<Vec3b>> channels;
    Mat_<Vec3b>::iterator it, itend;
    cvtColor(src, YCrCb_img, CV_BGR2YCrCb);

    //Aplica el efecto poster
    it = YCrCb_img.begin<Vec3b>();
    itend = YCrCb_img.end<Vec3b>();
    for (; it != itend; ++it) {
        (*it)[0] = (*it)[0] / div * div + div / 2;
    }

    cvtColor(YCrCb_img, dst, CV_YCrCb2BGR);
}

void reallocate_map(Mat &src, Mat &x, Mat &y, float cx, float cy, float k) {
    int i, j;
    float r, dx, dy;

    for (j = 0; j < src.rows; j++) {
        for (i = 0; i < src.cols; i++) {
            dx = i - cx;
            dy = j - cy;
            r = dx * dx + dy * dy;
            x.at<float>(j, i) = dx * (1 + k * r) + cx;
            y.at<float>(j, i) = dy * (1 + k * r) + cy;
        }
    }
}

void contrast_gain_bias(Mat &src, Mat &dst, double gain, double bias) {
    Mat lab_img;
    cvtColor(src, lab_img, CV_BGR2Lab);
    vector<Mat> channels(3);
    split(lab_img, channels);

    channels[0] = channels[0] * gain + bias; // modificar canal L

    merge(channels, lab_img);

    cvtColor(lab_img, dst, CV_Lab2BGR);
}

void equalize_hist(Mat &src, Mat &dst) {
    Mat lab_img, hist_img;
    cvtColor(src, lab_img, CV_BGR2Lab);
    vector<Mat> channels(3);
    split(lab_img, channels);

    equalizeHist(channels[0], hist_img); // ecualizar canal L

    hist_img.copyTo(channels[0]);
    merge(channels, lab_img);

    cvtColor(lab_img, dst, CV_Lab2BGR);
}

void contrast_clahe(Mat &src, Mat &dst, Ptr<CLAHE> &clahe) {
    Mat lab_img, clahe_img;
    cvtColor(src, lab_img, CV_BGR2Lab);
    vector<Mat> channels(3);
    split(lab_img, channels);

    clahe->apply(channels[0], clahe_img); //Usar canal L

    clahe_img.copyTo(channels[0]);
    merge(channels, lab_img);

    cvtColor(lab_img, dst, CV_Lab2BGR);
}

void imshow_hist(string s, Mat &mat) {
    /// Separate the image in 3 places ( B, G and R )
    Mat lab;
    cvtColor(mat, lab, CV_BGR2Lab);
    vector<Mat> bgr_planes;
    split(lab, bgr_planes);

    /// Establish the number of bins
    int histSize = 256;

    /// Set the ranges ( for B,G,R) )
    float range[] = {0, 256};
    const float *histRange = {range};

    bool uniform = true;
    bool accumulate = false;

    Mat l_hist;

    /// Compute the histograms:
    calcHist(&bgr_planes[0], 1, 0, Mat(), l_hist, 1, &histSize, &histRange, uniform, accumulate);

    // Draw the histograms for B, G and R
    int hist_w = 512;
    int hist_h = 400;
    int bin_w = cvRound((double) hist_w / histSize);

    Mat histImage(hist_h, hist_w, CV_8UC3, Scalar(0, 0, 0));

    /// Normalize the result to [ 0, histImage.rows ]
    normalize(l_hist, l_hist, 0, histImage.rows, NORM_MINMAX, -1, Mat());

    /// Draw for each channel
    for (int i = 1; i < histSize; i++) {
        line(histImage, Point(bin_w * (i - 1), hist_h - cvRound(l_hist.at<float>(i - 1))),
                Point(bin_w * (i), hist_h - cvRound(l_hist.at<float>(i))),
                Scalar(255, 255, 255), 2, 8, 0);
    }

    imshow(s, histImage);

}
