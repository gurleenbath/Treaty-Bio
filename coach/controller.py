import time

from coach.get_motion import *
from coach.get_feedback import *
from coach.get_suggestion import *
from coach.shared_variables import *


class coach_main():
    def __init__(self):
        self.was_connected = False

        #creating threads
        self.motion = threading.Thread(target=get_motion)
        self.suggestion = threading.Thread(target=get_suggestion)
        #self.sound = threading.Thread(target=self.get_feedback)
        self.sound_tts = threading.Thread(target=get_feedback_tts)

        # running threads
        # These threads use the shared variables to determine what action to take
        # create finite state machine to coordinate get shot data, get_motion -> get_suggestion -> get_feedback

        self.motion.start()
        self.suggestion.start()
        #self.sound.start()
        self.sound_tts.start()

    def run(self):
        global connection_state
        global connection_lock
        global connection_tries
        global speaker
        global speaker_lock
        global command
        global command_lock
        global shots
        global makes
        global continue_variable

        while continue_variable:
            ##connecting
            #telling the user the ble device is connecting
            if connection_state == 0:
                self.wait_for_speaker()
                speaker_lock.acquire()
                speaker = 1
                speaker_lock.release()
            #waiting for connection
            self.tries = 0
            while connection_state !=1 and self.tries<connection_tries:
                self.tries += 1
                time.sleep(0.5)
            #telling the user they are connected if they weren't
            if connection_state == 1 and  not self.was_connected:
                wait_for_speaker()
                speaker_lock.acquire()
                speaker = 2
                speaker_lock.release()
                self.was_connected = True
            ##getting data
            if connection_state == 1:
                #asking for user input
                choice = 0
                while not choice in [1,2]:
                    choice = int(input('\n\nShots:'+str(shots)+' '+'\nMakes:'+\
                    str(makes)+'\n\nPlease make a selection.\n\t1) Record Shot'+\
                    '\n\t2) Exit'))
                    if not choice in [1,2]:
                        sys.stdout('\n\nPlease select 1) or 2).')
                #recording data
                if choice == 1:
                    while command != 0:
                        time.sleep(0.1)
                    command_lock.acquire()
                    command = 1
                    command_lock.release()
                    while command != 0:
                        time.sleep(0.1)
                    #getting suggestion
                    command_lock.acquire()
                    command = 2
                    command_lock.release()
                    while command != 0:
                        time.sleep(0.1)
                else:
                    continue_variable = False

    def getShotData(self):
        global continue_variable
        global command

        while continue_variable:
            while command != 0:
                time.sleep(0.1)
            command_lock.acquire()
            command = 1
            command_lock.release()

    def getSuggestion(self):
        global continue_variable
        global command
        

        while continue_variable:
            while command != 0:
                time.sleep(0.1)
            command_lock.acquire()
            command = 2
            rows=motion_data.shape()[0]
            result = motion_data['suggestion'][rows-1]
            command_lock.release()
            
        return result
