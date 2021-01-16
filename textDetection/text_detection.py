# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import imutils
import os
import time
from cv2 import cv2
import pafy 

def decode_predictions(scores, geometry, min_confidence):
    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the
        # geometrical data used to derive potential bounding box
        # coordinates that surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]
        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability,
            # ignore it
            if scoresData[x] < min_confidence:
                continue
            # compute the offset factor as our resulting feature
            # maps will be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            # extract the rotation angle for the prediction and
            # then compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # use the geometry volume to derive the width and height of the bounding box
            # top + bottom offset
            h = xData0[x] + xData2[x]

            # right + left wrt offset
            w = xData1[x] + xData3[x]

            # # compute both the starting and ending (x, y)-coordinates
            # # for the text prediction bounding box
            # endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            # endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            # startX = int(endX - w)
            # startY = int(endY - h)
            # # add the bounding box coordinates and probability score
            # # to our respective lists
            # rects.append((startX, startY, endX, endY))

            # A more accurate bounding box for rotated text
            offsetX = offsetX + cos * xData1[x] + sin * xData2[x]
            offsetY = offsetY - sin * xData1[x] + cos * xData2[x]

            # calculate the UL and LR corners of the bounding rectangle
            p1x = -cos * w + offsetX
            p1y = -cos * h + offsetY
            p3x = -sin * h + offsetX
            p3y = sin * w + offsetY

            # add the bounding box coordinates
            rects.append((p1x, p1y, p3x, p3y))

            confidences.append(scoresData[x])

    # return a tuple of the bounding boxes and associated confidences
    return (rects, confidences)


def text_detection(vid_ref,east="frozen_east_text_detection.pb", min_confidence=0.5, width=320, height=320,max_percent=10.0,min_percent=1.0,warmup=200):
    # initialize the original frame dimensions, new frame dimensions,
    # and ratio between the dimensions
    (W, H) = (None, None)
    (newW, newH) = (width, height)
    (rW, rH) = (None, None)

    # define the two output layer names for the EAST detector model that
    # we are interested -- the first is the output probabilities (sigmoid-AF)and the
    # second (Featre map -> geometry info.)..
    #  can be used to derive the bounding box coordinates of text detected.
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    # load the pre-trained EAST text detector
    print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet(east)

    # if a video path was not supplied, grab the reference to the web cam
    if not vid_ref:
        print("[INFO] starting video stream...")
        vs = VideoStream(src=0).start()
        time.sleep(1.0)
    # otherwise, grab a reference to the video file
    else:
        vs = cv2.VideoCapture(vid_ref)
    # start the FPS throughput estimator
    fps = FPS().start()

    # Define path for saving cropped images.
    path = 'C:/Users/Vishal Ramane/Documents/GitHub/MTProject/textDetection/Img_cropped'
    frameNo =0   
    
    # loop over frames from the video stream
    while True:
        # grab the current frame, then handle if we are using a
        # VideoStream or VideoCapture object- returns (ret,rame)
        
        frame = vs.read()
        frame = frame[1] if vid_ref else frame
        #  VideoCapture object- returns (ret,frame)
        # ret -> True/False.

        # check to see if we have reached the end of the stream
        if frame is None:
            break

        # resize the frame, maintaining the aspect ratio
        frame = imutils.resize(frame, width=1000)
        orig = frame.copy()

        # if our frame dimensions are None, we still need to compute the
        # ratio of old frame dimensions to new frame dimensions
        if W is None or H is None:
            (H, W) = frame.shape[:2]
            rW = W / float(newW)
            rH = H / float(newH)


        # resize the frame, this time ignoring aspect ratio
        frame = cv2.resize(frame, (newW, newH))

        # construct a blob from the frame and then perform a forward pass
        # of the model to obtain the two output layer sets
        blob = cv2.dnn.blobFromImage(frame, 1.0, (newW, newH),
                                     (123.68, 116.78, 103.94), swapRB=True, crop=False)
        net.setInput(blob)
        (scores, geometry) = net.forward(layerNames)

        # decode the predictions,
        (rects, confidences) = decode_predictions(
            scores, geometry, min_confidence)

        # then  apply non-maximal suppression to suppress weak, overlapping bounding boxes
        boxes = non_max_suppression(np.array(rects), probs=confidences)

        # loop over the bounding boxes
        textNo = 0        

        for (startX, startY, endX, endY) in boxes:
            textNo += 1
            # scale the bounding box coordinates based on the respective
            # ratios
            startX = int(startX * rW)
            startY = int(startY * rH)
            endX = int(endX * rW)
            endY = int(endY * rH)

            # draw the bounding box on the frame
            cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

            # Crooping bounding boxes.
            cropped_img = orig[startY:endY, startX:endX]

            if(cropped_img.size !=0):
                # saving cropped images.
                cv2.imwrite(os.path.join(path ,f'f{frameNo}_{textNo}.png'), cropped_img)

        # update the FPS counter
        fps.update()
        # show the output frame
        cv2.imshow("Text Detection", orig)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    # if we are using a webcam, release the pointer
    if not vid_ref:
        vs.stop()
    # otherwise, release the file pointer
    else:
        vs.release()
    # close all windows
    cv2.destroyAllWindows()


def text_detection_command():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", type=str, default=None,
                    help="path to optional input video file")
    ap.add_argument("-east", "--east", type=str, default=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'frozen_east_text_detection.pb'),
                    help="path to input EAST text detector")
    ap.add_argument("-c", "--min-confidence", type=float, default=0.5,
                    help="minimum probability required to inspect a region")
    ap.add_argument("-w", "--width", type=int, default=320,
                    help="resized image width (should be multiple of 32)")
    ap.add_argument("-e", "--height", type=int, default=320,
                    help="resized image height (should be multiple of 32)")
    args = vars(ap.parse_args())

    text_detection(vid_ref=args["video"], east=args["east"],
                   min_confidence=args['min_confidence'], width=args["width"], height=args["height"], )


if __name__ == '__main__':
    #text_detection_command()

    # url of the video 
    # url = "https://www.youtube.com/watch?v=SkcddD0LGlM"  
    url = "https://www.youtube.com/watch?v=AsDfluoYB4Q"  
    # creating pafy object of the video 
    video = pafy.new(url)  
    # getting best stream 
    best = video.getbest() 
    # best.download()       
    
    text_detection(vid_ref=best.url )
    # folderpath ='C:/Users/Vishal Ramane/Documents/GitHub/MTProject/videos/'    
    # text_detection(vid_ref=os.path.join(folderpath ,'The Female Reproductive System.mp4') )
