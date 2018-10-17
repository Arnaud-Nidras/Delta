import cv2
import numpy as np
import os
import time
import fcntl
import atexit

class PipeSocket :

    def getFrame(self) :

        sizeReceived = False
        frameReceived = False
        bufferSize = 0
        os.write(self.ctlPipe, "Send".encode("UTF-8"))
            
        while not sizeReceived :

            try :
                inputText = os.read(self.imgPipe, 1024)


                if inputText :
                    if "Size : " in inputText.decode("UTF-8") :
                        bufferSize = int(inputText.decode("UTF-8")[7:])
                        #print("Size received : " + str(bufferSize))
                        os.write(self.ctlPipe, "Ready".encode("UTF-8"))
                        #print("Ready sent !")
                        sizeReceived = True

            except OSError as error :
                if error.errno == 11 :
                    continue
                else :
                    raise error

        while not frameReceived :

            try:
                inputText = os.read(self.imgPipe, bufferSize)

                if inputText :
                    #print("Received : " + str(len(inputText)) + " Expected : " + str(bufferSize))
                    decodedFrame = np.asarray(bytearray(inputText), dtype=np.uint8)
                    decodedFrame = cv2.imdecode(decodedFrame, 1)
                    return decodedFrame

            except OSError as error :
                if error.errno == 11 :
                    continue
                else :
                    raise error


    def exit_handler(self) :

        os.close(self.ctlPipe)
        os.close(self.imgPipe)
        os.system("pkill -f CameraSocket.py")


    def __init__(self, path) :

        atexit.register(self.exit_handler)

        cv2.namedWindow("Frame", cv2.WINDOW_AUTOSIZE)
        time.sleep(20)
        self.ctlPipe = os.open(path + "/CameraConnector/ctlPipe", os.O_WRONLY | os.O_NONBLOCK)
        self.imgPipe = os.open(path + "/CameraConnector/imgPipe", os.O_RDONLY | os.O_NONBLOCK)
        fcntl.fcntl(self.imgPipe, 1031, 1000000)

        print("[INFO] Connecting to Camera Socket ...")
        os.write(self.ctlPipe, "Open".encode("UTF-8"))
        

            

