#include <Stepper.h>
#include <Adafruit_VL53L0X.h>

Adafruit_VL53L0X lox = Adafruit_VL53L0X();
const int stepsPerRevolution = 200;
Stepper myStepper(stepsPerRevolution, 2, 3);

void setup() {
Serial.begin(115200);

   while (!Serial)
   {
      delay(1);
  }
  /*
  if (!lox.begin())
  {
    Serial.println(F("Failed to boot VL53L0X"));
    while(1);
  }
  Serial.println(F("VL53L0X API Simple Ranging example\n\n"));
*/

  // set the speed at 60 rpm:
  myStepper.setSpeed(60);


}

void loop() {


  // step one revolution  in one direction:
  Serial.println("clockwise");
  myStepper.step(stepsPerRevolution);
  delay(500);

  // step one revolution in the other direction:
  Serial.println("counterclockwise");
  myStepper.step(-stepsPerRevolution);
  delay(500);









  /*
   VL53L0X_RangingMeasurementData_t measure;

   Serial.print("Reading a measurement...");
   lox.rangingTest(&measure, false); // pro výpis debug informací předáme true

   if (measure.RangeStatus != 4)  // úspěch
   {
      Serial.print("Distance (mm): ");
      Serial.println(measure.RangeMilliMeter);
   }
   else
   {
      Serial.println(" out of range ");
   }

   delay(100);
*/

}
