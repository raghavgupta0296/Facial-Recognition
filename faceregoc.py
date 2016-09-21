import cv2
import numpy as np
import pygame
# import picamera
# from picamera.array import PiRGBArray
import time
import socket
from thread import start_new_thread
from twilio.rest import TwilioRestClient


print 'started'
model=cv2.createLBPHFaceRecognizer(radius=1,neighbors=9,grid_x=8,grid_y=8,threshold=60)
model.load("./trainer.xml")
print "loaded"


#initialize pygame
pygame.init()
disp=pygame.display.set_mode((640,480))
disp.fill((0,0,255))
#set font for displaying the information
font=pygame.font.SysFont('Calibri',76,True,False)


recog=False
server_answered=False
###################################################################################################################################

def connect_server():
    global server_answered,recog
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(("localhost",7567))
        s.sendall("start_recog")
        ans=s.recv(1024)
        if(ans == "authorized"):
            server_answered = True
            recog = True
        else:
            server_answered = True
            recog = False
    except:
        server_answered=True
        recog=False

###################################################################################################################################
def server_connect():
    global server_answered,recog
    server_answered=False
    print "do your code here"
    running=True
    start_new_thread(connect_server,())
    while(running):
        disp.fill((0,0,0))
        for(events) in pygame.event.get():
            pass
        if(server_answered):
            time.sleep(0.1)
            running=False
            if(recog):
                return True
            else:
                return False
		pygame.tick(10)
####################################################################################################################################

def pin_entry(tries=0):
    dispx=640
    dispy=480
    chkPass="4519"
    running=True
    dispy=float(dispy)*4/5;
    numbers=[[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    numbers_string=[['1','2','3'],['4','5','6'],['7','8','9'],['Clear','0','Enter']]
    for i in range(4):
        for j in range(3):
            numbers[i][j]=pygame.Rect(j*dispx/3+10,(i+1)*dispy/4+20,dispx/3-20,dispy/4-40)

    def draw_again():
        global disp
        num=0
        disp.fill((0, 0, 0))
        for i in range(4):
            for j in range(3):
                pygame.draw.rect(disp, (100, 140, 170), numbers[i][j])
                if (num < 9):
                    num += 1
                    label = font.render(str(num), 1, (255, 255, 255))
                    disp.blit(label, (j * dispx / 3 +84, ((i + 1) * dispy / 4)+15 ))

        pygame.draw.rect(disp, (255, 0, 0), numbers[3][0])
        pygame.draw.rect(disp, (255, 0, 0), numbers[3][2])
        label = font.render("Clear", 1, (255, 255, 255))
        disp.blit(label, (0 * dispx / 3+23 , ((3 + 1) * dispy / 4) + 15))
        label = font.render(str(0), 1, (255, 255, 255))
        disp.blit(label, (1 * dispx / 3 + 84, ((3 + 1) * dispy / 4) + 15))
        label = font.render("Enter", 1, (255, 255, 255))
        disp.blit(label, (2 * dispx / 3 +23, ((3 + 1) * dispy / 4) + 15))


    numbers[3][1]=pygame.Rect(1*dispx/3+10,(3+1)*dispy/4+20,dispx/3-20,dispy/4-40)
    disp_pass=''
    passw=""
    draw_again()
    #pygame.Rect()
    while(running):
        mousex, mousey=0,0
        for events in pygame.event.get():
            if(events.type==pygame.QUIT):
                pygame.quit()
            if(events.type==pygame.MOUSEBUTTONDOWN):
                print passw
                mousex,mousey=pygame.mouse.get_pos()
        for i in range(4):
            for j in range(3):
                if numbers[i][j].collidepoint(mousex,mousey):
                    temp=numbers_string[i][j]
                    if temp=="Clear":
                        passw=passw[0:-1]
                        disp_pass=disp_pass[0:-1]
                        print disp_pass
                        draw_again()
                    elif temp=="Enter":
                        if(passw==chkPass):
                            return True
                        else:
                            tries+=1
                            if(tries<3):
                                disp.fill((0,0,0))
                                new_pin=pin_entry(tries)
                                if(new_pin):
                                    return True
                            return False
                    else:
                        disp_pass+='*'
                        passw+=temp

        password=font.render(disp_pass,True,(255,255,255))
        disp.blit(password,(0,0))
        pygame.display.update()


####################################################################################################################################
####SMS
def send_sms():
    acc="AC48fdb952e0270d16b415924a682b742b"
    token="2c84da59eefa650c7f7ca1c9e6c874ac"
    client=TwilioRestClient(acc,token)
    message=client.messages.create(to="+917567792829",from_="+18329243614",body="Testing 123")
    print "Message sent!"

###################################################################################################################################
#####CODE STARTS HERE
##FLAGS
touched=False
face=False
mainloop=True
##VARIABLES
clock=pygame.time.Clock()
deltaTime=float(0)
timeTaken=float(0)
detected=False
show_text=False
unlock_method=0
while(mainloop):

    touched=False
    disp.fill((0,0,0))
    pygame.display.update()
    while(not touched):
        for events in pygame.event.get():
            if events.type==pygame.QUIT:
                pygame.quit()
            if events.type==pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    touched=True

    if(touched):
        face=server_connect()
        clock.tick(1)
        if(face):
            detected=True
        else:
            detected=False
            disp.fill((0,0,0))
            pygame.display.update()
            show_text=True
            while(show_text):
                timeTaken+=deltaTime
                print timeTaken,"use pin"
                for(events) in pygame.event.get():
                    pass
                string_=font.render("Use pin please!",True,(255,0,255))
                pygame.display.update()
                disp.blit(string_,(0,0))
                pygame.display.update()
                if(timeTaken>1):
                    touched=False
                    show_text=False
                    timeTaken=0
                deltaTime=float(clock.tick(30))/1000

            pin=pin_entry()
            clock.tick(30)
            if(pin):
                detected=True
            else:
                detected=False
        show_text=True


    disp.fill((0,0,0))
    pygame.display.update()
    while(show_text):
        timeTaken+=deltaTime
        print timeTaken,"the other thing"
        for(events) in pygame.event.get():
            pass
        if(detected):
            string_=font.render("Opened!",True,(0,0,255))
            ####open_lock()
            disp.blit(string_,(0,0))
            pygame.display.update()
        else:
            string_=font.render("Not Autherized!",True,(255,0,0))
            disp.blit(string_,(0,0))
            pygame.display.update()
        if(timeTaken>7):
            touched=False
            show_text=False
            timeTaken=0
            if(not detected):
                disp.fill((0,0,0))
                send_sms()
        deltaTime=float(clock.tick(30))/1000
    ####close_lock()
pygame.quit()
cv2.destroyAllWindows()

