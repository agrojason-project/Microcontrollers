/* we use the right serial port into myPort command 
a float number comes to this port so in this programm we take only the int part of the value(before ".").*/
import processing.serial.*;
Serial myPort;

int xPos;
int oldXpos = 0;
int oldxtint;
int dx = 10;

void setup(){
  size(500, 250);
  init_graph();
  xPos = dx;
  
  myPort = new Serial (this, "/dev/ttyUSB1", 9600);
}

void draw(){
  int ixt = 0,n=0;
  String inString = myPort.readStringUntil('\n');
  if(inString!=null){
    String[] num = splitTokens(inString, ".");
      n = Integer.parseInt(num[0]);
    //n = Integer.parseInt("10");
    ixt = (n*3);
    println(n);
    
    
    stroke(0,0,0);
    line(oldXpos,150-oldxtint,xPos,150-ixt);
    
    
    oldXpos = xPos;
    oldxtint = ixt;
    
    if(xPos >= width-dx){
      xPos = dx;
      oldXpos = 0;
      init_graph();
    }
    else {
      xPos+=10;
    }
  }
}

void init_graph(){
  background(255,255,255);
  line(0,150,500,150);
  line(10,250,10,0);
  textSize(16);
  fill(50);
  text("[Y]-thermokrasia",11,20);
  text("[X]-time",390,130);
}
