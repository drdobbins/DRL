#!/usr/bin/python
#This is DRL as of 10/22/18

#DRL Version 2.0.1
#Includes slow clock bug, and 3 dots of death fix.
#2.0.3-Resizing of logos for different resolutions
#2.0.4-IPF 3rd timer requirement.
#2.0.4- World Games RS232 Compatability
#2.0.5- LiftingCast Integration
#2.0.6-Auto Update functionality

#Created by Scott Dobbins
#This software shall not be redistrubted without the expressed written consent of Scott Dobbins
#This version is also compatible with DRL 2.0 Remotes


import pygame, sys
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import time
import math
import os
from pygame import movie #necessary for showing videos
import socket
import fcntl
import struct
import json
pygame.init()
pygame.font.init()

#Configuration Settings.
#---------------------------
#Draw the main timer?
'''main_clock_master = True
#---------------------------
#Draw the attempt timers?
draw_attempt_timer_1 = True
draw_attempt_timer_2 = True
draw_attempt_timer_3 = True
#---------------------------
#Display Infraction Cards?
show_infraction_cards = True
#----------------------------
#3rd Attempt Bump Functionality?
third_bump_enabled = True
#----------------------------
#Display Custom center logo?
main_logo_enable = True
#If true, define logo image name
logo_name = "uruguay.png"
#----------------------------
#Configure the Startup Screen'''
version_text = 'Version: 2.0.4'
#-----------------------------
#Configure Opener Change
#opener change message?
#opener_changes_allowed = True
#opener_min_time = 3
#------------------------------'''
#Combo Set?
Dual_Mode = False
#------------------------------

#Read in the local JSON config file
with open('config.json') as f:
	config_data = json.load(f)
print config_data
	
main_clock_master = config_data["main_clock"]
draw_attempt_timer_1 = config_data["attempt_timer_1"]
draw_attempt_timer_2 = config_data["attempt_timer_2"]
draw_attempt_timer_3 = config_data["attempt_timer_3"]
show_infraction_cards = config_data["infraction_cards"]
third_bump_enabled = config_data["deluxe_features"]
opener_changes_allowed = config_data["deluxe_features"]
opener_min_time = config_data["opener_change_time"]
main_logo_enable = config_data["center_logo"]
logo_name = config_data["logo_name"]




os.system('amixer cset numid=3 2') #sets the audio output to digital this will be the default
                         
dimensions = pygame.display.Info() #this grabs the screen's size in pixels

surface = pygame.display.set_mode((dimensions.current_w, dimensions.current_h), pygame.FULLSCREEN)#creates the main window

pygame.mouse.set_visible(0)#remvoes the mouse icon rom the main screen

surface.fill((0,0,0)) #color the screen black


initialization_timer = 5

while initialization_timer >= 0:


    surface.fill((0,0,0)) #color the screen black

    #pygame.draw.rect(surface, (0,148,71),(0,0, dimensions.current_w, dimensions.current_h),10)#this draws the green border
    logo = pygame.image.load(".DRL Logo.png") #load in the image you want displayed
    scaled_logo_main = pygame.transform.scale(logo, ((dimensions.current_w/100)*35, (dimensions.current_h/100)*70)) #rescales the image based on the screen

    surface.blit(scaled_logo_main, ((dimensions.current_w/100)*34, (dimensions.current_h/100)*4)) #place the image with the left hand corner being (0,0)


    init_timer_string = str(initialization_timer)
    intro_message = 'Initalizing the DRL System...'+ init_timer_string
    textFont = pygame.font.Font(".SafetyMedium.otf",(dimensions.current_w/20))
    Welcome_message = textFont.render(intro_message, 0, (0,148,71))
    surface.blit(Welcome_message,(((dimensions.current_w)/100)*12,((dimensions.current_h)/100)*85))

    version_font = pygame.font.Font(".SafetyMedium.otf",(dimensions.current_w/45))
    version_message = version_font.render(version_text, 0, (0,148,71))
    surface.blit(version_message,(((dimensions.current_w)/100)*12,((dimensions.current_h)/100)*98))
    
    time.sleep(1)
    initialization_timer -=1
 
    pygame.display.update()

textFont = pygame.font.Font(".SafetyMedium.otf",(dimensions.current_w/20)) #sets the font for the numbers

pygame.display.update()

 
DRL_logo = pygame.image.load(".DRL Logo.png")
#logo = pygame.image.load(".DRL Logo.png") #load in the image you want displayed

scaled_logo = pygame.transform.scale(DRL_logo, (dimensions.current_w/4, dimensions.current_h/2)) #rescales the image based on the screen

surface.blit(scaled_logo, (dimensions.current_w/12, dimensions.current_h/20)) #place the image with the left hand corner being (0,0)

pygame.display.update()

#If I preload all the images here, then it should speed up the program.

#Preload all images here for possible speed increase.

if main_logo_enable:
    selected_logo = pygame.image.load(logo_name).convert_alpha()
    #usaw_logo = pygame.image.load("usaw.gif").convert_alpha()
    #usapl_logo = pygame.image.load("usapl.png").convert_alpha()
    #badger_logo = pygame.image.load("badger.png").convert_alpha()
    #whspa_logo = pygame.image.load("whspa.png").convert_alpha()

#this sets the defualt logo
#selected_logo = rohr_logo

#light variables
#--------Left Side Referee-------------
#Main Light
red1 = 0
blue1 = 0
green1 = 0
#Red Card
red2 = 0
blue2 = 0
green2 = 0
#Blue Card
red3 = 0
blue3 = 0
green3 = 0
#Yellow Card
red4 = 0
blue4 = 0
green4 = 0

#--------Chief Referee---------------
#Main Light
red5 = 0
blue5 = 0
green5 = 0
#Red Card
red6 = 0
blue6 = 0
green6 = 0
#Blue Card
red7 = 0
blue7 = 0
green7 = 0
#Yellow Card
red8 = 0
blue8 = 0
green8 = 0

#--------Right Side Referee---------------
#Main Light
red9 = 0
blue9 = 0
green9 = 0
#Red Card
red10 = 0
blue10 = 0
green10 = 0
#Blue Card
red11 = 0
blue11 = 0
green11 = 0
#Yellow Card
red12 = 0
blue12 = 0
green12 = 0

#-----------------------------
#"input recieved circles"
red13 = 0
blue13 = 0
green13 = 0

red14 = 0
blue14 = 0
green14 = 0

red15 = 0
blue15 = 0
green15 = 0

#------------------------------
ref1_w_flag = 0
ref2_w_flag = 0
ref3_w_flag = 0

ref1_r_flag = 0
ref2_r_flag = 0
ref3_r_flag = 0
#------------------------------
timer_display = 0

# Keyboard Variables
#right refree "buttons"
leftDown = False
rightDown = False
upDown = False
downDown = False
#left refreee "buttons"
wDown = False
aDown = False
sDown = False
dDown = False

#Chief refree "buttons"
iDown = False
jDown = False
kDown = False
lDown = False

enterDown = False

spaceDown = False

ref1_flag = False
ref2_flag = False
ref3_flag = False



Timer_Enter = False
enable = 0

countdown = False

timer_init = True


left_input = False
chief_input = False
right_input = False

left_goodlift = False
left_nolift = False



chief_goodlift = False
chief_nolift = False


right_goodlift = False
right_nolift = False

left_red_card = False
clock_reset = False


bump_inputted = False


timer_edit_mode = False

start_selection_clock = False
start_selection_clock2 = False
start_selection_clock3 = False

selection_timer_init = False

Time2 = [1,0]#1st attempt selection timer
Time3 = [1,0]#2nd attempt selection timer
Time4 = [1,0]#3rd attempt selection timer

capsUp = False
capsDown = False

meet_break = False

timer1_running = False
timer2_active = False
timer3_active = False

selection_timer2_init = False
selection_timer3_init = False

autoclear_flag = False

tiny_green = True

third_attempt_mode = False

first_time_here = True

change_mind = True

no_decesion = True

manual_clock_reset = False #the manual reset variable
lights_shown = False #if true, then the decision is currently being displayed

reset_condition = False
dont_reset_the_timer = False
marksteiner_reset = False

audio_toggle = 0
menu_mode = False

multiply_Down = False
divide_Down = False

exit_menu = True

usapl_color = (255,0,0)
neenah_color = (0,148,71)
badger_color = (0,148,71)
whspa_color = (0,148,71)
anthem_color = (0,148,71)
usapl_logo_display = True
neenah_logo_display = False
badger_logo_display = False
whspa_logo_display = False


logo_changed = True


#-------------


x = 0
y = 0

attempt_timer_x = 0
attempt_timer_y = 0

attempt_timer2_x = 0
attempt_timer2_y = 0

attempt_timer3_x = 0
attempt_timer3_y = 0

scroll_lock_count = 0
#new stuff



Time = [1,0] # this array is the value of the clock


OriginalTime = list(Time)
Screen = max(pygame.display.list_modes())#initialize the screen 
Font = pygame.font.Font(".SafetyMedium.otf",dimensions.current_h/4)#sets font to cool digital clock (thats  necessary for IPF lights)
attempt_clock_font = pygame.font.Font(".SafetyMedium.otf", dimensions.current_h/8)#sets the font size of the smaller clock




#This code imports and plays the "beeping" sound
pygame.mixer.init()
pygame.mixer.music.load(".beep-08b.mp3")


