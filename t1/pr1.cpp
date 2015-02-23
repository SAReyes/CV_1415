
#include "opencv2/opencv.hpp"

/**
* Constantes
*/
#define ALIEN 'a' //Tecla 'a'
#define EXIT 27 //Tecla 'esc' para cerrar el programa
#define POSTER 112 //Tecla 'p' para hacer poster
#define PLUS '+' //Tecla '+'
#define LESS '-' //Tecla '-'
#define BLUE 'b' //Tecla 'b'
#define RED 'r' //Tecla 'c'
#define GREEN 'g' //Tecla 'g'
#define SNAP 's' //Tecla 's'

using namespace cv;

/**
* Funciones
*/
void posterRealTime (VideoCapture webcam);
void poster (Mat &img);
void skinYcrCb (VideoCapture webcam);
void skinHSV (VideoCapture webcam);


/**
* Abre la webcam y permite tomar capturas de la misma
*/
int main( int argc, char** argv ) {
    VideoCapture webcam;
    Mat frame;
    char key = 0;

    webcam.open(0);
    if(!webcam.isOpened()) { //Sale si existe algun error con la camara
        std::cout << "Error en la camara" << std::endl;
        return -1;
    }

    namedWindow("WebCam");

    for(;;)
    {
        webcam >> frame;

        if((key = waitKey(50)) == EXIT){
            break;
        } else if(key == ALIEN) {
            skinYcrCb(webcam);
            //skinHSV(webcam);
        } else if(key == POSTER){
            posterRealTime(webcam);
        } else if(key == SNAP){
            poster(frame);
        } else{
            imshow("WebCam", frame); //Muestra imagenes de la camera
        }
    }

    return 0;
}


/**
* Aplica efecto alien
*/
void skinHSV (VideoCapture webcam){
    Mat hsv, frame;
    Mat_<Vec3b>::iterator it, itend;
    uchar h, s, v, key, hColor;

    hColor = 120;

    std::cout << "[a/b/r] para cambiar el color, ESC para salir: " << std::endl;

    for(;;) {
        webcam >> frame;
;
        
        cvtColor(frame, hsv, CV_BGR2HSV);

        it = hsv.begin<Vec3b>();
        itend = hsv.end<Vec3b>();
        for (; it != itend; ++it) {
            h = (*it)[0];
            s = (*it)[1];
            v = (*it)[2];
            //Si es el color de la piel
            if ((h > 0) && (h < 20) && (s > 40) && (s < 150) && (v > 60) && (v < 255)) {
                (*it)[0] = hColor;
                (*it)[1] = 1;
                (*it)[2] = 1;
            }
        }
        cvtColor(hsv, hsv, CV_HSV2BGR);
        imshow("WebCam", hsv);

        if((key = waitKey(20)) == BLUE){
            hColor = 240;
        } else if(key == RED){
            hColor = 0;
        } else if(key == GREEN){
            hColor = 120;
        } else if(key == EXIT){
            return;
        }

    }
}

/**
* Aplica efecto alien
*/
void skinYcrCb (VideoCapture webcam){
    Mat YCrCb, frame;
    Mat_<Vec3b>::iterator it, itend;
    uchar Cr, Cb, Y, key, CrColor, CbColor;

    CrColor = 25;
    CbColor = 25;

    std::cout << "[a/b/r] para cambiar el color, ESC para salir: " << std::endl;

    for(;;) {
        webcam >> frame;

        cvtColor(frame, YCrCb, CV_BGR2YCrCb);

        it = YCrCb.begin<Vec3b>();
        itend = YCrCb.end<Vec3b>();
        for (; it != itend; ++it) {
            Y = (*it)[0];
            Cr = (*it)[1];
            Cb = (*it)[2];
            //Si es el color de la piel
            if ((Y > 80) && (Cr > 135) && (Cr < 180) && (Cb > 85) && (Cb < 135)) {
                (*it)[1] = CrColor;
                (*it)[2] = CbColor;
            }
        }
        cvtColor(YCrCb, YCrCb, CV_YCrCb2BGR);
        imshow("WebCam", YCrCb);

        if((key = waitKey(20)) == BLUE){
            CrColor = 0;
            CbColor = 255;
        } else if(key == RED){
            CrColor = 255;
            CbColor = 0;
        } else if(key == GREEN){
            CrColor = 25;
            CbColor = 25;
        } else if(key == EXIT){
            return;
        }

    }
}

/**
* Aplica efecto poster en tiempo real
*/
void posterRealTime (VideoCapture webcam){
    Mat poster, frame;
    char key;
    int div = 8;
    Mat_<Vec3b>::iterator it, itend;

    std::cout << "[+/-] para aumentar/disminuir rango de colores, ESC para salir: " << std::endl;

    for(;;) {
        webcam >> frame;

        cvtColor(frame, poster, CV_BGR2YCrCb);

        //Aplica el efecto poster
        it = poster.begin<Vec3b>();
        itend = poster.end<Vec3b>();
        for (; it != itend; ++it) {
            (*it)[0] = (*it)[0] / div * div + div / 2;
            //(*it)[1]= (*it)[1]/div*div + div/2;
            //(*it)[2]= (*it)[2]/div*div + div/2;
        }

        cvtColor(poster, poster, CV_YCrCb2BGR);

        imshow("WebCam", poster);

        // Aumenta o elimina colores
        if((key = waitKey(20)) == PLUS && div < 64){
            div = div * 2;
        } else if(key == LESS && div > 8){
            div = div / 2;
        } else if(key == EXIT){
            return;
        }

    }
}

/**
* Aplica el efecto poster a una imagen concreta
*/
void poster (Mat &img){
    Mat imgFinal;

    /**
    * @param - 1: imagen fuente
    * @param - 2: imagen destino
    * @param - 3: radio de ventana
    * @param - 4: radio de color
    * @param - 5: nivel maximo de segmentacion
    */
    pyrMeanShiftFiltering(img, imgFinal, 16, 16, 2);

    imshow("Snap", imgFinal);
}