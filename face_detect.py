# from dis import dis
import cv2
import pygame
import picamera
from picamera.array import PiRGBArray
import numpy as np
import time

##PYGAME INITIALIZATION
pygame.init()
dispx=640
dispy=480
disp=pygame.display.set_mode((dispx,dispy))

##OPENCV INITIALIZATION
#cap=cv2.VideoCapture(0)

#LOAD haar for face detection
face_cas=cv2.CascadeClassifier("./haarcascade_frontalface_alt_tree.xml")

#if the code is running
running = True

#image number of the person we are taking image of
image_no=0
#the index of the person of whom we are taking image
bitchnumber=0
#flag for continuesly taking images
stay=False
camera = picamera.PiCamera()
camera.resolution = (400, 200)
camera.framerate = 60
raw = PiRGBArray(camera, size = (400, 200))
time.sleep(0.1)
# while the images are beign captured from webcam
while running:

    for f in camera.capture_continuous(raw, format = "bgr", use_video_port = True):
        if running:
            fram = f.array
            raw.truncate(0)
            #when a new frame is recived , sets the flag to false, saying nothing has been detected yet
            #detect=False
            
            #read from camera
            fram=cv2.flip(fram,1)
            #copy the color frame for future
            color_frame=fram
            #convert to B&W for detection
            fram=cv2.cvtColor(fram,cv2.COLOR_BGR2GRAY)
            #detect the face
            faces=face_cas.detectMultiScale(fram)
            # incase the face is not detected, this allows program to not be crashed
            test=fram
            #create a surface on which we will work
            temp_disp=pygame.Surface(disp.get_size())

            #see the detected faces
            for (x,y,w,h) in faces:
                #sets that detect is true, so that it stops if not detecting
                detect=True
                #draw a rectangle
                cv2.rectangle(color_frame,(x,y+10),(x+w,y+h+20),(255,0,0))
                #crop the frame to show on the face
                test=fram[y+30:y+h-15,x+10:x+w-10]
                #code not needed:
                # test=fram[y+10:y+h+20,x:x+w]
                # r = 112 / test.shape[1]
                #set the dimesions of the image to stored
                dim = (300 , 300)
                #so that program doesnt crash
                try:
                    #try to resize, if the box is raelly small might thro an exception
                    #if error thrown, then set the test as empty
                    test = cv2.resize(test, dim, interpolation = cv2.INTER_AREA)
                except:
                    test=[]
            try:
                ###########THIS IS ONLY FOR THE DETECTED FACE ON TOP RIGHT
                #showing the image
                # cv2.imshow("test",test)
                #doesnt work if not converted//no idea y
                test_frame=cv2.cvtColor(test,cv2.COLOR_GRAY2RGB)
                #flips the image as the pygame flips again  the frame. do we really need to flip atall??
                test_frame=cv2.flip(test_frame,1)
                #conver the frame to the image
                face_img=pygame.surfarray.make_surface(test_frame)
                face_img=pygame.transform.rotate(face_img,-90)
            except:
                print "error"
            finally:
                ###########THIS IS FOR THE WHOLE FRAME
                # cv2.imshow("bla",fram) ### removed
                ## conver to rgb
                frame=cv2.cvtColor(color_frame,cv2.COLOR_BGR2RGB)
                frame=cv2.flip(frame,1)
                img=pygame.surfarray.make_surface(frame)
                img=pygame.transform.rotate(img,-90)
                #put the image on th etemp_display surface
                temp_disp.blit(img,(0,0))
            ## NOT NEEDED IF NO IM.SHOW()
            # if(cv2.waitKey(30)==27&0xff):
            #     break

            ##EVENTS
            for events in pygame.event.get():
                if events.type==pygame.QUIT:
                    running=False
                if events.type==pygame.KEYDOWN:
                    if (events.key==pygame.K_SPACE): #toggles the continuity of clicking the images
                        stay=not stay
                    if events.key==pygame.K_ESCAPE:
                        running=False
                    if events.key==pygame.K_TAB: ##increase the person number
                        bitchnumber+=1
                        image_no=0
                        print "bitch number changed to "+str(bitchnumber)
                    if events.key==pygame.K_a: ##decrease to person number
                        bitchnumber-=1
                        image_no=0
                        print "bitch number changed to "+str(bitchnumber)


                    ##IF the images is to be taken and the frame has a frame
            if(stay==True and detect==True):
                #increase tyhe image no
                image_no+=1
                #automatically ends if images >100
                if(image_no>=100):
                    stay= not stay
                print "Saved "+str(bitchnumber)+"th bitch "+str(image_no)
                ## save,, can we use jpg??
                cv2.imwrite("./pics/s"+str(bitchnumber)+"/"+str(image_no)+".pgm",test)
            ##blit the temp display to the screen
            disp.blit(temp_disp,(0,0))
            ##blit the face image to the screen
            disp.blit(face_img,(0,0))
            #update the screen
            pygame.display.update()
    # except:
    #     print "error"
        else:
            break
pygame.quit()
cv2.destroyAllWindows()