def change_light():
    #print "The changelight function has been entered"
    
    global left_red_card, red14, red15, blue14, blue15, green14, green15, left_input, chief_input, right_input, chief_goodlift, chief_nolift, right_goodlift, right_nolift,left_nolift, left_goodlift, red13, green13, blue13, enable, Timer_Enter, ref1_flag, ref2_flag, ref3_flag, red1, blue1, green1, red2, blue2, green2, red3, blue3, green3, red4, blue4, green4, red5, blue5, green5, red6, blue6, green6, red7, blue7, green7, red8, blue8, green8, red9, blue9, green9, red10, blue10, green10, red11, blue11, green11, red12, blue12, green12
    global aDown, sDown, dDown, wDown, jDown, kDown, lDown, iDown, leftDown, downDown, rightDown, upDown, marksteiner_reset 


    if lDown and iDown: #this is the hard manual reset of the lights/timer
        manual_reset()
        iDown = False
        lDown = False


    if kDown and iDown:
        #this is a total screen clear, which will remove premature decesions
        marksteiner_reset = True
        manual_reset()

        kDown = False
        iDown = False

        
    #this section is for if we disable infraction cards and only have re/white.
    if jDown and iDown and not show_infraction_cards:
        manual_reset()
        jDown = False
        iDown = False


    
    #----LEFT SIDE REFEREE----------------

    if aDown and change_mind: #left red card
        red1 = 255
        green1 = 0
        blue1 = 0

        red2 = 255
        green2 = 0
        blue2 = 0

        ref1_flag = True
        left_goodlift = False
        left_nolift = True
        aDown = False

        #not sure why left_input is here?
        left_input = True
        #----TEST---------
        left_red_card = True

    if dDown and change_mind and show_infraction_cards: # left ref yellow card
        red1 = 255
        green1 = 0
        blue1 = 0

        red4 = 255
        green4 = 255
        blue4 = 0

        ref1_flag = True
        left_goodlift = False
        left_input = True
        left_nolift = True
        dDown = False

    if wDown and change_mind: #left ref good lift
        red1 = 255
        green1 = 255
        blue1 = 255

        red2 = 0
        green2 = 0
        blue2 = 0

        red3 = 0
        green3 = 0
        blue3 = 0

        red4 = 0
        green4 = 0
        blue4 = 0
        

        ref1_flag = True #goodlift flag
        left_goodlift = True
        left_input = True
        left_nolift = False
        wDown = False #I think by doing this we will eliminate all the raw nationals problem...




    if sDown and change_mind and show_infraction_cards: #left ref blue card
        red1 = 255
        green1 = 0
        blue1 = 0

        red3 = 0
        green3 = 0
        blue3 = 255
        
        
        ref1_flag = True #red flag
        left_goodlift = False
        left_input = True
        left_nolift = True

        sDown = False
#------------------------------------------
#-------Chief referee

    if iDown and change_mind: #chief ref good lift
        red5 = 255
        green5 = 255
        blue5 = 255

        red6 = 0
        green6 = 0
        blue6 = 0

        red7 = 0
        green7 = 0
        blue7 = 0

        red8 = 0
        green8 = 0
        blue8 = 0

        ref2_flag = True #goodlift flag
        chief_goodlift = True
        chief_input = True
        chief_nolift = False
        
        iDown = False

        
    if jDown and change_mind: #chief ref red card
        red5 = 255#color main light red
        green5 = 0
        blue5 = 0

        red6 = 255 #color red card
        green6 = 0
        blue6 = 0
        
        ref2_flag = 1 #nolift flag
        chief_goodlift = False
        chief_input = True
        chief_nolift = True
        jDown = False
        
        
    if lDown and change_mind and show_infraction_cards: # chief ref yellow card
        red5 = 255
        green5 = 0
        blue5 = 0

        red8 = 255
        green8 = 255
        blue8 = 0

        ref2_flag = True #nolift flag

        chief_goodlift = False
        chief_input = True
        chief_nolift = True

        lDown = False
        
    if kDown and change_mind and show_infraction_cards: #chief ref blue card
        red5 = 255
        green5 = 0
        blue5 = 0

        red7 = 0
        green7 = 0
        blue7 = 255

        ref2_flag = True #nolift flag
        chief_goodlift = False
        chief_input = True
        chief_nolift = True
        
        kDown = False
#-------------------------------------------------
        #RIGHT REFREEE 
    if upDown and change_mind:#right refree goodlift
        red9 = 255
        green9 = 255
        blue9 = 255

        red10 = 0
        green10 = 0
        blue10 = 0

        red11 = 0
        green11 = 0
        blue11 = 0

        red12 = 0
        green12 = 0
        blue12 = 0

        ref3_flag = True #goodlift flag
        right_goodlift = True
        right_input = True
        right_nolift = False

        upDown = False
        
    if leftDown and change_mind:
        red9 = 255 #color main light red
        green9 = 0
        blue9 = 0

        red10 = 255 #color red card
        green10 = 0
        blue10 = 0
        right_goodlift = False
        right_input = True

        ref3_flag = True #nolift flag
        right_nolift = True

        leftDown = False
 
    if downDown and change_mind and show_infraction_cards:
        red9 = 255 #color main light red
        green9 = 0
        blue9 = 0

        red11 = 0 #color blue card
        green11 = 0
        blue11 = 255

        ref3_flag = True
        right_goodlift = False
        right_input = True
        right_nolift = True
        
        downDown = False

    if rightDown and change_mind and show_infraction_cards: #color main light red
        red9 = 255
        green9 = 0
        blue9 = 0

        red12 = 255 #color yellow card
        green12 = 255
        blue12 = 0

        ref3_flag = True
        right_input = True
        right_goodlift = False
        right_nolift = True

        rightDown = False
    #--------------------------------


    #these two options keep manual resets from messing up the system on a IPF deluxe remote while running a Eco Deluxe software
    #print "the next line is the kDown!"
    if kDown and not show_infraction_cards:
        kDown = False

            
    if lDown and not show_infraction_cards:
        lDown = False 

        
# How to quit our program
def quitGame():
	pygame.quit()
	sys.exit()        



#---------------ADDING NEW TIMER STUFF---------------------------------

def Update():
    
    global exit_menu, multiply_Down, divide_Down, marksteiner_reset, reset_condition, ref1_flag, ref2_flag, ref3_flag, manual_clock_reset, scroll_lock_count, Time3, Time2, start_selection_clock2, attempt_timer2_x, attempt_timer2_y, Time3, Time4, attempt_timer3_x, attempt_timer3_y, selection_timer2_init, selection_timer3_init, timer2_active, timer3_active, timer1_running, capsDown, capsUp, clock_reset, x, y, timer_init, countdown, mode,Time, Timer_Enter, enable, start_selection_clock, selection_timer_init, attempt_timer_y, attempt_timer_x, Time2
    global timer_display, attempt_timer_display, main_clock_enable, start_selection_clock3

    if timer_display%2 == 0:
        main_clock_enable = True
    else:
        main_clock_enable = False

    #pygame.mixer.music.load(".beep-08b.mp3")

    if scroll_lock_count%2 == 0:
        Timer_Enter = False
        #scroll_lock_count = 0 # attempt to get clock to stop running after lights come on.
        if meet_break == False:
			Time = [1,0]

    else:
        Timer_Enter = True
        
    if multiply_Down and divide_Down:
        exit_menu = False
        print 'divide and multiply have been pushed!'

    
    if lDown and iDown: #this is the hard manual reset of the lights/timer
        manual_reset()


    if kDown and iDown:
        #this is a total screen clear, which will remove premature decesions
        marksteiner_reset = True
        manual_reset()


    
    if Timer_Enter and Time != [0,0]: #if the timer is currently paused/reset then this portion can be entered

        countdown = True #when true, means its currently counting down


        if timer_init: #if this is the first time approaching this statement, enter it
            
            x = pygame.time.get_ticks()
            #print 'x value is: '
           # print x
            
            timer_init = False # dont enter this unless the entire program restarts


        y = pygame.time.get_ticks()
        
        current_time = y-x

        if current_time > 900:
            #print current_time
            if (1000-current_time)>0:

                correction_factor = 0.001*(1000-current_time)
                time.sleep(correction_factor)

        
            Time[1] -= 1 #decrement the seconds hand always

            if Time[1] < 0: #if the seconds portion has reached zero
                Time[1] = 59 #reset the seonds portion then...l
                Time[0] -= 1#decrement the minute number

            if Time[0] == 0 and Time[1] == 30:
                print "30 seconds!"
                pygame.mixer.music.load(".beep-08b.mp3")
                #beep every second its in here
                pygame.mixer.music.play(0,0.0)
                pygame.mixer.music.play(0,0.0)

                
            if Time[0] == 0 and Time[1] < 11 and Time[1]>0:

                pygame.mixer.music.load(".beep-08b.mp3")
                #beep every second its in here
                pygame.mixer.music.play(0,0.0)
                
            
            if Time[1] == 0 and Time[0] == 0:
                Timer_Enter = False

                #this means the lifter's timer is zero, we need to play a buzz!
                pygame.mixer.music.load(".no_lift_buzzer.mp3")
                pygame.mixer.music.play(0,0.0)

            x = pygame.time.get_ticks()

     
