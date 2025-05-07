const int ledPin = 5;  // LED pin
const int ldrPin = A0; // LDR pin

// Define reference voltages
const float V0 = 1.0;  // Example reference voltage with no sample (V0)
const float Vref = 2.5; // Example reference voltage with a white surface (Vref)
const float Vdark = 0.5; // Example dark reading voltage (Vdark)

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  
  // Measure Absorbance
  digitalWrite(ledPin, HIGH);  // Turn on LED
  delay(2000);
  float absorbanceValue = analogRead(ldrPin);  // Read LDR value



  float reflectanceValue = analogRead(ldrPin);  // Read LDR value



  float fluorescenceValue = analogRead(ldrPin);  // Read LDR value


  // Convert readings to voltages
  float voltageAbsorbance = (absorbanceValue * 5.0) / 1023.0;
  float voltageReflectance = (reflectanceValue * 5.0) / 1023.0;
  float voltageFluorescence = (fluorescenceValue * 5.0) / 1023.0;

  // Calculate Absorbance
  float absorbance = -log10(voltageAbsorbance / V0);

  // Calculate Reflectance
  float reflectance = voltageReflectance / Vref;

  // Calculate Fluorescence
  float fluorescence = voltageFluorescence - Vdark;

  // Output results
  //Serial.print("Absorbance: ");
  Serial.print(absorbance);
  Serial.print(", ");
  //Serial.print("  Reflectance: ");
  Serial.print(reflectance);
  Serial.print(", ");
  //Serial.print("  Fluorescence: ");
  Serial.println(fluorescence);
  Serial.print("  ");

  delay(1000);  // Wait before the next loop
}