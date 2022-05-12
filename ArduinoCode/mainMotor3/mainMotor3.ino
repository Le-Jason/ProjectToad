/************************HEADER*****************************
  PROJECT: CU BOULDER PROJECT TOAD
  AUTHOR: JASON LE(jason.le7131@gmail.com)
  LAST MODIFIED: 5/9/2022
  DESCRIPTION: ROTATE SERVO AND DOWNLINK ENCODER DATA
  HARDWARE: USES STEPPER MOTOR WITH ENCODER
  HELP:Curious Scientist(https://www.youtube.com/watch?v=CC4nBDcz6Xs)
 ***********************************************************/

//****Libaries****
#include <AccelStepper.h>
#include <WiFiNINA.h>
#include <WiFiUdp.h>

//****DEFINES****

//****Global Variables****
//WIFI SETUP(CHANGE WIFI SETTING UNDER arduino_secrets.h TAB)
int status = WL_IDLE_STATUS;
#include "arduino_secrets.h" 
///////please enter your sensitive data in the Secret tab/arduino_secrets.h
char ssid[] = SECRET_SSID;        // your network SSID (name)
char pass[] = SECRET_PASS;    // your network password (use for WPA, or use as key for WEP)
int keyIndex = 0;            // your network key index number (needed only for WEP)
unsigned int localPort = 2390;      // local port to listen on
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //buffer to hold incoming packet
char relyBuffer[UDP_TX_PACKET_MAX_SIZE] = "100.0";
//STEPPER MOTOR AND ENCODER SETUP
long receivedSteps = 0; //Number of steps
long receivedSpeed = 0; //Steps / second
long receivedAcceleration = 0; //Steps / second^2
char receivedCommand;
int directionMultiplier = 1; // = 1: positive direction, = -1: negative direction
bool newData, runallowed = false; // booleans for new data from serial, and runallowed flag
AccelStepper stepper(1, 6, 7);// direction Digital 7 (CCW), pulses Digital 6 (CLK)
float encoder = 0;

//****Objects****
WiFiUDP Udp;
 
//****Setup Function****
void setup()
{
  //INITIALIZE SERIAL PORT
  Serial.begin(115200);
  //WIFI SETUP
  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    // don't continue
    while (true);
  }
  String fv = WiFi.firmwareVersion();
  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
    Serial.println("Please upgrade the firmware");
  }
  // attempt to connect to WiFi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:
    status = WiFi.begin(ssid, pass);
    // wait 10 seconds for connection:
    delay(1000);
  }
  Serial.println("Connected to WiFi");
  printWifiStatus();
  Serial.println("\nStarting connection to server...");
  // if you get a connection, report back via serial:
  Udp.begin(localPort);
  
  //STEPPER MOTOR SETUP
  stepper.setMaxSpeed(16000); //<===CHANGE THIS FOR DESIRED SPEED(SPEED = Steps / second)
  stepper.setAcceleration(16000); //<===CHANGE THIS FOR DESIRED SPEED(ACCELERATION = Steps /(second)^2)
  receivedSpeed = 200; //<===CHANGE THIS FOR DESIRED SPEED
  stepper.disableOutputs(); //disable outputs
}

//****Main Code ****
void loop()
{
  // if there's data available, read a packet
  int packetSize = Udp.parsePacket();
  if(packetSize){
    //read command from laptop and uplink encoder data
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    String datReq(packetBuffer);
    //Serial.println(datReq);
    receivedSteps = datReq.toFloat();
    RotateRelative();
    memset(packetBuffer,0,UDP_TX_PACKET_MAX_SIZE);
    // send a reply, to the IP address and port that sent us the packet we received
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    encoder = stepper.currentPosition();
    if(encoder > 9600){
      int divEncoderPos = (int)stepper.currentPosition()/9600;
      encoder = encoder - (divEncoderPos*9600);
    }
    if(encoder < -9600){
      int divEncoderNeg = (int)abs(stepper.currentPosition())/9600;
      encoder = encoder + (divEncoderNeg*9600);
    }
    float sendencoder = map(abs(encoder),0,9600,0,360);
    if(encoder < 0){
      sendencoder *= -1;
    }
    String temp(sendencoder);
    temp.toCharArray(relyBuffer,UDP_TX_PACKET_MAX_SIZE);
    Udp.write(relyBuffer);
    Udp.endPacket();
  }else{
    RunTheMotor();
  }
}
 
 
void RunTheMotor() //function for the motor
{
  if (runallowed == true)
  {
    stepper.enableOutputs(); //enable pins
    stepper.run(); //step the motor (this will step the motor by 1 step at each loop)  
  }
}

void RotateRelative()
{
  //We move X steps from the current position of the stepper motor in a given direction.
  //The direction is determined by the multiplier (+1 or -1)
  runallowed = true; //allow running - this allows entering the RunTheMotor() function.
  stepper.setMaxSpeed(receivedSpeed); //set speed
  stepper.move(directionMultiplier * receivedSteps); //set relative distance and direction
//    stepper.setSpeed(receivedSteps);
  RunTheMotor();
}

void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
 }
