import sys
import cv2
sys.path.insert(0, "./CameraConnector/")
import PipeSocket

def main(path) :
    
    ps = PipeSocket.PipeSocket(path)

    while 1 :

            frame = ps.getFrame()
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)


if __name__ == "__main__" :
    main(sys.argv[1])