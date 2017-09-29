import cv2
import sys
import time
import smbus

#custom
import i2c_lcd
import led_piezzo

i2c_lcd.lcd_init()
led_piezzo.toggleLed(4,1)
led_piezzo.toggleLed(17,1)
print "Configuring system:"
i2c_lcd.lcd_string("Konfiguriram",i2c_lcd.LCD_LINE_1)
i2c_lcd.lcd_string("sustav:",i2c_lcd.LCD_LINE_2)

cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

recognizer = cv2.createLBPHFaceRecognizer()
recognizer.load('recognizer_withme.xml')

video_capture = cv2.VideoCapture(0)
video_capture.set(3,320)
video_capture.set(4,240)
time.sleep(1)
video_capture.set(15, -8.0)

led_piezzo.toggleLed(4,0)
led_piezzo.toggleLed(17,0)

print "Detection started:"
i2c_lcd.lcd_string("Pokrenuta",i2c_lcd.LCD_LINE_1)
i2c_lcd.lcd_string("detekcija:",i2c_lcd.LCD_LINE_2)

i = 0
face_i = 0
last = 0
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_i = 0
    if i  % 10 == 0:
        i2c_lcd.lcd_string("Pokrenuta",i2c_lcd.LCD_LINE_1)
        i2c_lcd.lcd_string("detekcija:",i2c_lcd.LCD_LINE_2)
    
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        frameText =  {}

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        if frameText.has_key(face_i):
            cv2.putText(frame,frameText[face_i], (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
            #print frameText[face_i]
        if i % 10 == 0:
            nbr_predicted, conf = recognizer.predict(gray[y: y + h, x: x + w])
            print str(nbr_predicted) + " - " + str(conf)
            if conf <= 265:
                if nbr_predicted == 16:
                    nbr_predicted = 'Emanuel'
                led_piezzo.toggleLed(17,1)
                
                frameText[face_i] = str(nbr_predicted) + " - " + str(int(conf))
                print frameText[face_i]
                cv2.putText(frame,frameText[face_i], (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
                i2c_lcd.lcd_string("Raspoznata osoba:",i2c_lcd.LCD_LINE_1)
                i2c_lcd.lcd_string(str(nbr_predicted) + " - " + str(int(conf)),i2c_lcd.LCD_LINE_2)
                led_piezzo.buzzOn()
                last = i
            else:
                led_piezzo.toggleLed(4,1)
                i2c_lcd.lcd_string("Detektirana",i2c_lcd.LCD_LINE_1)
                i2c_lcd.lcd_string("osoba:",i2c_lcd.LCD_LINE_2)
                last = i
        else:
            led_piezzo.buzzOff()
            
        face_i = face_i + 1

    # Display the resulting frame
    cv2.imshow('Video', frame)
    led_piezzo.toggleLed(17,0)
    led_piezzo.toggleLed(4,0)
    
    i = i + 1
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
led_piezzo.cleanup()
i2c_lcd.lcd_byte(0x01, i2c_lcd.LCD_CMD)



