# Adaptive Basketball Coach

Utilizing motion sensing wearable technology, our application will train a 
model on a basketball players specific motion characteristics and provide 
feedback on a shot by shot basis.

## Hardware
The application was tested on the following configuration:
* SensorTile STM32L4  
* Raspberry Pi Zero W

## Installation requirements

The are several technologies being employed:
* Bluetooth for capturing motion data
* Speech recognition for accepting voice commands
* Text to speech for providing feedback

 
### Operating System Support
* Currently Linux is the only supported OS
    * Android and iOS are planned for a future release 
    
### SensorTile Installation
* Follow Tutorial 8 to get the SensorTile set up with the BLE codebase

    [Tutorial 8: Introduction to Motion Data Acquisition via Bluetooth Low Energy Communication](https://drive.google.com/open?id=1JVyw8-XIxEEnwGrHeDo7190aznLs3eTf)
    

### Raspberry Pi installation
1. Make sure python 3.7 is installed

    <code>sudo python3 --version</code>

2. Update the packages index

    <code>sudo apt update</code>


#### Installing the training application
1. Clone the repo into a local folder
    
    [github.com/gurleenbath/Treaty-Bio](https://github.com/gurleenbath/Treaty-Bio)

    
3.  Install all the dependencies (this will take some time) 

    <code>sudo pip3 install -r requirements.txt</code>

    
### Running the app
1. On the Raspberry Pi, open a terminal and cd to the cloned repo folder
2. Run the app:
    
    For the UI version, run this:
    
    <code>sudo python3 main_ui.py</code>
    
    For the command line version run this:
    
    <code>sudo python3 main.py</code>
    


## Demo files
Try speech recognition running:

    sudo python3 speech/guess_game.py

Try the text to speech by running:
   
    sudo python3 speech/test_speak.py "hello world" "nice to meet you"
    
    
