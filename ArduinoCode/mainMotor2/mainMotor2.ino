/************************HEADER*****************************
  PROJECT: CU BOULDER PROJECT TOAD
  AUTHOR: JASON LE(jason.le7131@gmail.com)
  LAST MODIFIED: 5/9/2022
  DESCRIPTION: ROTATE SERVO AND DOWNLINK ENCODER DATA
  HARDWARE: USES CONTINUOUS SERVO AND OPTICAL ENCODER
 ***********************************************************/

//****Libaries****
#include <SPI.h>
#include <WiFiNINA.h>
#include <WiFiUdp.h>
#include <Servo.h>
#include "arduino_secrets.h" 

//****DEFINES****
#define servoPin 9 //<===CHANGE TO SERVO PIN

//****Global Variables****
//ENCODER SETUP
int A = 12;
int B = 11;
int I = 10;
float countTick = 0;
float countIndex = 0;
float precTick = 0;
float precIndex = 0;
float tick = 0;
float tickB = 0;
float index = 0;
float encoder = 0;
//WIFI SETUP(CHANGE WIFI SETTING UNDER arduino_secrets.h TAB)
int status = WL_IDLE_STATUS;
char ssid[] = SECRET_SSID;        // your network SSID (name)
char pass[] = SECRET_PASS;    // your network password (use for WPA, or use as key for WEP)
int keyIndex = 0;            // your network key index number (needed only for WEP)
unsigned int localPort = 2390;      // local port to listen on
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //buffer to hold incoming packet
char relyBuffer[UDP_TX_PACKET_MAX_SIZE] = "100.0";

//****Objects****
WiFiUDP Udp;
Servo myServo;

//****Setup Function****
void setup() {
  //INITIALIZE SERIAL PORT
  Serial.begin(115200);
  //ENCODER SETUP
  pinMode(A, INPUT);
  pinMode(B, INPUT);
  pinMode(I, INPUT);
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
  //SERVO AND INTERRUPT SETUP
  myServo.attach(servoPin);
  attachInterrupt(digitalPinToInterrupt(A),encoderFunc,CHANGE);
  attachInterrupt(digitalPinToInterrupt(B),encoderFunc,CHANGE);
}

//****Main Code ****
void loop() {
  // if there's data available, read a packet
  int packetSize = Udp.parsePacket();
  if (packetSize) {
      //read command from laptop and uplink encoder data
      Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
      String datReq(packetBuffer);
      //Serial.println(datReq);
      myServo.write(datReq.toFloat());
      memset(packetBuffer,0,UDP_TX_PACKET_MAX_SIZE);
      // send a reply, to the IP address and port that sent us the packet we received
      Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
      if(countTick > 2048){
        countTick = 0;
      }
      if(countTick < -2048){
        countTick = 0;
      }
      float encoderAngle = map(abs(countTick),0,2048,0,360);
      if(countTick < 0){
        encoderAngle *= -1;
      }   
      encoder = encoderAngle;
      String temp(encoder);
      temp.toCharArray(relyBuffer,UDP_TX_PACKET_MAX_SIZE);
      Udp.write(relyBuffer);
      Udp.endPacket();
  }
}


void encoderFunc(){
  //count ticks when they are triggered
  tick = digitalRead(A);
  tickB = digitalRead(B);
  index = digitalRead(I);
  if(tick != precTick)
  {
    if(tick != tickB)
    {
      countTick = countTick + tick;
      precTick = tick;
    }
    else
    {
      countTick = countTick - tick;
      precTick = tick;
    }
  }
  if(index != precIndex)
  {
    if(countTick > 0)
    {
      countIndex = countIndex + index;
      precIndex = index;
    }
    else
    {
      countIndex = countIndex - index;
      precIndex = index;
    }
    countTick = 0;
  }
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
