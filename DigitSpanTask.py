#Digit Task Code
#This experiment tests the working memory of the participant. Known to be associated with intelligence and language learning ability, working memory can be tested using a simple digit span task. The experiment presents a sequence of random digits between 1-9, with which they are tasked with remembering and reentering into the program immediately after presentation of the digits. The program measures how many digits are entered correctly.
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
directory = os.getcwd() #get current working directory
path = os.path.join(directory, 'dataFiles') #make data files go to current working directory
if not os.path.exists(path):
   os.makedirs(path)
#=====================
#COLLECT PARTICIPANT INFO
#=====================
expInfo = {'subject_nr':0, 'age':0, 'handedness':('right','left','ambi')} #collect participant info
myDlg = gui.DlgFromDict(dictionary=expInfo)
expInfo['date'] = datetime.now()  #collect date of experiment
filename = (str(expInfo['subject_nr']) + '_outputFile.csv')

#=====================
#STIMULUS AND TRIAL SETTINGS
#=====================
nTrials = 5 #number of trials per trial
nBlocks = 3 #number of blocks
totalTrials = nTrials*nBlocks #number of total trials

#=====================
#PREPARE CONDITION LISTS
#=====================

trials = []
for i in range(totalTrials): #for loop to append trials list to add 9 random integers between 1 and 9
    currentTrial = [random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9), random.randint(1, 9)]
    trials.append(currentTrial)


#=====================
#PREPARE DATA COLLECTION LISTS
#=====================
#create empty lists for datat collection
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

instructText = visual.TextStim(win, text='A sequence of nine numbers will appear. After the sequence concludes, please type the numbers in order in the box that appears. Type as many as you can remember. Afterwards, press return to begin the next trial. Press any key to begin the experiment.') #start message
fixation = visual.TextStim(win, text='+', color='white') #create fixation cross
instructText.draw() #draw instructions
win.flip() #present instructions
event.waitKeys() #wait for participant to press key to begin first block
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
        for stimnumber in currentTrial: #draw stimuli (digits) nine times
            fixation.draw()
            # flip window
            win.flip() 
            core.wait(0.5)
            experimentText = visual.TextStim(win, text='+', color='white') #create stimuli text
            experimentText.text = str(stimnumber) #present random number as string
            experimentText.draw()
            win.flip() 
            core.wait(0.5)
            
        textBox = visual.TextStim(win, text='Enter Text', color='white')  #create and present textbox to record answer
        textBox.draw()
        win.flip()
        loop = True
        while loop: #while loop to record multiple keys
            keys=event.waitKeys(keyList=['1','2','3','4','5','6','7','8','9', 'return']) #list of digits that can be entered
            if keys:
                keyPressed = keys[0] #create list of keys that are pressed
                if keyPressed == 'return': #if the return key is pressed, break the loop and move on to the next trial
                    loop = False
                    break
                if textBox.text == "Enter Text": #if the text box contains "Enter Text," add the key press (for the first key press)
                    textBox.text = keyPressed
                else: #for each key press, add it to the running list of digits that have been recorded
                    textBox.text = textBox.text + keyPressed 
            textBox.draw()
            win.flip() #present the textbox
        win.flip()  
        
        # end trial when participant responds
        currentResponse = textBox.text #change the response to what has been recorded in the textbox
        if len(currentResponse) > 9: #if the length of the response is greater than 9, slice the string to contain only the first 9 digits (delete extra keypresses)
            currentResponse = currentResponse[0:9]
        if len(currentResponse) < 9: #if the length of the response is less than 9, fill the rest of the required digits with "0" (this will avoid the program crashing if the participant does not remember every digit and doesn't fill the box with 9 characters)
            currentResponse = currentResponse + "0"*(9-len(currentResponse))
        response[overallTrial] = currentResponse
        for pos in range(len(currentResponse)): #for each digit the participant types, check if it matches the actual digit, increase the number of correct digits by one
            letter = currentResponse[pos]
            if str(letter) == str(currentTrial[pos]):
                num_accurate[overallTrial] = num_accurate[overallTrial] + 1
end_expText = visual.TextStim(win, text='You have now completed all trials. Press any key to end the experiment.')
end_expText.draw()
win.flip()
event.waitKeys()
win.close()

#======================
# END OF EXPERIMENT
#======================
#record data for block number, trial number, the response, the given number, and how many numbers were correctly answered
df = pd.DataFrame(data={
 "Block Number": blockNumbers, 
 "Trial Number": trialNumbers,
 "Response": response,
 "Number": number,
 "Number Accurate": num_accurate
})
df.to_csv(os.path.join(path, filename), sep=',', index=False) #save the data as a csv file

mean_accurate = df["Number Accurate"].mean() #calculate and print the mean of accurate digits remembered over the entire experiment
print(mean_accurate)

# close window
win.close()