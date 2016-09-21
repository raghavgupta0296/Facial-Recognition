import cv2
from PIL import Image
import os
import numpy as np
import pygame

#INITIATE PYGAME
pygame.init()
disp=pygame.display.set_mode((200,200))
disp.fill((0,0,0))

#SET PEOPLE NAME, MANUALLY ,
###################################DONT FORGET TO CHAGE IN THE OTHER FILE TOO
people=['rohan','raghav','rohit','aproocv','riya','director','aksha','']
#FOR INDEX OF THE PERSON
c=0
#empty list
image,person=[],[]

#lazy to comment:
for dirname,dirnames,filenames in os.walk("./pics"):
    for subdir in dirnames:
        subjec_path=os.path.join(dirname,subdir)
        total_image=0
        print subjec_path,people[c],c,
        for filename in os.listdir(subjec_path):
            try:
                f=Image.open(os.path.join(subjec_path,filename))
                f=f.convert("L")
                test=cv2.imread(os.path.join(subjec_path,filename))
                print filename,c
                im=np.array(f)
                print im.shape[0],":",im.shape[1]
                cv2.imshow("bla",im)
                if(cv2.waitKey(001)==27&0xff):
                    break
                image.append(np.asarray(f,dtype=np.uint8))
                person.append(c)
                total_image+=1
                stop=False
                for events in pygame.event.get():
                    if events.type==pygame.QUIT:
                        pygame.quit()
                    if events.type==pygame.KEYDOWN:
                        if events.key==pygame.K_SPACE:
                            stop=not stop
                while(stop):
                    for events in pygame.event.get():
                        if events.type==pygame.QUIT:
                            pygame.quit()
                        if events.type==pygame.KEYDOWN:
                            if events.key==pygame.K_SPACE:
                                stop=not stop
            except IOError:
                print "I/O error ({0}) : {1} ",IOError.errno,IOError.strerror
            except:
                print "other error"
                raise
        print total_image
        c+=1
print "Learning"

##select which algo to use
########################################DONT FORGET TO CHANGE IN THE faceregoc FILE ALSO##################################
# model=cv2.createFisherFaceRecognizer(2,500)
model=cv2.createLBPHFaceRecognizer(radius=1,neighbors=9,grid_x=8,grid_y=8,threshold=60)
# model=cv2.createFisherFaceRecognizer()

model.train(np.asarray(image),np.asarray(person))
print "learnt"
model.save("./trainer.xml")