#--------THIS IS AN ATTEMPT TO GET THE ATTEMPT TIMER TO SHOW UP WITHOUT FLASHING CONSTANTLY-------------
    if start_selection_clock: #if a decesion has been made, make this badboy true

        if selection_timer_init: #if this is the first time approaching this statement, enter it
            
            attempt_timer_x = pygame.time.get_ticks()
            selection_timer_init = False # dont enter this unless the entire program restarts

        
        attempt_timer_y = pygame.time.get_ticks()
        
        attempt_current_time = attempt_timer_y-attempt_timer_x

        if attempt_current_time > 940:
        
            Time2[1] -= 1 #decrement the seconds hand always

            if Time2[1] < 0: #if the seconds portion has reached zero
                
                Time2[1] = 59 #reset the seonds portion then...l
                Time2[0] -= 1#decrement the minute number

                timer1_running = True
                
            
            if Time2[1] == 0 and Time2[0] == 0:
                #Once the 1st timer is zero, we need to check to see if timer 2 has anything we can transfer over
                if timer2_active: #if timer 3 is active, transfer t3 data to t2
                    #If theres time left on 2, transfer it to spot 1
                    Time2[0] = Time3[0]
                    Time2[1] = Time3[1]
                    #check and see if theres time on 3, then transfer that to 2
                    if timer3_active:
                        Time3[0] = Time4[0]
                        Time3[1] = Time4[1]

                        Time4[0] = 0
                        Time4[1] = 1
                    else:

                        Time3[0] = 0
                        Time3[1] = 1

                else:
                    #If there isnt any data left on 2, then turn everything off and wait.
                    start_selection_clock = False
                    timer_init = True
                    timer1_running = False
                    Time2 = [1,0] #reset the clock for the next time.

            attempt_timer_x = pygame.time.get_ticks()

#------------------------------------------------------------------------------------------------------
#---------------------DO THE MATH FOR THE 2ND POSSIBLE ATTEMPT SELECTION TIMER------------------------

        if timer2_active: #if timer 2 is still activee

            #*********************
            if selection_timer2_init: #if this is the first time approaching this statement, enter it
               #print 'timer2 has been initiated'
                attempt_timer2_x = pygame.time.get_ticks()
                selection_timer2_init = False # dont enter this unless the entire program restarts

            attempt_timer2_y = pygame.time.get_ticks()
            attempt_current_time2 = attempt_timer2_y-attempt_timer2_x

            if attempt_current_time2 > 980:        
                Time3[1] -= 1 #decrement the seconds hand always

                if Time3[1] < 0: #if the seconds portion has reached zero
                    Time3[1] = 59 #reset the seonds portion then...l
                    Time3[0] -= 1#decrement the minute number
                    timer2_active = True
                    
                if Time3[1] == 0 and Time3[0] == 0:
                    print '2nd attempt timer is at 0'
                    #if timer3_active:
                     #   print 'Transfer timer 3 to timer 2!'
                        #If 3 is empty, but 4 is going, transfer to 4.
                      #  Time3[0] = Time4[0]
                       # Time3[1] = Time4[1]

                        #Time4[0] = 0
                        #Time4[1] = 1

                    #else:
                    #if there isnt any data left on 3, then turn it off
                    timer2_active = False
                    start_selection_clock2 = False
                attempt_timer2_x = pygame.time.get_ticks()
            #**********************
#------------------------------------------------------------------------------------------------------
#---------------------DO THE MATH FOR THE 3rd POSSIBLE ATTEMPT SELECTION TIMER------------------------

        if timer3_active: #if timer 2 is still activee
            #*********************
            if selection_timer3_init: #if this is the first time approaching this statement, enter it
               #print 'timer2 has been initiated'
                attempt_timer3_x = pygame.time.get_ticks()
                selection_timer3_init = False # dont enter this unless the entire program restarts

            attempt_timer3_y = pygame.time.get_ticks()
            attempt_current_time3 = attempt_timer3_y-attempt_timer3_x

            if attempt_current_time3 > 980:        
                Time4[1] -= 1 #decrement the seconds hand always

                if Time4[1] < 0: #if the seconds portion has reached zero
                    Time4[1] = 59 #reset the seonds portion then...l
                    Time4[0] -= 1#decrement the minute number
                if Time4[1] == 0 and Time4[0] == 0:
                    print 'Stop drawing clock #3'
                    timer3_active = False
                    start_selection_clock3 = False
                attempt_timer3_x = pygame.time.get_ticks()
            #**********************

#--------------

