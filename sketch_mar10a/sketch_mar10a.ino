#include <Wire.h>
#include <Adafruit_VL53L0X.h>

#define XSHUT_1 2  // XSHUT pin for Sensor 1
#define XSHUT_2 3  // XSHUT pin for Sensor 2

Adafruit_VL53L0X sensor1 = Adafruit_VL53L0X();
Adafruit_VL53L0X sensor2 = Adafruit_VL53L0X();
int difference;

void setup() {
   Serial.begin(115200);
    Wire.begin();

    pinMode(XSHUT_1, OUTPUT);
    pinMode(XSHUT_2, OUTPUT);
    
    // Turn OFF both sensors
    digitalWrite(XSHUT_1, LOW);
    digitalWrite(XSHUT_2, LOW);
    delay(10);

    // Enable Sensor 1, keep Sensor 2 off
    digitalWrite(XSHUT_1, HIGH);
    delay(10);

    // Initialize Sensor 1 and change its I2C address
    if (!sensor1.begin(0x30)) {  // Assign new I2C address to Sensor 1
        Serial.println(F("Failed to initialize Sensor 1!"));
        while (1);
    }
    
    Serial.println(F("Sensor 1 initialized at 0x30."));

    // Enable Sensor 2
    digitalWrite(XSHUT_2, HIGH);
    delay(10);

    // Initialize Sensor 2 and keep default I2C address (0x29)
    if (!sensor2.begin(0x31)) {  // Assign new I2C address to Sensor 2
        Serial.println(F("Failed to initialize Sensor 2!"));
        while (1);
    }
    
    Serial.println(F("Sensor 2 initialized at 0x31."));

    //zapnou zelenou LED
}

void loop() {
    VL53L0X_RangingMeasurementData_t measure1, measure2;

    // Read Sensor 1
    sensor1.rangingTest(&measure1, false);
    Serial.print(F("Sensor 1 Distance: "));
    if (measure1.RangeStatus != 4) {
        Serial.print(measure1.RangeMilliMeter);
        Serial.println(F(" mm"));
    } else {
        Serial.println(F("Out of range!"));
    }

    // Read Sensor 2
    sensor2.rangingTest(&measure2, false);
    Serial.print(F("Sensor 2 Distance: "));
    if (measure2.RangeStatus != 4) {
        Serial.print(measure2.RangeMilliMeter);
        Serial.println(F(" mm"));
    } else {
        Serial.println(F("Out of range!"));
    }

    difference = int(measure1.RangeMilliMeter) - int(measure2.RangeMilliMeter);

    Serial.print(F("difference: "));
    Serial.println(difference);

    delay(500);
}