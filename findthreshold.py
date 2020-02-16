import cv2
import numpy as np

import gbvision as gbv


stdv = 20


def main():
    frame = cv2.imread('layout.jpeg')
    cv2.imshow("name", frame)


    bbox = cv2.selectROI('feed', frame)
    thr = gbv.median_threshold(frame, stdv, bbox, gbv.ColorThreshold.THRESH_TYPE_BGR)

    cv2.destroyAllWindows()
    print(thr)

    threshold = gbv.StreamWindow('threshold', frame, drawing_pipeline=thr)
    threshold.open()





if __name__ == '__main__':
    main()