def Draw():
    global seleccted_logo, no_decesion, manual_clock_reset, scroll_lock_count, main_clock_enable, draw_attempt_timer_1, draw_attempt_timer_2, draw_attempt_timer_3,third_attempt_mode, red2, red3, red4, red6, red7, red8, red10, red11, red12, blue2, blue3, blue4, blue6, blue7, blue8, blue10, blue11, blue12, green2, green3, green4, green6, green7, green8, green10, green11, green12, chief_goodlift, chief_nolift, right_nolift, right_goodlift, tiny_green, left_nolift, left_goodlift, red9, green9, blue9, red5,green5, blue5, autoclear_flag, red1, green1, blue1,Time3, Time, meet_break, textFont, clock_reset, left_input, chief_input, right_input, red13, green13, blue13, red14, red15, blue15, blue14, green14, green15
    global logo_changed, usapl_logo, DRL_logo, show_infraction_cards, main_clock_master, main_logo_enable, opener_changes_allowed, opener_min_time


    surface.fill((0,0,0))
    #pygame.draw.rect(surface, (0,148,71),(0,0, dimensions.current_w, dimensions.current_h),10)

    #DRL_logo = pygame.image.load(".DRL Logo.png") #load in the image you want displayed

    scaled_logo = pygame.transform.scale(DRL_logo, (dimensions.current_w/8, dimensions.current_h/4)) #rescales the image based on the screen

    surface.blit(scaled_logo, (dimensions.current_w/25, dimensions.current_h/20)) #place the image with the left hand corner being (0,0)

    if not chief_input and not left_input and not right_input and  no_decesion and not meet_break:
        draw_main_logo = True
    elif meet_break and Time[0] >= 8:
        #This should draw the main logo during breaks, if no warning messages show up.
        draw_main_logo = True
    else:
        draw_main_logo = False


    #we need to redraw the decesision for 10 seconds

    
    if autoclear_flag:#system is armed THE MYSTERY HAS BEEN SOLVED!!!!

        tiny_green = False

       # print'drawing the main circles inside the draw function'
        #pygame.display.flip()

        #must redraw the main circles so long as 
        
        pygame.draw.circle(surface, (red1,green1,blue1), (((dimensions.current_w)/10)*2, (dimensions.current_h)/2), (dimensions.current_w)/10, 0) #LEFT MAIN
        pygame.draw.circle(surface, (red5,green5,blue5), ((dimensions.current_w)/2, (dimensions.current_h)/2), (dimensions.current_w)/10, 0) #CHIEF MAIN
        pygame.draw.circle(surface, (red9,green9,blue9), ((((dimensions.current_w)/10)*8), (dimensions.current_h)/2), (dimensions.current_w)/10, 0) #RIGHT MAIN


        if show_infraction_cards:

            #left referee infraction lights-----------------
            pygame.draw.circle(surface, (red2,green2,blue2), (((dimensions.current_w)/10)*1, ((dimensions.current_h)/100)*83), (dimensions.current_w/25),0)
            pygame.draw.circle(surface, (red3,green3,blue3), (((dimensions.current_w)/10)*2, ((dimensions.current_h)/100)*83), (dimensions.current_w/25),0)
            pygame.draw.circle(surface, (red4,green4,blue4), (((dimensions.current_w)/10)*3, ((dimensions.current_h)/100)*83), (dimensions.current_w/25),0)
            #----------------------------------------------------------------------------------
            #middle referee infraction lights-------------
            pygame.draw.circle(surface, (red6,green6,blue6), (((dimensions.current_w)/10)*4, ((dimensions.current_h)/100)*83), (dimensions.current_w/25),0)
            pygame.draw.circle(surface, (red7,green7,blue7), (((dimensions.current_w)/2), ((dimensions.current_h)/100)*83), (dimensions.current_w/25),0)
            pygame.draw.circle(surface, (red8,green8,blue8), (((dimensions.current_w)/10)*6, ((dimensions.current_h)/100)*83), (dimensions.current_w/25),0)
            #------------------------------------------------------------------------------------
            #middle refreee infraction lights-------------
            pygame.draw.circle(surface, (red10,green10,blue10), (((dimensions.current_w)/10)*7, ((dimensions.current_h)/100)*83), ((dimensions.current_w/25)),0)
            pygame.draw.circle(surface, (red11,green11,blue11), (((dimensions.current_w)/10)*8, ((dimensions.current_h)/100)*83), ((dimensions.current_w/25)),0)
            pygame.draw.circle(surface, (red12,green12,blue12), (((dimensions.current_w)/10)*9, ((dimensions.current_h)/100)*83), ((dimensions.current_w/25)),0)


        numberFont = pygame.font.Font(".SafetyMedium.otf",(dimensions.current_w/16)) #sets the font size, needs to be a percentage of the screen width

        red_card_ref_1 = numberFont.render ('1', 0,(0, 0, 0))#sets text color and content
        blue_card_ref_1 = numberFont.render ('2', 0,(0, 0, 0))#sets text color and content
        yellow_card_ref_1 = numberFont.render ('3', 0,(0, 0, 0))#sets text color and content

        red_card_ref_2 = numberFont.render ('1', 0,(0, 0, 0))#sets text color and content
        blue_card_ref_2 = numberFont.render ('2', 0,(0, 0, 0))#sets text color and content
        yellow_card_ref_2 = numberFont.render ('3', 0,(0, 0, 0))#sets text color and content

        red_card_ref_3 = numberFont.render ('1', 0,(0, 0, 0))#sets text color and content
        blue_card_ref_3 = numberFont.render ('2', 0,(0, 0, 0))#sets text color and content
        yellow_card_ref_3 = numberFont.render ('3', 0,(0, 0, 0))#sets text color and content
        #print dimensions.current_w


        x = ((dimensions.current_w)/10)*1
        y = ((dimensions.current_h)/100)*83

        r = dimensions.current_w/25



        

        
        surface.blit(red_card_ref_1, (((dimensions.current_w)/10)*1-(r/4),(((dimensions.current_h)/100)*83)-r)) #places the text on the screen at desired coordinates

        surface.blit(blue_card_ref_1, ((((dimensions.current_w)/10)*2)-(r/2),(((dimensions.current_h)/100)*83)-r)) #places the text on the screen at desired coordinates

        surface.blit(yellow_card_ref_1, (((dimensions.current_w)/10)*3-(r/2),(((dimensions.current_h)/100)*83)-r)) #places the text on the screen at desired coordinates


        surface.blit(red_card_ref_2, (((dimensions.current_w)/10)*4-(r/4),(((dimensions.current_h)/100)*83)-r)) #places the text on the screen at desired coordinates
        surface.blit(blue_card_ref_2, (((dimensions.current_w)/10)*5-(r/2),(((dimensions.current_h)/100)*83)-r)) #places the text on the screen at desired coordinates
        surface.blit(yellow_card_ref_2, (((dimensions.current_w)/10)*6-(r/2),(((dimensions.current_h)/100)*83)-r)) #places the text on the screen at desired coordinates

        surface.blit(red_card_ref_3, (((dimensions.current_w)/10)*7-(r/4),(((dimensions.current_h)/100)*83)-r)) #places the text on the screen at desired coordinates
        surface.blit(blue_card_ref_3, (((dimensions.current_w)/10)*8-(r/2),(((dimensions.current_h)/100)*83)-r)) #places the text on the screen at desired coordinates
        surface.blit(yellow_card_ref_3, (((dimensions.current_w)/10)*9-(r/2),(((dimensions.current_h)/100)*83)-r)) #places the text on the screen at desired coordinates



        if left_goodlift: #recolor the small dot white so it appears it has dissapeared
           # print 'print left goodlift tiny circle being drawn'    
            red13 = 255
            green13 = 255
            blue13 = 255
            pygame.draw.circle(surface, (red13, green13, blue13), ((((dimensions.current_w)/10)*2), (dimensions.current_h)/2), (dimensions.current_w)/40, 0)
                
        if left_nolift: #the lfit is either good, or bad, if its bad, make the dot red to hide it
           # print 'print left nolift tiny circle being drawn'
            red13 = 255
            green13 = 0
            blue13 = 0
            pygame.draw.circle(surface, (red13, green13, blue13), ((((dimensions.current_w)/10)*2), (dimensions.current_h)/2), (dimensions.current_w)/40, 0)

        if chief_goodlift:

            red14 = 255
            blue14 = 255
            green14 = 255
            pygame.draw.circle(surface, (red14, green14, blue14), ((dimensions.current_w)/2, (dimensions.current_h)/2), (dimensions.current_w)/40, 0)


        if chief_nolift:

            red14 = 255
            blue14 = 0
            green14 = 0
            pygame.draw.circle(surface, (red14, green14, blue14), ((dimensions.current_w)/2, (dimensions.current_h)/2), (dimensions.current_w)/40, 0)


        if right_nolift:

            red15 = 255
            blue15 = 0
            green15 = 0
            pygame.draw.circle(surface, (red15, green15, blue15), ((((dimensions.current_w)/10)*8), (dimensions.current_h)/2), (dimensions.current_w)/40, 0)


        if right_goodlift:

            red15 = 255
            blue15 = 255
            green15 = 255
            pygame.draw.circle(surface, (red15, green15, blue15), ((((dimensions.current_w)/10)*8), (dimensions.current_h)/2), (dimensions.current_w)/40, 0)

        




    
    if left_input and tiny_green and not meet_break:#a decesion has been inputted, make sure not to delete the icons
        #we need to recolor/redraw the status circles so long as the screen hasnt been cleared by the timer/program

        if manual_clock_reset:
            print'we have a manual clock reset'
            #we need to keep the dot black
            red13 = 0
            green13 = 0
            blue13 = 0
            manual_clock_reset = False
            left_input = False #shot in the dark here
            ref1_flag = False
            

        else:
            #print'drawing the left green dot!'
            red13 = 0
            green13 = 148
            blue13 = 71

    if chief_input and tiny_green and not meet_break:
        if manual_clock_reset:
            #we need to keep the dot black
            red14 = 0
            green14 = 0
            blue14 = 0
            manual_clock_reset = False
            chief_input = False #shot in the dark here
            ref2_flag = False

        else:
            red14 = 0
            green14 = 148
            blue14 = 71

        
        #pygame.display.flip()
    if right_input and tiny_green and not meet_break:


        if manual_clock_reset:
            #we need to keep the dot black
            red15 = 0
            green15 = 0
            blue15 = 0
            manual_clock_reset = False
            right_input = False #shot in the dark here
            ref3_flag = False

            

        else:
            red15 = 0
            green15 = 148
            blue15 = 71
        
    pygame.draw.circle(surface, (red13, green13, blue13), ((((dimensions.current_w)/10)*2), (dimensions.current_h)/2), (dimensions.current_w)/40, 0)
    pygame.draw.circle(surface, (red14, green14, blue14), ((dimensions.current_w)/2, (dimensions.current_h)/2), (dimensions.current_w)/40, 0)
    pygame.draw.circle(surface, (red15, green15, blue15), ((((dimensions.current_w)/10)*8), (dimensions.current_h)/2), (dimensions.current_w)/40, 0)

        
    #------draws the main clock-------------------------------
   
    t1 = str(Time[0]) #converts the minute area into a string
    if len(t1) == 1: t1 = t1 #if the string has something in it, do nothing
    t2 = str(Time[1])

    #print t2 + "this is the string version of the seconds"
    if len(t2) == 1: t2 = "0"+t2
 
    string = t1 + ":" + t2  #this creates the screen
    
    clock = Font.render (string, 0,(225,228,0))#sets text color and content



    if main_clock_enable and main_clock_master:
        
        surface.blit(clock, ((dimensions.current_w/100)*37,dimensions.current_h/38)) #places the text on the screen at desired coordinates


    #going to add a 3rd attempt mode, this will disable attempt selection timers.

    #-----draw the attempt timer screen--------------------

    #we need to only draw this if the timer is actually active


    

    if start_selection_clock and  not third_attempt_mode and draw_attempt_timer_1:
        #print third_attempt_mode
    
        t11 = str(Time2[0]) #converts the minute area into a string
        if len(t11) == 1: t11 = t11 #if the string has something in it, do nothing
        t22 = str(Time2[1])

        #print t2 + "this is the string version of the seconds"
        if len(t22) == 1: t22 = "0"+t22
 
        attempt_string = t11 + ":" + t22  #this creates the string
    
        attempt_clock = attempt_clock_font.render (attempt_string, 0,(225,228,0))#sets text color and content

        surface.blit(attempt_clock, ((dimensions.current_w/100)*20,(dimensions.current_h/100)*91)) #places the text on the screen at desired coordinates

        textFont = pygame.font.Font(".SafetyMedium.otf",(dimensions.current_w/47)) #sets the font for the numbers

        attempt_message = textFont.render('ATTEMPT', 0,(225,228,0))
        attempt_message2 = textFont.render('SELECTION', 0, (225,228,0))

        surface.blit(attempt_message, ((((dimensions.current_w)/100)*4),((dimensions.current_h/100)*94)))
        surface.blit(attempt_message2, ((((dimensions.current_w)/100)*4),((dimensions.current_h/100)*98)))
#***************************************************************************************************************************
    #insert the 2nd attempt selection timer in here, this is going to get tricky.



    if start_selection_clock2 and not third_attempt_mode and draw_attempt_timer_2:

        #print 'the drawing code for timer 2 is active'
        
        t111 = str(Time3[0]) #converts the minute area into a string
        if len(t111) == 1: t111 = t111 #if the string has something in it, do nothing
        t222 = str(Time3[1])

        #print t2 + "this is the string version of the seconds"
        if len(t222) == 1: t222 = "0"+t222
 
        attempt2_string = t111 + ":" + t222  #this creates the screen
    
        attempt2_clock = attempt_clock_font.render (attempt2_string, 0,(225,228,0))#sets text color and content

        surface.blit(attempt2_clock, ((dimensions.current_w/100)*45,(dimensions.current_h/100)*91)) #places the text on the screen at desired coordinates

#***************************************************************************************************************************************************
    #This is where the 3rd attempt selection timer code needs to go.
    if start_selection_clock3 and not third_attempt_mode and draw_attempt_timer_3:

        #print 'the drawing code for timer 3 is active'
        t1111 = str(Time4[0]) #converts the minute area into a string
        if len(t1111) == 1: t1111 = t1111 #if the string has something in it, do nothing
        t2222 = str(Time4[1])

        #print t2 + "this is the string version of the seconds"
        if len(t2222) == 1: t2222 = "0"+t2222
        attempt3_string = t1111 + ":" + t2222  #this creates the screen
        attempt3_clock = attempt_clock_font.render (attempt3_string, 0,(225,228,0))#sets text color and content
        surface.blit(attempt3_clock, ((dimensions.current_w/100)*70,(dimensions.current_h/100)*91)) #places the text on the screen at desired coordinates





#------------------------------------------------------------------------------------------------------------------------------------------------------------


    if third_attempt_mode:
        #the timers are already disabled, this portion is to place a message stating that were in 3rd attempt mode.



        third_message_Font = pygame.font.Font(".SafetyMedium.otf",dimensions.current_w/23)
        third_message = third_message_Font.render('3rd ATTEMPTS', 0,(0, 148, 71))


        #surface.blit(third_message, (((dimensions.current_w)/100*4),((dimensions.current_h/100)*93)))









