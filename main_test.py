
#from __future__ import print_function
import sys
import os
import time
import pandas as pd
from abc import abstractmethod

from blue_st_sdk.manager import Manager
from blue_st_sdk.manager import ManagerListener
from blue_st_sdk.node import NodeListener
from blue_st_sdk.feature import FeatureListener
from blue_st_sdk.features.audio.adpcm.feature_audio_adpcm import FeatureAudioADPCM
from blue_st_sdk.features.audio.adpcm.feature_audio_adpcm_sync import FeatureAudioADPCMSync

from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression

from scipy.integrate import simps

data = ''
suggestions = ['ns', 'ft', 'cw', 'bl', 'ei', 'ss', 'sf', 'so']
#ns no suggestion, ft follow through, cw cock wrist, bl bend legs, ei elbow in,
#ss square sholder, sf shoot faster, so shoot in one continuous motion
NOTIFICATIONS = 40
SCANNING_TIME_s = 5

def print(output=''):
    global data
    output = str(output)+'\n'
    data += output
    sys.stdout.write(output+'\n')

# INTERFACES

#
# Implementation of the interface used by the Manager class to notify that a new
# node has been discovered or that the scanning starts/stops.
#
class MyManagerListener(ManagerListener):

    #
    # This method is called whenever a discovery process starts or stops.
    #
    # @param manager Manager instance that starts/stops the process.
    # @param enabled True if a new discovery starts, False otherwise.
    #
    def on_discovery_change(self, manager, enabled):
        print('Discovery %s.' % ('started' if enabled else 'stopped'))
        if not enabled:
            print()

    #
    # This method is called whenever a new node is discovered.
    #
    # @param manager Manager instance that discovers the node.
    # @param node    New node discovered.
    #
    def on_node_discovered(self, manager, node):
        print('New device discovered: %s.' % (node.get_name()))


#
# Implementation of the interface used by the Node class to notify that a node
# has updated its status.
#
class MyNodeListener(NodeListener):

    #
    # To be called whenever a node connects to a host.
    #
    # @param node Node that has connected to a host.
    #
    def on_connect(self, node):
        print('Device %s connected.' % (node.get_name()))

    #
    # To be called whenever a node disconnects from a host.
    #
    # @param node       Node that has disconnected from a host.
    # @param unexpected True if the disconnection is unexpected, False otherwise
    #                   (called by the user).
    #
    def on_disconnect(self, node, unexpected=False):
        print('Device %s disconnected%s.' % \
            (node.get_name(), ' unexpectedly' if unexpected else ''))
        if unexpected:
            # Exiting.
            print('\nExiting...\n')
            sys.exit(0)


#
# Implementation of the interface used by the Feature class to notify that a
# feature has updated its data.
#
class MyFeatureListener(FeatureListener):

    _notifications = 0
    """Counting notifications to print only the desired ones."""

    #
    # To be called whenever the feature updates its data.
    #
    # @param feature Feature that has updated.
    # @param sample  Data extracted from the feature.
    #
    def on_update(self, feature, sample):
        if self._notifications < NOTIFICATIONS:
            self._notifications += 1
            print(feature)

def get_feedback(speaker):
    if speaker == 'cg':
        os.system('omxplayer /sounds/connecting.mp3')
    elif  speaker == 'cd':
        os.system('omxplayer /sounds/connected.mp3')
    elif  speaker == 'ud':
        os.system('omxplayer /sounds/unconnected.mp3')
    elif  speaker == 'rd':
        os.system('omxplayer /sounds/ready.mp3')
    elif  speaker == 'nd':
        os.system('omxplayer /sounds/noDeviceFound.mp3')
    elif  speaker == 'ce':
        os.system('omxplayer /sounds/cantConnectGoodbye.mp3')
    elif  speaker == 'bl':
        os.system('omxplayer /sounds/bendYourLegs.mp3')
    elif  speaker == 'st':
        os.system('omxplayer /sounds/shoot.mp3')
    elif  speaker == 'ft':
        os.system('omxplayer /sounds/followThrough.mp3')
    elif  speaker == 'cw':
        os.system('omxplayer /sounds/cockYourWrist.mp3')
    elif  speaker == 'ei':
        os.system('omxplayer /sounds/elbowIn.mp3')
    elif  speaker == 'ss':
        os.system('omxplayer /sounds/squareShoulders.mp3')
    elif  speaker == 'sf':
        os.system('omxplayer /sounds/shootFaster.mp3')
    elif  speaker == 'sm':
        os.system('omxplayer /sounds/shootInOneMotion.mp3')

