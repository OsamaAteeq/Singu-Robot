#include <Servo.h> // servo library

#define ROTARY_ANGLE_SENSOR A0
#define SPEAKER_PIN 6
#define ADC_REF 5 //reference voltage of ADC is 5v.If the Vcc switch on the seeeduino
                    //board switches to 3V3, the ADC_REF should be 3.3
#define GROVE_VCC 5 //VCC of the grove interface is normally 5v
#define FULL_ANGLE 300 //full value of the rotary angle is 300 degrees
#define MAX_ARM_ANGLE 120
#define HEAD_STATIONARY 1550

Servo myservo; // create servo object to control a servo
Servo myservo2;
Servo myservoHead;

const int arm1Pin = 5;
const int arm2Pin = 8;
const int headPin = 9;


const unsigned long servoInterval = 15;

int pos = 0;    // variable to store the servo position
int pos2 = 0;   // variable to store the previous servo position

//MUSIC
int melody[] = {
  262, 262, 392, 392, 440, 440, 392,
  349, 349, 330, 330, 294, 294, 262
};
int durations[] = {
  4, 4, 4, 4, 4, 4, 2,
  4, 4, 4, 4, 4, 4, 2
};

unsigned long noteStartTime = 0;
int currentNote = 0;
bool playingNote = false;
int freq = 0;
int maxFrequency;
int minFrequency;
bool playingMelody = true;

void setup()
{
    Serial.begin(9600);
    pinMode(ROTARY_ANGLE_SENSOR, INPUT);
    pinMode(SPEAKER_PIN, OUTPUT);
    myservo.attach(arm1Pin);
    myservo2.attach(arm2Pin);
    myservoHead.attach(headPin);
    setMinMaxFrequency();
}

void loop()
{
    //PLAY SONG
    playMelodyNonBlocking();

    //ARMS   
    float voltage;
    if(!playingMelody)
    {
    int sensor_value = analogRead(ROTARY_ANGLE_SENSOR);
    voltage = (float)sensor_value*ADC_REF/1023;
    float degrees = (voltage*FULL_ANGLE)/GROVE_VCC;
    //Serial.println(degrees);
    pos = map(degrees, 0, FULL_ANGLE, 0, MAX_ARM_ANGLE);
    }
    else
    {
      pos = map(freq, minFrequency+20, maxFrequency, 0, MAX_ARM_ANGLE);
    }
    if(pos-pos2 > 0.5 || pos2-pos > 0.5)
    {
      Serial.println(pos);
      myservo.write(pos);
      myservo2.write(MAX_ARM_ANGLE-pos);
      pos2 = pos;
    }
    //HEAD
    myservoHead.writeMicroseconds(HEAD_STATIONARY);

    //DELAY
    delay(servoInterval);
}

void playMelodyNonBlocking() {
  if(!playingMelody) return;

  if (currentNote >= sizeof(melody) / sizeof(int))
  {
    playingMelody = false;
    return;
  }

  unsigned long now = millis();
  int duration = 1000 / durations[currentNote];
  if (!playingNote) {
    freq = melody[currentNote];
    tone(SPEAKER_PIN, freq);
    noteStartTime = now;
    playingNote = true;
  } else if (now - noteStartTime >= duration) {
    noTone(SPEAKER_PIN);
    playingNote = false;
    currentNote++;
    delay(50); // slight pause between notes
  }
}

void setMinMaxFrequency() {
  int maxFreq = melody[0];
  int minFreq = melody[0];
  for (int i = 1; i < sizeof(melody) / sizeof(int); i++) {
    if (melody[i] > maxFreq) maxFreq = melody[i];
    if (melody[i] < minFreq) minFreq = melody[i];
  }
  maxFrequency = maxFreq;
  minFrequency = minFreq;
}