#***************************************************************************************************************************


    if meet_break: #if meetbreak is shown we need to periodically display warning messages about openeing changes
        safety_Font = pygame.font.Font(".SafetyMedium.otf",dimensions.current_w/20)



        #print 'meet break has been detected'
        #if Time[0] <= 7 and Time [0] >=3: # display this warning from 4:00 to 3:45
        if Time[0] <= (opener_min_time+4) and Time [0] >=opener_min_time and opener_changes_allowed: # display this warning from 4:00 to 3:45

            opener_change = str(Time[0]-opener_min_time)

            warning_string = opener_change + ":" + t2
            

            warning_message = safety_Font.render ('Time left to change openers', 0, (255,0,0))
            time_left = attempt_clock_font.render(warning_string, 0, (255,0,0))

            
            surface.blit(warning_message, ((((dimensions.current_w)/100)*12),((dimensions.current_h/100)*40)))
            surface.blit(time_left, ((((dimensions.current_w)/100)*40),((dimensions.current_h/100)*55))) 
            
        if Time[0] <= (opener_min_time-1) and Time[1] <= 59 and opener_changes_allowed :
            # this displays the "no more changes" message 
            
            warning_message1 = safety_Font.render ('NO MORE CHANGES TO OPENERS', 0, (255,0,0))
    
            surface.blit(warning_message1, ((((dimensions.current_w)/100)*4),((dimensions.current_h/100)*50)))

            if Time[0] == 0 and Time[1] == 0:
                meet_break = False
                Timer_Enter = True#playing around with this value
                #Time = [1,0]
                Time = [1,0]
                scroll_lock_count += 1
                



    #we only need to draw this when nothing is going on. So we need to have a variable that will determine when its okay to display the logo
                

    #This is the code that will display the main logo in the middle of the screen


    if draw_main_logo and main_logo_enable:
        #This is the potion that will actually draw the logo on the screen.


        #Get the size of the photo, to see its shape.
        
        #print dimensions.current_w
        #print dimensions.current_h

        image_dimensions = selected_logo.get_rect().size
        #print image_dimensions[0]
        #print image_dimensions[1]

        scaling_factor = 57

        x_scale = (((float(dimensions.current_h/100)*scaling_factor))*float(image_dimensions[0]))/(float(image_dimensions[1]))
    
        scaled_main_logo = pygame.transform.scale(selected_logo, ((int(x_scale)),(dimensions.current_h/100)*scaling_factor))
        
        logo_position = scaled_main_logo.get_rect()
        
        logo_position.centerx = (dimensions.current_w/100)*50 #this should be the middle of the screen
        logo_position.centery = (dimensions.current_h/100)*62               
        surface.blit(scaled_main_logo, logo_position)




    #------------------------------------------------------
        pygame.display.flip() #update the screen
        clock_reset = False
    #----------------------------------------------------------
def third_attempt_change():
    #we need to import the two timer variables. and decrement in here like we would normally
    
    global bump_inputted, start_selection_clock, selection_timer_init, attempt_timer_x, selection_timer_init, attempt_timer_y, attempt_current_time, Time2, timer1_running, Time3, timer2_active, timer3_active, selection_timer2_init, attempt_timer2_x, selection_timer2_init, attempt_timer2_y, attempt_current_time2, start_selection_clock2, start_selection_clock3
    global third_bump_enabled, timer3_active, selection_timer3_init, attempt_timer3_x, attempt_timer3_y, Time4, start_selection_clock3


    #print '3rd attempt change function entered'

    loopcount = 0
    text_red = 0
    text_blue = 0
    text_green = 0

    #pygame.draw.rect(surface, (0,148,71),(0,0, dimensions.current_w, dimensions.current_h),10)

    logo = pygame.image.load(".DRL Logo.png") #load in the image you want displayed

    scaled_logo = pygame.transform.scale(logo, (dimensions.current_w/8, dimensions.current_h/4)) #rescales the image based on the screen

    Dodge_Font = pygame.font.Font(".SafetyMedium.otf",dimensions.current_w/16)
    
    while bump_inputted and third_bump_enabled: #so long as this variable is true, we need to stay in this loop and keep pasting over the screen with the Rohr Message
        surface.fill((0,0,0))
        #--------THIS IS AN ATTEMPT TO GET THE ATTEMPT TIMER TO SHOW UP WITHOUT FLASHING CONSTANTLY-------------
     #--------THIS IS AN ATTEMPT TO GET THE ATTEMPT TIMER TO SHOW UP WITHOUT FLASHING CONSTANTLY-------------
        if start_selection_clock: #if a decesion has been made, make this badboy true

            if selection_timer_init: #if this is the first time approaching this statement, enter it
                
                attempt_timer_x = pygame.time.get_ticks()
                selection_timer_init = False # dont enter this unless the entire program restarts

            
            attempt_timer_y = pygame.time.get_ticks()
            
            attempt_current_time = attempt_timer_y-attempt_timer_x

            if attempt_current_time > 940:
            
                Time2[1] -= 1 #decrement the seconds hand always

                if Time2[1] < 0: #if the seconds portion has reached zero
                    
                    Time2[1] = 59 #reset the seonds portion then...l
                    Time2[0] -= 1#decrement the minute number

                    timer1_running = True
                    
                
                if Time2[1] == 0 and Time2[0] == 0:
                    #Once the 1st timer is zero, we need to check to see if timer 2 has anything we can transfer over
                    if timer2_active: #if timer 3 is active, transfer t3 data to t2
                        #If theres time left on 2, transfer it to spot 1
                        Time2[0] = Time3[0]
                        Time2[1] = Time3[1]
                        #check and see if theres time on 3, then transfer that to 2
                        if timer3_active:
                            Time3[0] = Time4[0]
                            Time3[1] = Time4[1]

                            Time4[0] = 0
                            Time4[1] = 1
                        else:

                            Time3[0] = 0
                            Time3[1] = 1

                    else:
                        #If there isnt any data left on 2, then turn everything off and wait.
                        start_selection_clock = False
                        timer_init = True
                        timer1_running = False
                        Time2 = [1,0] #reset the clock for the next time.

                attempt_timer_x = pygame.time.get_ticks()

    #------------------------------------------------------------------------------------------------------
    #---------------------DO THE MATH FOR THE 2ND POSSIBLE ATTEMPT SELECTION TIMER------------------------

            if timer2_active: #if timer 2 is still activee

                #*********************
                if selection_timer2_init: #if this is the first time approaching this statement, enter it
                   #print 'timer2 has been initiated'
                    attempt_timer2_x = pygame.time.get_ticks()
                    selection_timer2_init = False # dont enter this unless the entire program restarts

                attempt_timer2_y = pygame.time.get_ticks()
                attempt_current_time2 = attempt_timer2_y-attempt_timer2_x

                if attempt_current_time2 > 980:        
                    Time3[1] -= 1 #decrement the seconds hand always

                    if Time3[1] < 0: #if the seconds portion has reached zero
                        Time3[1] = 59 #reset the seonds portion then...l
                        Time3[0] -= 1#decrement the minute number
                        timer2_active = True
                        
                    if Time3[1] == 0 and Time3[0] == 0:
                        print '2nd attempt timer is at 0'
                        #if timer3_active:
                         #   print 'Transfer timer 3 to timer 2!'
                            #If 3 is empty, but 4 is going, transfer to 4.
                          #  Time3[0] = Time4[0]
                           # Time3[1] = Time4[1]

                            #Time4[0] = 0
                            #Time4[1] = 1

                        #else:
                        #if there isnt any data left on 3, then turn it off
                        timer2_active = False
                        start_selection_clock2 = False
                    attempt_timer2_x = pygame.time.get_ticks()
                #**********************
    #------------------------------------------------------------------------------------------------------
    #---------------------DO THE MATH FOR THE 3rd POSSIBLE ATTEMPT SELECTION TIMER------------------------

            if timer3_active: #if timer 2 is still activee
                #*********************
                if selection_timer3_init: #if this is the first time approaching this statement, enter it
                   #print 'timer2 has been initiated'
                    attempt_timer3_x = pygame.time.get_ticks()
                    selection_timer3_init = False # dont enter this unless the entire program restarts

                attempt_timer3_y = pygame.time.get_ticks()
                attempt_current_time3 = attempt_timer3_y-attempt_timer3_x

                if attempt_current_time3 > 980:        
                    Time4[1] -= 1 #decrement the seconds hand always

                    if Time4[1] < 0: #if the seconds portion has reached zero
                        Time4[1] = 59 #reset the seonds portion then...l
                        Time4[0] -= 1#decrement the minute number
                    if Time4[1] == 0 and Time4[0] == 0:
                        print 'Stop drawing clock #3'
                        timer3_active = False
                        start_selection_clock3 = False
                    attempt_timer3_x = pygame.time.get_ticks()
                #**********************
            #**********************

        

        if loopcount%2 == 0:
            text_red = 255
            text_blue = 0
            text_green = 0
            #pygame.draw.rect(surface, (0,148,71),(0,0, dimensions.current_w, dimensions.current_h),10)
            surface.blit(scaled_logo, (dimensions.current_w/25, dimensions.current_h/20))

        else:
            
            text_red = 255
            text_blue = 255
            text_green = 255
            #pygame.draw.rect(surface, (0,148,71),(0,0, dimensions.current_w, dimensions.current_h),10)
            surface.blit(scaled_logo, (dimensions.current_w/25, dimensions.current_h/20))


        

        bump_message1 = Dodge_Font.render('ATTENTION', 0,(text_red,text_blue,text_green))
        bump_message2 = Dodge_Font.render('   ATTEMPT CHANGE', 0,(text_red, text_blue, text_green))#sets text color and content
        bump_message3 = Dodge_Font.render('HAS BEEN SUBMITTED', 0,(text_red, text_blue, text_green))

        surface.blit(bump_message1, ((((dimensions.current_w)/20)*6),((dimensions.current_h)/4)))
        surface.blit(bump_message2, (((dimensions.current_w)/8),((dimensions.current_h)/2)))
        surface.blit(bump_message3, (((dimensions.current_w)/8),((dimensions.current_h)/4)*3))

        loopcount += 1
        
        pygame.display.update()

        time.sleep(0.5)
        
        #print 'while loop for 3rd attempt change entered'







        #check for the exit condition
        for event in GAME_EVENTS.get():

		if event.type == pygame.KEYUP:
                    
                        if event.key == pygame.K_NUMLOCK: #if the exit key is pressed, make the boolean variable false and exit
                            bump_inputted = False
                            
    
