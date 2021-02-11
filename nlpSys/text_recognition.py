import easyocr
import imutils
from imutils.video import FPS
from imutils.video import VideoStream
import time
from os import listdir
from os import path
from os.path import isfile, join
from cv2 import cv2
import pafy 
import numpy as np
from halo import Halo




def textRecog(vid_url,folderpath,vidCount):   
    start_time = time.time()
    spinner = Halo(text='processing', spinner='dots')
    print("\n")
    print("\n")
    print("  [INFO] : Text Recognition System Initialized...")
    print("  [INFO] : ============================= Text Recognition System  ================")
    if not vid_url:
        spinner.start("[INFO] starting video stream...")
        # print("[INFO] starting video stream...")
        vs = VideoStream(src=0).start()
        time.sleep(1.0)
    # otherwise, grab a reference to the video file
    else:
        spinner.start("[INFO] : Loading video file...")
        vs = cv2.VideoCapture(vid_url)
    
    spinner.succeed()
    spinner.start("[INFO] : Loading Text Recognition Model ...")
    # print("[INFO] : Loading Text Recognition Model ...")
    reader = easyocr.Reader(['en']) # loading  english language model.
    spinner.succeed()

    # start the FPS throughput estimator
    fps = FPS().start()   
    
    spinner.start( "[INFO] : Started text-recognition...")
    # print("[INFO] : Recognizing ...")
    result = []
    frameNo = 0

    # loop over frames from the video stream
    while True:
        # grab the current frame, then handle if we are using a
        # VideoStream or VideoCapture object- returns (ret,rame)
        
        frame = vs.read()
        frame = frame[1] if vid_url else frame
        #  VideoCapture object- returns (ret,frame)
        # ret -> True/False.

        # check to see if we have reached the end of the stream
        if frame is None:
            break
        
        cv2.imshow("Frame:", frame)
        key = cv2.waitKey(2) & 0xFF
        
        if key == ord("r"):
            spinner.text = "[INFO] : reader-invoked on the current frame ..."
            spinner.succeed()
            spinner.start("[INFO] : Extracting text...")
            frameNo +=1
            recognition = reader.readtext(frame)

            # Draw the bounding box on the frame
            for (box,text,confidence) in recognition:
                # draw the bounding box on the frame
                startX = int(box[0][0])
                startY = int(box[0][1])
                endX = int(box[2][0])
                endY = int(box[2][1])

                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

                # Gather results:    
                result.append(text)             
            
            spinner.succeed("[INFO] : textual contents extracted...")
                   
            # show the output frame and save it
            cv2.imshow("Text Detection", frame)
            cv2.imwrite(path.join(folderpath , f"v_{vidCount}_f{frameNo}.png"), frame)

            print("  [ALERT] : Press Key 'c' : to continue , 'q' : quit.")
            key = cv2.waitKey(0) & 0xFF

            if key == ord("c"):
                print("  [INFO] : Key 'c' is pressed, continue video analysis...")
                cv2.destroyAllWindows()
                spinner.start("[INFO] : Resumed processing... ")
                continue
            elif key == ord("q"):
                print(" [INFO] : Key q is pressed, exiting application...")
                fps.update()
                break

        elif key == ord("q"):
            break                         
             
        # update the FPS counter
        fps.update()
                  
   
    fps.stop()
    spinner.stop()
    elapsed_time = time.time() - start_time
    elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    print(f"  [INFO] : Exiting Text Recognition\n  [INFO] : Elapsed Time -{elapsed_time}")
    print("  [INFO] approx. FPS: {:.2f}".format(fps.fps()))
   
    
    # if we are using a webcam, release the pointer
    if not vid_url:
        vs.stop()
    # otherwise, release the file pointer
    else:
        vs.release()
    # close all windows
    cv2.destroyAllWindows()
    

    print("  [INFO] : Results - \n")
    print(result)
    return result



if __name__ == '__main__':
     # url of the video 
    
    # Female Reproductive sys
    url = "https://www.youtube.com/watch?v=SkcddD0LGlM"  
    # url = "https://www.youtube.com/watch?v=L-cXrt8RWek"  
    
    # Access Math
    # url = "https://www.youtube.com/watch?v=AsDfluoYB4Q"  
    # url = "https://www.youtube.com/watch?v=7D8-R-4Cdfg&t=237s"  
    
    # creating pafy object of the video 
    video = pafy.new(url)  
    # getting best stream 
    best = video.getbest() 
    # best.download()       

    folderPath = 'C:/Users/vrama/Documents/GitHub/MTProject/nlpSys/frames'

    textRecog(best.url,folderPath,1)