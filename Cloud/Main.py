import sys
sys.path.insert(0, "./CameraConnector/")
import PipeSocket

def main(path) :
    
    ps = PipeSocket.PipeSocket(path)


if __name__ == "__main__" :
    main(sys.argv[1])