#---------------------------------------------------------------------------

def timer_update():
    #this function will allow the user to change the duration of the main timer for breaks and what not

    global meet_break, Time, timer_edit_mode, scroll_lock_count

    #when a key is pressed we need to enter a "modify timer mode" then exit when another key is pressed.

    safety_Font = pygame.font.Font(".SafetyMedium.otf",dimensions.current_h/9)
    timer_message = safety_Font.render('Timer Edit Mode', 0,(0, 148, 71))
    
    
    #print 'inside timer update, timer_edit_mode is....'
    #print timer_edit_mode
    first_key = False
    first_input = 0
    nd_input = 0


    while timer_edit_mode:
        for event in GAME_EVENTS.get(): #we need to listen for keystrokes....

            if event.type == pygame.KEYDOWN and ~first_key:
                    
                if event.key == pygame.K_KP0:
                    #time.sleep(1)
                    first_key = True
                    Time = [0,0]
                    first_input = 0

                elif event.key == pygame.K_KP1:
                    #time.sleep(1)
                    first_key = True
                    Time = [1,0]
                    first_input = 1

                elif event.key == pygame.K_KP2:
                    #time.sleep(1)
                    first_key = True
                    Time = [2,0]
                    first_input = 2

                elif event.key == pygame.K_KP3:
                    #time.sleep(1)
                    first_key = True
                    Time = [3,0]
                    first_input = 3

                elif event.key == pygame.K_KP4:
                    #time.sleep(1)
                    first_key = True
                    Time = [4,0]
                    first_input = 4

                elif event.key == pygame.K_KP5:
                    #time.sleep(1)
                    first_key = True
                    Time = [5,0]
                    first_input = 5

                elif event.key == pygame.K_KP6:
                    #time.sleep(1)
                    first_key = True
                    Time = [6,0]
                    first_input = 6

                elif event.key == pygame.K_KP7:
                    #time.sleep(1)
                    first_key = True
                    Time = [7,0]
                    first_input = 7

                elif event.key == pygame.K_KP8:
                    #time.sleep(1)
                    first_key = True
                    Time = [8,0]
                    first_input = 8

                elif event.key == pygame.K_KP9:
                    #time.sleep(1)
                    first_key = True
                    Time = [9,0]
                    first_input = 9

                    
                time.sleep(1)

            #---------this deals with double digit entries to the system


        for event in GAME_EVENTS.get(): #we need to listen for keystrokes....


            if event.type == pygame.KEYDOWN and first_key:
                    
                if event.key == pygame.K_KP0: 

                    second_input = 0
                    actual_time = (second_input) + first_input*10
                    Time = [actual_time,0]

                if event.key == pygame.K_KP1: 
                    second_input = 1
                    actual_time = (second_input) + first_input*10
                    Time = [actual_time,0]

                if event.key == pygame.K_KP2: 
                    second_input = 2
                    actual_time = (second_input) + first_input*10
                    Time = [actual_time,0]

                if event.key == pygame.K_KP3: 
                    second_input = 3
                    actual_time = (second_input) + first_input*10
                    Time = [actual_time,0]

                if event.key == pygame.K_KP4: 
                    second_input = 4
                    actual_time = (second_input) + first_input*10
                    Time = [actual_time,0]

                if event.key == pygame.K_KP5: 
                    second_input = 5
                    actual_time = (second_input) + first_input*10
                    Time = [actual_time,0]

                if event.key == pygame.K_KP6: 
                    second_input = 6
                    actual_time = (second_input) + first_input*10
                    Time = [actual_time,0]

                if event.key == pygame.K_KP7: 
                    second_input = 7
                    actual_time = (second_input) + first_input*10
                    Time = [actual_time,0]

                if event.key == pygame.K_KP8: 
                    second_input = 8
                    actual_time = (second_input) + first_input*10
                    Time = [actual_time,0]

                if event.key == pygame.K_KP9: 
                    second_input = 9
                    actual_time = (second_input) + first_input*10
                    Time = [actual_time,0]

                    
            if event.key == pygame.K_KP_ENTER: #if the exit key is pressed, make the boolean variable false and exit
                
                timer_edit_mode = False
                print Time
                scroll_lock_count = 0
                if Time[0] >= 5:
                    meet_break = True #if the timer has been set for 5 min or greater, we need to display opener change warnings
                    #print 'a timer duration greater than 5 minutes has been detected'
                else:
                    meet_break = False
            

        surface.blit(timer_message, (((dimensions.current_w)/8),((dimensions.current_h)/4)*3)) #prints the 'timer edit mode message to the screen'
        pygame.display.flip()
        
    
#-----------------------------------------------------------------------------------------------------------------------------------


def screen_clear(): #this is the clear everything function
    global marksteiner_reset, reset_condition, no_decesion, tiny_green, Timer_Enter, Time, red1, red2, red3, red4, red5, red6, red7, red8, red9, red10, red11, red12, red13, red14, red15, blue1, blue2, blue3, blue4, blue5, blue6, blue7, blue8, blue9, blue10, blue11, blue12, blue13, blue14, blue15, green1, green2, green3, green4, green5, green6, green7, green8, green9, green10, green11, green12, green13, green14, green15, left_nolift, left_goodlift, ref1_flag, ref2_flag, ref3_flag, left_input, chief_input, right_input, left_nolift, chief_nolift, right_nolift, autoclear_flag, first_time_here, change_mind

    no_decesion = True #this resets the ability to enter the change light function
    tiny_green = True #this allows green dots to be drawn next time.
            
    Timer_Enter = False

    if reset_condition:
        
        #nothing really needs to be here.
        print 'blah'

    elif marksteiner_reset:
        print'marksteiner reset'

    else:
        #Time = [1,0]
        #print 'heres your problem, Scott!'
        print ''

    red1 = 0
    green1 = 0
    blue1 = 0

    red2 = 0
    green2 = 0
    blue2 = 0

    red3 = 0
    green3 = 0
    blue3 = 0

    red4 = 0
    green4 = 0
    blue4 = 0

    red5 = 0
    green5 = 0
    blue5 = 0

    red6 = 0
    green6 = 0
    blue6 = 0

    red7 = 0
    green7 = 0
    blue7 = 0

    red8 = 0
    green8 = 0
    blue8 = 0

    red9 = 0
    green9 = 0
    blue9 = 0

    red10 = 0
    green10 = 0
    blue10 = 0

    red11 = 0
    green11 = 0
    blue11 = 0

    red12 = 0
    green12 = 0
    blue12 = 0

    red13 = 0
    green13 = 0
    blue13 = 0

    red14 = 0
    green14 =0
    blue14 = 0

    red15 = 0
    green15 = 0
    blue15 = 0

    left_nolift = False
    left_goodlift = False

    ref1_flag = False
    ref2_flag = False
    ref3_flag = False


    left_input = False #this should remove the tiny green circles
    chief_input = False
    right_input = False

    left_red_card = False

    left_nolift = False
    chief_nolift = False
    right_nolift = False

    autoclear_flag = False

    first_time_here = True

    change_mind = True
    pygame.display.update() #this is what actually updates all the "changes"
    marksteiner_reset = False
    


def manual_reset():
    global marksteiner_reset, lights_shown, Time, scroll_lock_count, reset_condition
    print 'sanity check'
    if lights_shown:
        #we need to only reset the clock
        print 'a manual reset was detected while the lights were currently on'
        Time = [1,0]
        scroll_lock_count = 0
        reset_condition = True

    elif marksteiner_reset:
        print 'a marksteiner reset has been initated'
        #just clear the dots!
        screen_clear()
    else:
        #this is a normal manual reset condition
        print 'a normal manual reset was detected squirtle'
        Time = [1,0]
        scroll_lock_count = 0 
        screen_clear()


def audio_output():
    #this will allow the scoretable remote to select which output medium they want, analog or digital
    global audio_toggle, surface


    textFont = pygame.font.Font(".SafetyMedium.otf",(dimensions.current_w/40))
    
    audio_toggle = audio_toggle + 1
    
    if audio_toggle%2 == 0:
        os.system('amixer cset numid=3 2') #sets the audio output to digital
        audio_message = textFont.render('HDMI', 0,(0,148,71))
 
    else:
        os.system('amixer cset numid=3 1') #sets the audio output to analog
        audio_message = textFont.render('ANALOG', 0,(0,148,71))
                

    surface.blit(audio_message, ((((dimensions.current_w)/20)*6),((dimensions.current_h)/60)))
    pygame.display.flip()
    time.sleep(2)
                

