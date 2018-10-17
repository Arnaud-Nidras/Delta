import cv2
import numpy as np
import os
import errno
import time
import sys
import atexit

class CameraSocket :

    def getCurrentPicture(self) :

        inputFrame = self.cap.read()[1]
        encodedFrame = cv2.imencode(".jpg", inputFrame)[1]
        arrayFrame = np.array(encodedFrame)
        return arrayFrame.tostring()

    def sendCurrentPicture(self) :

        dataToSend = self.getCurrentPicture()
        bufferSize = len(dataToSend)

        os.write(self.imgPipe, ("Size : " + str(bufferSize)).encode("UTF-8"))
        #print("Size sent : " + str(bufferSize))
        ready = False

        while(not ready) :

            try:
                inputText = os.read(self.ctlPipe, 1024)

                if inputText :
                    if inputText.decode("UTF-8") == "Ready" :
                        os.write(self.imgPipe, dataToSend)
                        #print("IMG sent !")
                        return

            except OSError as error:
                
                if error.errno == 11:
                    continue
                
                else:
                    raise error

    def exit_handler(self) :

        os.close(self.ctlPipe)
        os.close(self.imgPipe)

            
    def __init__(self, path) :

        atexit.register(self.exit_handler)

        print("\n\n[INFO] Connecting Camera Socket to Camera ...")
        print("\tWaiting ...")
        self.cap = cv2.VideoCapture('udpsrc port=8004 caps = "application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)H264, payload=(int)96" ! rtpjitterbuffer latency=0 ! rtph264depay ! decodebin ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
        print("\tDone !")
        cv2.namedWindow("Frame", cv2.WINDOW_AUTOSIZE)
        print("[OK] Camera <----------> Camera Socket")
        self.ctlPipe = os.open(path + "/CameraConnector/ctlPipe", os.O_RDONLY | os.O_NONBLOCK)
        self.imgPipe = None

        while(1) :

            try:
                inputText = os.read(self.ctlPipe, 1024)

                if inputText :
                    if inputText.decode("UTF-8") == "Send" :
                        self.sendCurrentPicture()
                    if inputText.decode("UTF-8") == "Open" :
                        self.imgPipe = os.open(path + "/CameraConnector/imgPipe", os.O_WRONLY | os.O_NONBLOCK)
                        print("[OK] Camera Socket <----------> Pipe Socket")
                        print("[INFO] Socket successfully initialized, ready to start !")
                        print("\n---------------------------------------------------------\n")

            except OSError as err:
                if err.errno == 11:
                    continue
                else:
                    raise err
                
        

if __name__ == '__main__':
    CameraSocket(sys.argv[1])