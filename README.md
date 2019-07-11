# **Flag Waver using 4 orthogonal wind sensors**

This project is an implementation of https://krikienoid.github.io/flagwaver/ using Python

Flask web server is used with ThreeJS to capture the data coming from arduino analog pins, representing the wind sensors data , and pushing
it to the ThreeJS graphical interface (3D Environment) with the help of Flask. 

Also, WebSocket-IO was implemented to change the user interface based on the serial data available

This code can be uploaded to raspberry pi via SSH or can be used on Windows/Linux PCs

![alt text](https://github.com/mrvolta/flagwaver/blob/master/flagwaver/flagnotify.png)

# **Installation**

You have to install python 3 on your raspberry pi
```
sudo apt-get update -y
sudo apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y
```
If one of the packages cannot be found, try a newer version number (e.g. libdb5.4-dev instead of libdb5.3-dev).

Download and install the latest Python 3.7 source. Select the most recent release of Python (as of writing, 3.7.2) from the official site. Adjust the file names accordingly to match your version.
```
 wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz
 tar xf Python-3.7.2.tar.xz
 cd Python-3.7.2
 ./configure
 make -j 4
 sudo make altinstall
```

If that didn't work, please try this one instead
```
sudo apt-get install python3-dev libffi-dev libssl-dev -y.
wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tar.xz.
tar xJf Python-3.6.3.tar.xz.
cd Python-3.6.3.
./ configure.
make.
sudo make install.
sudo pip3 install --upgrade pip.
```
-----------------------

After that , you can install our package using the following
```
pip3 install git+https://github.com/mrvolta/flagwaver
```

# **Usage**

You will find examples in the "examples" folder as follows:

Simple.py - Implementing the basic usage via simple python function called "run()" which will read the serial data coming from the arduino
via "arduino" class and conduct some calculations , producing the wind speed and direction to be transferred to ThreeJS Flag animation.

Detailed.py - Implementing the same previous concept, except you can actually view some deeper python code

Simulated.py - Here you can run the code without the need for arduino serial communication to be active , because it's simulating the data

![alt text](https://github.com/mrvolta/flagwaver/blob/master/flagwaver/potschematic.png)

# **Arduino Code**

```
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(115200);
  while (!Serial) {
  ; // wait for serial port to connect. Needed for native USB port only
}
}
int readings = 0;
int speeds[4] = {0};
int incomingByte = 0;

// the loop routine runs over and over again forever:
void loop() {
  if (Serial.available() > 0) {

  //incomingByte = Serial.read(); // read the incoming byte:
  Serial.read();
  Serial.println("I'm Here :)");

  //Serial.println(incomingByte);
  
  }
  // read the input on analog pin 0:
  speeds[0] += map(analogRead(A0), 0, 1223, 0, 255); //front
  speeds[1] += map(analogRead(A1), 0, 1223, 0, 255);//analogRead(A1); //back
  speeds[2] += map(analogRead(A2), 0, 1223, 0, 255);//analogRead(A2); //left
  speeds[3] += map(analogRead(A3), 0, 1223, 0, 255);//analogRead(A3); //right

  if (readings > 10)
  {
    speeds[0] = speeds[0] / 10;
    speeds[1] = speeds[1] / 10;
    speeds[2] = speeds[2] / 10;
    speeds[3] = speeds[3] / 10;

    switch (getIndexOfMaximumValue(speeds,4)) {
      case 0:
        // statements
        Serial.print("F");
        break;
      case 1:
        // statements
        Serial.print("B");
        break;
      case 2:
        // statements
        Serial.print("L");
        break;
      case 3:
        // statements
        Serial.print("R");
        break;
      default:
        // statements
        break;
    }
  // print out the value you read:
  Serial.print("[");
  Serial.print(speeds[0]);
  Serial.print(",");
    Serial.print(speeds[1]);
  Serial.print(",");
    Serial.print(speeds[2]);
  Serial.print(",");
    Serial.print(speeds[3]);
  Serial.println("]");
  delay(100);        // delay in between reads for stability
      speeds[0] = 0;
      speeds[1] = 0;
      speeds[2] = 0;
      speeds[3] = 0;
      readings = 0;
  }else
  {
  readings++;
  }
  delay(100);
}

int getIndexOfMaximumValue(int* array, int size){
 int maxIndex = 0;
 int max = array[maxIndex];
 for (int i=1; i<size; i++){
   if (max<array[i]){
     max = array[i];
     maxIndex = i;
   }
 }
 return maxIndex;
}
```