#--------------------------------------------------------------------------------------------------------------------------------------
def drl_menu():
    #This will be used to select the logo displayed in the middle,
    global selected_logo, exit_menu, multiply_Down, divide_Down, menu_mode, usapl_color, neenah_color, badger_color, whspa_color, anthem_color, usapl_logo_display, neenah_logo_display, badger_logo_display, whspa_logo_display
    global logo_changed, usapl_logo, neenah_logo, badger_logo, whspa_logo
    play_national_anthem = False
    while not exit_menu:
            
        surface.fill((0,0,0))
        #pygame.draw.rect(surface, (0,148,71),(0,0, dimensions.current_w, dimensions.current_h),10)
        logo = pygame.image.load(".DRL Logo.png") #load in the image you want displayed
        scaled_logo = pygame.transform.scale(logo, (dimensions.current_w/8, dimensions.current_h/4)) #rescales the image based on the screen
        surface.blit(scaled_logo, (dimensions.current_w/25, dimensions.current_h/20))

        Dodge_Font = pygame.font.Font(".SafetyMedium.otf",dimensions.current_w/16)
        bump_message1 = Dodge_Font.render('Menu', 0,(0,148,71))
        menu_message = bump_message1.get_rect()
        menu_message.centerx = (dimensions.current_w/100)*50
        menu_message.centery = (dimensions.current_h/100)*25
        surface.blit(bump_message1, menu_message)

        
        Dodge_Font2 = pygame.font.Font(".SafetyMedium.otf",dimensions.current_w/30)
        message2 = Dodge_Font2.render('Use keypad to select desired option', 0,(0,148,71))
        menu_message2= message2.get_rect()
        menu_message2.centerx = (dimensions.current_w/100)*50
        menu_message2.centery = (dimensions.current_h/100)*40
        surface.blit(message2, menu_message2)

        message3 = Dodge_Font2.render('Then press enter', 0,(0,148,71))
        menu_message3= message3.get_rect()
        menu_message3.centerx = (dimensions.current_w/100)*50
        menu_message3.centery = (dimensions.current_h/100)*50
        surface.blit(message3, menu_message3)

        message4 = Dodge_Font2.render('1.  USAPL', 0,(usapl_color))
        menu_message4= message4.get_rect()
        menu_message4.centerx = (dimensions.current_w/100)*10
        menu_message4.centery = (dimensions.current_h/100)*65
        surface.blit(message4, menu_message4)

        message5 = Dodge_Font2.render('2. NEENAH', 0,(neenah_color))
        menu_message5= message4.get_rect()
        menu_message5.centerx = (dimensions.current_w/100)*10
        menu_message5.centery = (dimensions.current_h/100)*75
        surface.blit(message5, menu_message5)

        message6 = Dodge_Font2.render('3. BADGER OPEN', 0,(badger_color))
        menu_message6= message4.get_rect()
        menu_message6.centerx = (dimensions.current_w/100)*10
        menu_message6.centery = (dimensions.current_h/100)*85
        surface.blit(message6, menu_message6)

        message7 = Dodge_Font2.render('4. WHSPA', 0,(whspa_color))
        menu_message7= message4.get_rect()
        menu_message7.centerx = (dimensions.current_w/100)*10
        menu_message7.centery = (dimensions.current_h/100)*95
        surface.blit(message7, menu_message7)

        message8 = Dodge_Font2.render('5. PLAY NATIONAL ANTHEM', 0,(anthem_color))
        menu_message8= message4.get_rect()
        menu_message8.centerx = (dimensions.current_w/100)*50
        menu_message8.centery = (dimensions.current_h/100)*65
        surface.blit(message8, menu_message8)

        #Now we need to listen for user input.

        #The command below plays a video quite well.
        #os.system('omxplayer national_anthem.mp4')

        pygame.display.update()

        print 'menu mode entered'
        for event in GAME_EVENTS.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP1:
                    #they want to display the usapl logo
                    usapl_color = (255,0,0)
                    neenah_color = (0,148,71)
                    badger_color = (0,148,71)
                    whspa_color = (0,148,71)
                    anthem_color = (0,148,71)

                    usapl_logo_display = True
                    neenah_logo_display = False
                    badger_logo_display = False
                    whspa_logo_display = False

                    play_national_anthem = False
                    logo_changed = True
                    
                if event.key == pygame.K_KP2:
                    #they want to show the neenah logo
                    usapl_color = (0,148,71)
                    neenah_color = (255,0,0)
                    badger_color = (0,148,71)
                    whspa_color = (0,148,71)
                    anthem_color = (0,148,71)

                    usapl_logo_display = False
                    neenah_logo_display = True
                    badger_logo_display = False
                    whspa_logo_display = False

                    play_national_anthem = False
                    logo_changed = True
                    
                if event.key == pygame.K_KP3:
                    #they want to show the badger logo
                    usapl_color = (0,148,71)
                    neenah_color = (0,148,71)
                    badger_color = (255,0,0)
                    whspa_color = (0,148,71)
                    anthem_color = (0,148,71)

                    usapl_logo_display = False
                    neenah_logo_display = False
                    badger_logo_display = True
                    whspa_logo_display = False

                    play_national_anthem = False
                    logo_changed = True
                    
                if event.key == pygame.K_KP4:
                    #they want to show the whspa logo
                    usapl_color = (0,148,71)
                    neenah_color = (0,148,71)
                    badger_color = (0,148,71)
                    whspa_color = (255,0,0)
                    anthem_color = (0,148,71)

                    usapl_logo_display = False
                    neenah_logo_display = False
                    badger_logo_display = False
                    whspa_logo_display = True
                    play_national_anthem = False

                    logo_changed = True
                    
                if event.key == pygame.K_KP5:
                    #they want to play the national anthem
                    usapl_color = (0,148,71)
                    neenah_color = (0,148,71)
                    badger_color = (0,148,71)
                    whspa_color = (0,148,71)
                    anthem_color = (255,0,0)
                    play_national_anthem = True

                    usapl_logo_display = False
                    neenah_logo_display = False
                    badger_logo_display = False
                    whspa_logo_display = False
                    
                if event.key == pygame.K_KP_ENTER: #if the exit key is pressed, make the boolean variable false and exit
                    #check to see which logo is going to be shown, if any.
                    if usapl_logo_display:
                        #make the appropriate string the correct filename
                        selected_logo = usapl_logo
                    if neenah_logo_display:
                        selected_logo = neenah_logo
                    if badger_logo_display:
                        selected_logo = badger_logo
                    if whspa_logo_display:
                        selected_logo = whspa_logo
                    if play_national_anthem:
                        surface.fill((0,0,0))
                        pygame.display.update()
                        os.system('omxplayer national_anthem.mp4')

                    exit_menu = True
                    divide_Down = False
                    multiply_Down = False
                    print 'enter button detected'
                    play_national_anthem = False
                            
                if event.key == pygame.K_n:
                        quitGame()
    
                if event.type == GAME_GLOBALS.QUIT:
			quitGame()


#------------------------------------------------------------------
def get_ip_address(ifname):
    #This function gets the IP address for us when fed 'eth0'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
#--------------------------------------------------------------------
def display_ip_address():
    #this will do the formatting to display the IP address.
    textFont = pygame.font.Font(".SafetyMedium.otf",(dimensions.current_w/40))

    try:
        ip_address = textFont.render("IP address:" + get_ip_address('eth0'), 0,(0,148,71))
    except:
        try:
            ip_address = textFont.render("IP address:" + get_ip_address('wlan0'), 0,(0,148,71))

        except:
            ip_address = textFont.render("Not connected to a network", 0,(0,148,71))


    
    surface.blit(ip_address, ((((dimensions.current_w)/20)*6),((dimensions.current_h)/50)))
    pygame.display.flip()
    time.sleep(10)
    
    
                

#--------------------------------------------------------------------------------------------------------------------------------------



while True:
        #--------------
        #NEW STUFF
       
        pygame.display.update()
        #-----------------

        '''VERY IMPORTANT CODE HERE! ITS WHAT MAKES EVERYTHING HAPPEN ONCE ALL THE JUDGES MAKE THEIR DECESION'''
        
        if ref1_flag and ref2_flag and ref3_flag:#if everybody has made their decesion, display it!
        #if left_input and right_input and chief_input:
            #we only enter this once all 3 refs inputs have been recorded
            
             

            
            #we need to document the exact time we entered here.
#------------------THIS IS ALL NEW STUFF TO MAKE THE DECESION NOT COME UP FOR 2 SECONDS TO GIVE THE LAST REF A CHANCE AT DOUBLE PUSH--
            if first_time_here: #is true

                display_timer_1 = pygame.time.get_ticks()
                first_time_here = False #so we dont enter here on the next iteration.

            display_timer_2 = pygame.time.get_ticks()

            if display_timer_2 - display_timer_1 > 1000: #1 second delay
