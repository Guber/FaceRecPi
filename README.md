
# An example of using OpenCV on RaspberryPi3
This project describes the application of the OpenCV library on RaspberyPi3 with a web camera and other periphery. I have built it for a seminar during my master thesis. If some images are in croatian mea culpa, sicne i copied it directly from my seminar. I will fix it! :)

I used RaspberryPi3 with a Rasbian Linux operating system installed on the SD card.

# System hardware arhitecture
 ![alt text](https://github.com/Guber/FaceRecPi/readmeimg/pigpio.jpg "RBP3 GPIO")
*RaspberryPi3 contains a GPIO 40-pin multi-multiplexed interface.*

To connect the periphery of pins 4 and 6 we used to share power from the RBP3 regulator. Pin 3 and 5 were used in I2C mode as SCL and SDA pin for connecting to the I2C controller of the LCD assembly. I2C is a two-way serial multi-master protocol suitable for transmitting low-distance signals, which is perfect for our purpose. Of course, the LCD controller must be connected to a common ground as well as the RBP3 circuit, and for the purpose of supplying it, it is possible to use 5V output from pin 4.

Pins 7 and 17 are connected to LED diodes (as output pins) which are protected by a short circuit via a 4.7kOhm resistor. Piezzo speaker is connected to pin 12 through which the internal PWM controller changes the output signal frequency to it. Piezzo loudspeaker, which otherwise produces different sound frequencies. Its purpose is to output an audible signal at an event like an actuator, similar to how the LEDs work with the same visual signal.
 
  ![alt text](https://github.com/Guber/FaceRecPi/readmeimg/fritzing.jpg "Fritzing schematic")
 *Schematic diagram drawn in the Fritzing hobby CAD software*
 
# Application Architecture
The application that drives our system is written in Python and is layered into multiple python scripts that perform certain actions in the system.

  ![alt text](https://github.com/Guber/FaceRecPi/readmeimg/component.jpg "UML component diagram")
 *UML Diagram of Software Components of an Existing System*

Python script *face_recognizer_learn.py* serves to recognize facial recognition over the image dataset, its result is a file *facerecognizer.xml* that we will use in facial recognition.
 The *haarcascade_frontalface_default.xml* file we downloaded from the Internet (open source) will be used in the face detection phase.
 
The Python *i2c_lcd.py* script is used to control prints on the lcd interface via the i2c interface.
The *led_piezzo.py* script is used to control our signal actuators: LED diodes and piezo speakers.
At the end of the script *webcam_facedetectrec.py* takes the frames with the webcams and performs detection and recognition of faces using all of the aforementioned scripts and files.


# Using a The System

On the GUI itself, the Raspbian system prinst in the console a description of the status of the system and the known person and the level of reliability that the person is recognizing (less is better).

The GUI also has a screen with the current frame of the camera where the detected face is detected, and in case of a recognized person (reliability level less than a certain threshold) and the printing of the recognized person as well as the level of confidence that we have been assigned to a person.

 ![alt text](https://github.com/Guber/FaceRecPi/readmeimg/gui.jpg "GUI")
*Displaying an application interface GUI*

Generally our system can be found in 4 states (except the initial and the final):
• Configuration - The system configures the camera and the peripheral circuit board
• Detection - The system is fully started and detects the appearance of the human face on the camera
• Person detected - human face detected
• Person detected and recognized - human face is detected and recognized

The states are also shown in the accompanying diagram of the condition:
 
  ![alt text](https://github.com/Guber/FaceRecPi/readmeimg/state.jpg "UML state diagram")
 *UML System State Diagram*

The following photographs show the state of the system on the peripheral hardware of the boot system:

![alt text](https://github.com/Guber/FaceRecPi/readmeimg/state1.jpg "System state 1")
*Configuration in progress* 

 ![alt text](https://github.com/Guber/FaceRecPi/readmeimg/state2.jpg "System state 2")
*Detection*

 ![alt text](https://github.com/Guber/FaceRecPi/readmeimg/state3.jpg "System state 3")
*Person detected *

![alt text](https://github.com/Guber/FaceRecPi/readmeimg/state4.jpg "System state 4")
*Person detected and identified*