def main(argv):
    global data

    try:

        motion_data = pd.read_csv('motion_data.csv')
        suggestion_data = pd.read_csv('suggestion_data.csv')

        # Creating Bluetooth Manager.
        manager = Manager.instance()
        manager_listener = MyManagerListener()
        manager.add_listener(manager_listener)

        while True:
            print(data)
            # Synchronous discovery of Bluetooth devices.
            print('Scanning Bluetooth devices...\n')
            manager.discover(SCANNING_TIME_s)

            # Alternative 1: Asynchronous discovery of Bluetooth devices.
            #manager.discover(SCANNING_TIME_s, True)

            # Alternative 2: Asynchronous discovery of Bluetooth devices.
            #manager.start_discovery()
            #time.sleep(SCANNING_TIME_s)
            #manager.stop_discovery()

            # Getting discovered devices.
            discovered_devices = manager.get_nodes()

            # Listing discovered devices.
            if not discovered_devices:
                print('No Bluetooth devices found. Exiting...\n')
                sys.exit(0)
            print('Available Bluetooth devices:')
            i = 1
            for device in discovered_devices:
                print('%d) %s: [%s]' % (i, device.get_name(), device.get_tag()))
                i += 1

            # Selecting a device.
            while True:
                choice = int(
                    input("\nSelect a device to connect to (\'0\' to quit): "))
                if choice >= 0 and choice <= len(discovered_devices):
                    break
            if choice == 0:
                # Exiting.
                manager.remove_listener(manager_listener)
                print('Exiting...\n')
                sys.exit(0)
            device = discovered_devices[choice - 1]
            node_listener = MyNodeListener()
            device.add_listener(node_listener)

            # Connecting to the device.
            print('Connecting to %s...' % (device.get_name()))
            if not device.connect():
                print('Connection failed.\n')
                continue

            while True:
                # Getting features.
                features = device.get_features()

                # Selecting a feature.
                while True:
                    choice = int(input('\nWould you like to shoot at this '\
                    + 'spot?\n1) Yes\n2) Change spots\n\nSelect a choice to '\
                    + 'connect to (\'0\' to quit): '))
                    if choice >= 1 and choice <= 2:
                        break
                if choice == 0:
                    # Disconnecting from the device.
                    print('\nDisconnecting from %s...' % (device.get_name()))
                    if not device.disconnect():
                        print('Disconnection failed.\n')
                        continue
                    device.remove_listener(node_listener)
                    # Resetting discovery.
                    manager.reset_discovery()
                    # Going back to the list of devices.
                    break
                if choice == 1:
                    #get feature indicies
                    feature_indices = []
                    for feature in features:
                        if feature.get_name() == 'Accelerometer':
                            acceleration_index = features.index(feature)
                            feature_indices.append(acceleration_index)
                        elif feature.get_name() == 'Gyroscope':
                            gyro_index = features.index(feature)
                            feature_indices.append(gyro_index)

                # Enabling notifications.
                feature_listener = MyFeatureListener()
                for index in feature_indices:
                    feature = features[index]
                    feature.add_listener(feature_listener)
                    device.enable_notifications(feature)

                # Handling audio case (both audio features have to be enabled).
                if isinstance(feature, FeatureAudioADPCM):
                    audio_sync_feature_listener = MyFeatureListener()
                    audio_sync_feature.add_listener(audio_sync_feature_listener)
                    device.enable_notifications(audio_sync_feature)
                elif isinstance(feature, FeatureAudioADPCMSync):
                    audio_feature_listener = MyFeatureListener()
                    audio_feature.add_listener(audio_feature_listener)
                    device.enable_notifications(audio_feature)

                # Getting notifications.
                get_feedback('rd')
                time.sleep(1)
                get_feedback('st')
                notifications = 0
                while notifications < NOTIFICATIONS:
                    start_time = time.time()
                    if device.wait_for_notifications(0.05):
                        notifications += 1
                    if time.time() - start_time > 0.001:
                        time.sleep(time.time()-start_time)

                #get result
                result = 6
                while not result in [0,1,2,3,4,5]:
                    result = int(input('\nPlease record the result.\n1) Make'\
                    + '\n2) Left\n3) Right\n4) Short\n5) Long\n6) Bad miss (do'\
                    + ' not record)\n'))-1
                if result == 0:
                    results = [1, 0, 0, 0, 0]
                elif result == 1:
                    results = [0, 1, 0, 0, 0]
                elif result == 2:
                    results = [0, 0, 1, 0, 0]
                elif result == 3:
                    results = [0, 0, 0, 1, 0]
                elif result == 4:
                    results = [0, 0, 0, 0, 1]
                else:
                    results = []

                if len(results):
                    #recording data
                    acceleration_df = pd.DataFrame([],columns=['time', 'ax', \
                    'ay', 'az'])
                    angular_speed_df = pd.DataFrame([],columns=['time', 'wx', \
                   'wy', 'wz'])
                    data_lines = data.split('\n')
                    for line in data_lines:
                    #Accelerometer(51692): ( X: 25 mg    Y: -45 mg    Z: 1010 mg )
                        if 'Accelerometer' in line:
                            t = line.split(')')[0].split('(')[1]
                            values = line.split(' ')
                            acceleration_df.loc[len(acceleration_df)] = [t, \
                            values[3],values[9], values[15]]
                        elif 'Gyroscope' in line:
                            t = line.split(')')[0].split('(')[1]
                            values = line.split(' ')
                            angular_speed_df.loc[len(angular_speed_df)] = [t, \
                            values[3], values[9], values[15]]

                    ts = acceleration_df['time'].to_numpy().astype(float)
                    axs = acceleration_df['ax'].to_numpy().astype(float)
                    ays = acceleration_df['ay'].to_numpy().astype(float)
                    azs = acceleration_df['az'].to_numpy().astype(float)
                    int_ax = simps(axs, ts)
                    int_ay = simps(ays, ts)
                    int_az = simps(azs, ts)
                    ax_max = max(axs)
                    ax_min = min(axs)
                    ay_max = max(ays)
                    ay_min = min(ays)
                    az_max = max(azs)
                    az_min = min(azs)
                    wxs = angular_speed_df['wx'].to_numpy().astype(float)
                    wys = angular_speed_df['wy'].to_numpy().astype(float)
                    wzs = angular_speed_df['wz'].to_numpy().astype(float)
                    wx_max = max(wxs)
                    wx_min = min(wxs)
                    wy_max = max(wys)
                    wy_min = min(wys)
                    wz_max = max(wzs)
                    wz_min = min(wzs)
                    #update suggestion data
                    if choice == 1 and len(motion_data)>1:
                        numerical_data = motion_data.drop(columns=['make', \
                        'left', 'right', 'short', 'long', 'suggestion'])
                        new_data = (\
                        numerical_data.loc[len(numerical_data-1)].to_numpy() -\
                        numerical_data.loc[len(numerical_data-2)].to_numpy())/\
                        numerical_data.loc[len(numerical_data-1)].to_numpy()
                        suggestion_data.loc[len(suggestion_data)] = \
                        list(new_data)+\
                        [motion_data.loc[len(suggestion_data) - 1]\
                        [len(motion_data.columns)-1]]
                    #get klusters
                    kluster_data = pd.DataFrame([])
                    if len(motion_data)>29:
                        kluster_data = motion_data.drop(columns=['suggestion'])
                        kluster_data.loc[len(kluster_data)] = [int_ax, ax_max,\
                        ax_min, int_ay, ay_max, ay_min, int_az, az_max, az_min,\
                        wx_max, wx_min, wy_max, wy_min, wz_max, wz_min] +\
                        results
                        kmeans = KMeans(n_clusters=30)
                        kmeans.fit(kluster_data)
                        y_kmeans = kmeans.predict(kluster_data)
                        kluster_data['y_kmeans'] = y_means
                        kluster_data = kluster_data[kluster_data['y_kmeans']==\
                        kluster_data['y_kmeans'][len(kluster_data['y_kmeans'])\
                        -1]]
                    #get suggestion
                    suggestion = 'ns'
                    if len(kluster_data) > 30:
                        logistic_data = kluster_data.drop(columns=['left', \
                        'right', 'short', 'long', 'y_kmeans'])
                        X = logistic_data.drop(['make'])
                        X = pd.concat([X,np.square(X)], axis=1)
                        X.columns = ['int_ax', 'ax_max', 'ax_min', 'int_ay',\
                        'ay_max', 'ay_min', 'int_az', 'az_max', 'az_min', \
                        'wx_max', 'wx_min', 'wy_max', 'wy_min', 'wz_max', \
                        'wz_min', 'int_ax2', 'ax_max2', 'ax_min2', 'int_ay2',\
                        'ay_max2', 'ay_min2', 'int_az2', 'az_max2', 'az_min2', \
                        'wx_max2', 'wx_min2', 'wy_max2', 'wy_min2', 'wz_max2', \
                        'wz_min2']
                        y = logistic_data['make']
                        clf = LogisticRegression().fit(X, y)
                        best_prob = 0
                        best_suggestion = 'ns'
                        for suggestion in suggestions:
                            one_suggestion = suggestion_data[\
                            suggestion_data['suggestion']==suggestion]
                            if len(one_suggestion):
                                coefficents = np.mean(suggestion_data).values
                                x = np.concatenate((coefficents, \
                                coefficients**2))*X.loc[len(X)-1].to_numpy()
                                if clf.predict(x) > best_prob:
                                    best_suggestion = suggestion
                    motion_data.loc[len(motion_data)] = [int_ax, ax_max,\
                    ax_min, int_ay, ay_max, ay_min, int_az, az_max, az_min,\
                    wx_max, wx_min, wy_max, wy_min, wz_max, wz_min] + results +\
                    [suggestion]
                    get_feedback(suggestion)
                motion_data.to_csv('motion_data.csv')
                suggestion_data.to_csv('suggestion_data.csv')
                data = ''


                # Disabling notifications.
                device.disable_notifications(feature)
                feature.remove_listener(feature_listener)

                # Handling audio case (both audio features have to be disabled).
                if isinstance(feature, FeatureAudioADPCM):
                    device.disable_notifications(audio_sync_feature)
                    audio_sync_feature.remove_listener(audio_sync_feature_listener)
                elif isinstance(feature, FeatureAudioADPCMSync):
                    device.disable_notifications(audio_feature)
                    audio_feature.remove_listener(audio_feature_listener)

    except KeyboardInterrupt:
        try:
            # Exiting.
            print('\nExiting...\n')
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == "__main__":

    main(sys.argv[1:])