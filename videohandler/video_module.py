import cv2


'''
This class is designed to show the visual part of application: show video recording,
scaled lips area, Buttons to start recording and input field for wordto speak

'''

class VideoHandler:


    def __init__(self):

        self.path_to_classifier = "../haarcascades/haarcascade_mcs_mouth.xml"
        self.path_to_output_word_prefix = "../data/{}"

        self.resized_width = 200
        self.resized_height = 100

        self.width = 640
        self.height = 480
        print("[INFO] : CV version: {}".format(cv2.__version__))

        self.mouth_cascade = cv2.CascadeClassifier(self.path_to_classifier)
        self.nose_cascade = cv2.CascadeClassifier('../haarcascades/haarcascade_mcs_nose.xml')
        self.face_cascade = cv2.CascadeClassifier('../haarcascades/haarcascade_frontalface_default.xml')

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,self.width)
        self.cap.set(4,self.height)

        self.originalOut = None
        self.resizedOut = None


    def readMouthFromWeb(self):

        if self.mouth_cascade.empty():
            raise IOError('Unable to load the mouth cascade classifier xml file')

        ds_factor = 0.5
        ret, frame = self.cap.read()

        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        mouth_rects = self.mouth_cascade.detectMultiScale(frame, 1.7, 11)
        resized = None

        nose = self.nose_cascade.detectMultiScale(gray_img)

        # faces = self.face_cascade.detectMultiScale(gray_img, 1.05, 5)   # print faces

        # for (p,q,r,s) in faces:
        #     cv2.rectangle(frame,(p,q),(p+r,q+s),(255,0,0),2)
        #     break

        nose_y = 0
        for (np,nq,nr,ns) in nose:
            nose_y = nq
            # cv2.rectangle(frame,(np,nq),(np+nr,nq+ns), (0,0,0),2)
            break

        for (x,y,w,h) in mouth_rects:
            y = int(y - 0.15*h)
            border_width = 3
            #mouth must be below the nose ~assumption
            if y > nose_y:
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), border_width)

                cropped = frame[y + border_width : y+h - border_width, x+border_width : x+w-border_width]
                resized = cv2.resize(cropped, (self.resized_width, self.resized_height), fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_AREA)
                break

            else:
                continue
        return (frame, resized)

    def showSplitChannels(self, frame):
        (B,G,R) = cv2.split(frame)
        cv2.imshow("Red", R)
        cv2.imshow("Green", G)
        cv2.imshow("Blue", B)


    def listenClose(self):
        #esc to exit and save video
        if cv2.waitKey(10) == 27:
            return False
        else:
            return True

    def writeFrame(self, name, frame):

        if self.originalOut is None:
            fourcc = cv2.cv.CV_FOURCC(*"DIVX")
            self.originalOut = cv2.VideoWriter('output.avi', fourcc, int(25), (self.width, self.height))

        self.originalOut.write(frame)


    def writeLips(self, name, frame):

        if self.resizedOut is None:
            fourcc = cv2.cv.CV_FOURCC(*"DIVX")
            self.resizedOut = cv2.VideoWriter('../data/{}.avi'.format(name), fourcc, int(25), (self.resized_width, self.resized_height))

        self.resizedOut.write(frame)

    def releaseResources(self):

        print("[INFO] release resourcess")
        self.cap.release()

        if self.originalOut is not None:
            self.originalOut.release()

        if self.resizedOut is not None:
            self.resizedOut.release()

        cv2.destroyAllWindows()