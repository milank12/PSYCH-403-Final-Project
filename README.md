# PSYCH-403-Final-Project

Digit Task Code

This experiment tests the working memory of the participant. Known to be associated with intelligence and language learning ability, working memory can be tested using a simple digit span task. The experiment presents a sequence of random digits between 1-9, with which they are tasked with remembering and reentering into the program immediately after presentation of the digits. The program measures how many digits are entered correctly.

After a inputting their information (age, handedness, subject number), participants are presented with an instruction message that describes their task, which they can begin after pressing any button. They begin each of three blocks with a prompt message which lets them start the block when they are ready with a key press. The trials constist of alternating fixations and random digits. The fixations and digits are presented for 0.5 seconds each, after which a textbox that says "Enter Text Here" appears. From here, participants can type in their nine digit response, attempting to correctly remember the nine digits that were presented and their order. The experiment repeats for three blocks, each with five trials (this can be changed if necessary in the stimulus and trial settings). Finally, after a completion message plays, the experiment ends.

The program records the participants response for each trial, along with the block number, trial number, the presented nine value string, and the number of digits correctly remembered for each trial. These are recorded and saved in a csv file at the current working directory. The program also prints the mean of the accurate number of digits per trial over all the trials for ease of use for the experimenter. 

This experiment judges the average digit span of the participant. This is useful to assess working memory performance, which may be measured as a test of intelligence that is not influenced by other factors such as socioeconomic status, and can be particularly useful in understanding cognitive deficits and performance for those with brain injuries or mental disabilities.

Code written by Milan Kalra
