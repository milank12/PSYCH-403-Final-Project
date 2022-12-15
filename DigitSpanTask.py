#Digit Task Code
#This experiment tests the working memory of the participant. Known to be associated with cintelligence and language learning ability, working memory can be tested using a simple digit span task. The experiment presents a sequence of random digits between 1-9, with which they are tasked with remembering and reentering into the program immediately after presentation of the digits. The program measures how many digits are entered correctly.
#Code written by Milan Kalra




#=====================
#IMPORT MODULES
#=====================
import random
import numpy as np
import pandas as pd
import os
from psychopy import visual, monitors, core, event
from psychopy import gui
from datetime import datetime

#=====================
#PATH SETTINGS
#=====================
directory = os.getcwd()
path = os.path.join(directory, 'dataFiles')
if not os.path.exists(path):
   os.makedirs(path)
#=====================
#COLLECT PARTICIPANT INFO
#=====================
expInfo = {'subject_nr':0}
myDlg = gui.DlgFromDict(dictionary=expInfo)
expInfo['date'] = datetime.now() 
filename = (str(expInfo['subject_nr']) + '_outputFile.csv')

#=====================
#STIMULUS AND TRIAL SETTINGS
#=====================
nTrials = 5
nBlocks = 3
totalTrials = nTrials*nBlocks

#=====================
#PREPARE CONDITION LISTS
#=====================

trials = []
for i in range(totalTrials):
    currentTrial = [random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9)]
    trials.append(currentTrial)


#=====================
#PREPARE DATA COLLECTION LISTS
#=====================
blockNumbers = [0]*totalTrials
trialNumbers = [0]*totalTrials
number = [0]*totalTrials
response = [0]*totalTrials
num_accurate = [0]*totalTrials


#=====================
#CREATION OF WINDOW AND STIMULI
#=====================
mon = monitors.Monitor('myMonitor', width=35.56, distance=60)
mon.setSizePix([1920, 1080])
win = visual.Window(
 fullscr=False, 
 monitor=mon, 
 size=(600,600), 
 color='black', 
 units='pix'
)
#=====================
#START EXPERIMENT
#=====================
instructText = visual.TextStim(win, text='A sequence of nine numbers will appear. After the sequence concludes, please type the numbers in order in the box that appears. Type as many as you can remember. Afterwards, press return to begin the next trial.')
fixation = visual.TextStim(win, text='+', color='white')
instructText.draw()
win.flip()
event.waitKeys()
#=====================
#BLOCK SEQUENCE
#=====================
# execute this code once for each block

for iblock in range(nBlocks):
    # define block start message, present block start message
    instructText.text = 'Press any key to begin Block ' + str(iblock+1)
    instructText.draw()
    # create window, wait for participant to start trial with key press
    win.flip()
    event.waitKeys()
    #=====================
    #TRIAL SEQUENCE
    #=====================  
    for itrial in range(nTrials):        
        # record trial number and block number for each trial
        overallTrial = iblock*nTrials+itrial
        blockNumbers[overallTrial] = iblock+1
        trialNumbers[overallTrial] = itrial+1
        #get the nine numbers from the trial as a string
        trialString = ""
        for currentnumber in trials[overallTrial]:
            trialString += str(currentnumber)
        currentWord = trials[overallTrial][0]
        number[overallTrial] = int(trialString)
        
        #=====================
        #START TRIAL
        #=====================
        # draw stimulus, draw fixation
        currentTrial = trials[overallTrial]
        for stimnumber in currentTrial:
            fixation.draw()
            # flip window
            win.flip() 
            core.wait(0.5)
            experimentText = visual.TextStim(win, text='+', color='white')
            experimentText.text = str(stimnumber)
            experimentText.draw()
            win.flip()
            core.wait(0.5)
            
        textBox = visual.TextStim(win, text='Enter Text', color='white')
        textBox.draw()
        win.flip()
        loop = True
        while loop:
            keys=event.waitKeys(keyList=['1','2','3','4','5','6','7','8','9', 'return'])
            if keys:
                keyPressed = keys[0]
                if keyPressed == 'return':
                    loop = False
                    break
                if textBox.text == "Enter Text":
                    textBox.text = keyPressed
                else:
                    textBox.text = textBox.text + keyPressed
            textBox.draw()
            win.flip()
        win.flip()
        
        # end trial when participant responds
        currentResponse = textBox.text
        if len(currentResponse) > 9:
            currentResponse = currentResponse[0:9]
        if len(currentResponse) < 9:
            currentResponse = currentResponse + "0"*(9-len(currentResponse))
        response[overallTrial] = currentResponse
        for pos in range(len(currentResponse)):
            print(pos)
            letter = currentResponse[pos]
            if str(letter) == str(currentTrial[pos]):
                num_accurate[overallTrial] = num_accurate[overallTrial] + 1

#======================
# END OF EXPERIMENT
#======================

df = pd.DataFrame(data={
 "Block Number": blockNumbers, 
 "Trial Number": trialNumbers,
 "Response": response,
 "Number": number,
 "Number Accurate": num_accurate
})
df.to_csv(os.path.join(path, filename), sep=',', index=False)

# close window
win.close()