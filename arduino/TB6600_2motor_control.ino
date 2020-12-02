//Code by Pavan <shpmadushanka_at_gmail_dot_com>
//Control 2 stepper motors with serial commands

//These are the pin connections
#define M1_dirPin 2
#define M1_stepPin 3
#define M2_dirPin 4
#define M2_stepPin 5
#define M1_EN 6
#define M2_EN 7


#define FORWARD 1
#define BACKWARD 2

// Change the number of steps to take here
int x_steps = 100;
int y_steps = 100;

String rec;

void setup() {
  // Declare pins as output:
  pinMode(M1_stepPin, OUTPUT);
  pinMode(M1_dirPin, OUTPUT);
  pinMode(M2_stepPin, OUTPUT);
  pinMode(M2_dirPin, OUTPUT);
  pinMode(M1_EN,OUTPUT);
  pinMode(M2_EN,OUTPUT);

  Serial.begin(115200);
  //Set the motor directions
  //set_direction('X', FORWARD);
  //set_direction('Y', FORWARD);

  //Start with motors disabled
  disable_M1();
  disable_M2();
  
}
void loop() { 

  //Read serial input and extract the available data
  if (Serial.available() > 0) {
    rec = Serial.readStringUntil('\n');
    //Serial.print("Got value : ");
    //Serial.println(rec_val);
    if (rec.length() == 4) {
      set_direction('X', rec.substring(1, 2).toInt());
      set_direction('Y', rec.substring(3, 4).toInt());
      enable_M1();
      step_motor('X', x_steps);
      disable_M1();
      enable_M2();
      step_motor('Y', y_steps);
      Serial.println("d");
      disable_M2();
    }
    else if (rec.length() == 2){
      if(rec[0] == 'x') {
        set_direction('X', rec.substring(1, 2).toInt());
        //Run Motor x
        enable_M1();
        step_motor('X',x_steps);
        Serial.println("d");
        disable_M1();
      }
      else if (rec[0] == 'y') {
        set_direction('Y', rec.substring(1, 2).toInt());
        //Run Motor y
        enable_M2();
        step_motor('Y',y_steps);
        Serial.println("d");
        disable_M2();
      }
    }
  }
}

//This function repeats steps till defined number of steps
void step_motor(char motor, int n) {
  for(int i = 0; i < n; i++ ) {
    one_step(motor);
  }
}

//This steps the selected motor by one pulse
void one_step(char motor) {
  if(motor == 'X') {
    digitalWrite(M1_stepPin, HIGH);
    delayMicroseconds(500);
    digitalWrite(M1_stepPin, LOW);
    delayMicroseconds(500);
  }
  else if (motor == 'Y') {
    digitalWrite(M2_stepPin, HIGH);
    delayMicroseconds(500);
    digitalWrite(M2_stepPin, LOW);
    delayMicroseconds(500);
  }
  
}

//This is used to set the motor direction
void set_direction(char motor, int a) {

  if (motor == 'X') {
    if (a == FORWARD)
      digitalWrite(M1_dirPin, HIGH);
    else
      digitalWrite(M1_dirPin, LOW);
  }
  else if (motor == 'Y') {
    if (a == FORWARD)
      digitalWrite(M2_dirPin, HIGH);
    else
      digitalWrite(M2_dirPin, LOW);
  }
}


void enable_M1() {
  digitalWrite(M1_EN,LOW);  //Low is enabled.
}

void enable_M2() {
  digitalWrite(M2_EN,LOW);  //Low is enabled.
}

void disable_M1() {
  digitalWrite(M1_EN,HIGH);  //High is disabled.
}

void disable_M2() {
  digitalWrite(M2_EN,HIGH);  //High is disabled.
}