#----------------------------------------------------------------------------

                if reset_condition:
                    #print 'reset condition is:'
                    #print reset_condition
                    reset_condition = False #this should allow the lights to reset automatically after a manual reset

                #once we enter this if statement, the lights are displayed. We need to establish a variable to differentiate the two types of resets


                lights_shown = True #this is the attempt to fix the rohr scenario.
                '''--------------------------------------------------------------------'''
                
                
                no_decesion = False

                #we need to put some sort of conditional statement here that only allows all the "resetting" to be done 2 seconds after all decesions have came in, so all refs have a chance to submit more than 1 infaction

                scroll_lock_count = 0 # attempt to get clock to stop running after lights come on.
                Time = [1,0] #This is part of the raw nats update, lets the clock start again immedately. 
            
                #print "a referee decesion has been detected"
           
                ref1_flag = False
                ref2_flag = False
                ref3_flag = False

                autoclear_flag = True #this is the variable that allows 10 second clearing of the screen
                #print ' '
                #print 'autoclear is: '
                #print autoclear_flag
                #print ' '

                #but now we need to recolor the green dot to the decesion.
                if left_goodlift: #recolor the small dot white so it appears it has dissapeared
                
                    red13 = 255
                    green13 = 255
                    blue13 = 255
                    pygame.draw.circle(surface, (red13, green13, blue13), ((((dimensions.current_w)/10)*2), (dimensions.current_h)/2), (dimensions.current_w)/40, 0)
                
                if left_nolift: #the lfit is either good, or bad, if its bad, make the dot red to hide it
            
                    red13 = 255
                    green13 = 0
                    blue13 = 0
                    pygame.draw.circle(surface, (red13, green13, blue13), ((((dimensions.current_w)/10)*2), (dimensions.current_h)/2), (dimensions.current_w)/40, 0)
                
            #-------------------------------------------------------------
                if chief_goodlift:
                #print 'chief goodlift has been detected'
                    red14 = 255
                    green14 = 255
                    blue14 = 255
                    pygame.draw.circle(surface, (red14,green14,blue14), ((dimensions.current_w)/2, (dimensions.current_h)/2), (dimensions.current_w)/40, 0)
               
                
                if chief_nolift: #the lfit is either good, or bad, if its bad, make the dot red to hide it
                #print 'chief nolift has been detected'
                    red14 = 255
                    green14 = 0
                    blue14 = 0
                    pygame.draw.circle(surface, (red14,green14,blue14), ((dimensions.current_w)/2, (dimensions.current_h)/2), (dimensions.current_w)/40, 0)


            #------------------------------------------------------------


                
                if right_goodlift:
                #print 'right goodlift has been detected'
                    red15 = 255
                    green15 = 255
                    blue15 = 255
                    pygame.draw.circle(surface, (red15,green15,blue15), ((((dimensions.current_w)/10)*8), (dimensions.current_h)/2), (dimensions.current_w)/40, 0)
                
                if right_nolift: #the lfit is either good, or bad, if its bad, make the dot red to hide it
                #print 'right nolift has been detected'
                    red15 = 255
                    green15 = 0
                    blue15 = 0
                    pygame.draw.circle(surface, (red15,green15,blue15), ((((dimensions.current_w)/10)*8), (dimensions.current_h)/2), (dimensions.current_w)/40, 0)
           # pygame.display.update()

                left_nolift = False
                left_goodlift = False

                ref1_flag = False
                ref2_flag = False
                ref3_flag = False


                left_input = False #this should remove the tiny green circles
                chief_input = False
                right_input = False

                left_red_card = False

                left_nolift = False
                chief_nolift = False
                right_nolift = False

                change_mind = False

           

            #---------------SELECTION CLOCK VARIABLE!!!----------------------
                start_selection_clock = True
                selection_timer_init = True
            #Time2 = [1,0]

                if timer2_active:
                    print 'I think a referee decision came in after the 2nd clock was running'
                    timer3_active = True #this activates the 2nd timer, if the 1st is still running.
                    selection_timer3_init = True
                    Time4 = [1,0]
                    start_selection_clock3 = True

                

                if timer1_running and not timer2_active:
                #print 'a 2nd decesion has came in while 1 timer is running'
                    timer2_active = True #this activates the 2nd timer, if the 1st is still running.
                    selection_timer2_init = True
                    Time3 = [1,0]

                    start_selection_clock2 = True

                #else:
                    #Time2 = [1,0]

               # if timer2_active:
                #    print 'I think a referee decision came in after the 2nd clock was running'
                 #   timer3_active = True #this activates the 2nd timer, if the 1st is still running.
                  #  selection_timer3_init = True
                   # Time4 = [1,0]
                    #start_selection_clock3 = True
            
            #----------------------------------------------------------------
            

            #pygame.display.update()

            #This is going to be the portion of the code that will audibly play a buzzer if its a "nolift

            
                if right_nolift and left_nolift or right_nolift and chief_nolift or left_nolift and chief_nolift:
            #load the music and play the buzzer!

                #print 'nolift has been detected'

                    pygame.mixer.music.load(".no_lift_buzzer.mp3")
                    pygame.mixer.music.play(0,0.0) #play the buzzer once\

      
        #This is the autoclear portion that gets rid of the lights at 10 seconds afterward.
        if autoclear_flag and Time2[1] == 50 or Time3[1] == 50 or Time4[1] == 50:

            #print 'autoclear statement has been entered'

            #the purpose of this is to clear the referee decesion once 10 seconds has passed.
            #seems to work fine.


            screen_clear()
            lights_shown = False



	# Get a list of all events that happened since the last redraw VERY IMPORTANT!!!!!!
	for event in GAME_EVENTS.get():

		if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_KP9 and Dual_Mode:

                            if selected_logo != usaw_logo:
                                print 'change mode to usaw'
                                #we need to change to usaw
                                selected_logo = usaw_logo
                                #Configuration Settings.
                                show_infraction_cards = False
                                third_bump_enabled = False
                                opener_changes_allowed = False
                              
                            else:
                                selected_logo = usapl_logo
                                show_infraction_cards = True
                                third_bump_enabled = True
                                opener_changes_allowed = True

                    

                        if event.key == pygame.K_KP0:
                            display_ip_address()#show the IP address on the screen for easier livestreaming.

                        if event.key == pygame.K_KP_DIVIDE and event.key == pygame.K_KP_MULTIPLY:
                            menu_mode = True
                            
                        if event.key == pygame.K_KP_PERIOD:
                            audio_output()
                            
                            #os.system('amixer cset numid=3 1') #sets the sudio output to analog


                        if event.key == pygame.K_KP_MINUS:
                            manual_reset()
                            meet_break = False
                            print "minus key was pressed"


                            #this will need to be uncommented after testing
                            #Time = [1,0]
                            #scroll_lock_count = 0

                            

                        if event.key == pygame.K_KP_DIVIDE:

                            #third_attempt_mode = True
                            #divide_Down = True
                            #This allows for the toggling of the main timer on/off
                            timer_display += 1

                        if event.key == pygame.K_KP_MULTIPLY:

                            #third_attempt_mode = False
                            #multiply_Down = True

                            if third_attempt_mode:
                                third_attempt_mode = False
                                
                            else:
                                third_attempt_mode = True

                    
                        if event.key == pygame.K_SCROLLOCK:
                            capsDown = True
                            print 'scroll lock down detected'

                            scroll_lock_count +=1


                        if event.key == pygame.K_BACKSPACE:
                            capsDown = True
                            print 'scroll lock down detected'

                            scroll_lock_count +=1

                        if event.key == pygame.K_KP_PLUS:

                            if main_clock_master:
                                timer_edit_mode = True #this will enter the timer edit mode
                    
                        if event.key == pygame.K_NUMLOCK:
                            screen_clear()
                            bump_inputted = True
                            
                            
                        #-----LEFT REF DECESISIONS AND KEYS
                        if event.key == pygame.K_w:
                            wDown = True

                            left_input = True
                            print 'LEFT REFEREE PUSHED A BUTTON!'

                            
			if event.key == pygame.K_a:#if left arrow is pressed
			    aDown = True
			    left_red_card = True
			    #left_input = True
			    #RED CARD LEFT REF
			if event.key == pygame.K_s:#if right arrow is pressed
			    sDown = True
			    #left_input = True
			    #BLUE CARD LEFT REF
                        if event.key == pygame.K_d: #if down arrow is pressed
                            dDown = True
                            #left_input = True
                            #YELLOW CARD LEFT REF
                        #-----------------------------------
                        #----Chief Referee
                        if event.key == pygame.K_i:
                            iDown = True
                        if event.key == pygame.K_j:
                            jDown = True
                        if event.key == pygame.K_k:
                            kDown = True
                        if event.key == pygame.K_l:
                            lDown = True

                        #------------------------------------
                            #-----Right Refreee
                        if event.key == pygame.K_UP:
                            upDown = True
                        if event.key == pygame.K_LEFT:
                            leftDown = True
                        if event.key == pygame.K_DOWN:
                            downDown = True
                        if event.key == pygame.K_RIGHT:
                            rightDown = True

                        #----------------------------------
                            #Right Referee 2.0 Compatability
                        if event.key == pygame.K_t:
                            upDown = True
                        if event.key == pygame.K_f:
                            leftDown = True
                        if event.key == pygame.K_g:
                            downDown = True
                        if event.key == pygame.K_h:
                            rightDown = True

                        if event.key == pygame.K_c:
                            scroll_lock_count += 1
#---------------------------------------------------------------------------------

                        if event.key == pygame.K_RETURN: #if the enter button is pushed
                            enterDown = True
                            time.sleep(0.5)
                            
#--------------------------------------------------------------------------------------

			if event.key == pygame.K_ESCAPE:
				quitGame()
#-------------------------------------------------------------


				#I think this entire section is responsible for fucking up raw nats.
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SCROLLOCK:
                            capsUp = True
                            print'scroll lock up detected'

                        if event.key == pygame.K_BACKSPACE:
                            capsUp = True
          

 #----------------------------------------------------   

                        #if event.key == pygame.K_RETURN: #HIT RETURN KEY TO CLEAR
                            #enterDown = False
                        if event.key == pygame.K_KP_DIVIDE:
                            divide_Down = False
                        if event.key == pygame.K_KP_MULTIPLY:
                            multiply_Down = False
                           

		if event.type == GAME_GLOBALS.QUIT:
			quitGame()




        if no_decesion and not meet_break:
    
            change_light()
            
	
	Update()
        Draw()
        third_attempt_change()
        timer_update()
        #drl_menu()
        
	


