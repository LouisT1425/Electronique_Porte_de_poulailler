#define LDR A0

const int pulsePin = 8;
const int directionPin = 9;
const int enablePin = 10;
const int switchPin = 4;
const int ledPin = 2;
const int buzzerPin = 3;

const int stepsPerRevolution = 770; // Nombre de pas idéal = 770


unsigned long previousMillis = 0; // Variable pour enregistrer le temps
const long interval = 500; // Interval pour 0.5 secondes
bool ledState = LOW; // Variable pour l'état de la LED

unsigned int value;

bool isDoorClosed() {
  int value = analogRead(LDR);
  return value < 330;
}

void calibrate() {
  unsigned long previousMillis = 0; // Variable pour enregistrer le temps
  const long interval = 500; // Interval pour 0.5 secondes
  bool ledState = LOW; // Variable pour l'état de la LED
  
  while (isDoorClosed()) {
    digitalWrite(directionPin, HIGH);

    for (int i = 0; i < 10; i++) {
      unsigned long currentMillis = millis();

      // Vérifier si suffisamment de temps s'est écoulé
      if (currentMillis - previousMillis >= interval) {
        // Sauvegarder le temps actuel
        previousMillis = currentMillis;
        
        // Changer l'état de la LED
        ledState = !ledState;
        
        // Mettre à jour l'état de la LED
        digitalWrite(ledPin, ledState);
      }

      // Votre code existant pour le mouvement
      digitalWrite(pulsePin, HIGH);
      delayMicroseconds(1000);
      digitalWrite(pulsePin, LOW);
      delayMicroseconds(1000);
    }
  }
  
  // Assurez-vous que la LED est éteinte à la fin de la calibration
  digitalWrite(ledPin, LOW);
}


void setup() {
  pinMode(LDR, INPUT);
  pinMode(pulsePin, OUTPUT);
  pinMode(directionPin, OUTPUT);
  pinMode(enablePin, OUTPUT);
  pinMode(switchPin, INPUT); // Configurer la broche de l'interrupteur comme une entrée
  pinMode(ledPin, OUTPUT);
  digitalWrite(enablePin, HIGH); // Activer le driver
  pinMode(buzzerPin, OUTPUT);
  
  Serial.begin(9600); // Commencer la communication série
  calibrate();
}

void loop() {
  int switchState = digitalRead(switchPin);
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (switchState == HIGH) {
      if (command == '1') {
        moveDoor(directionPin, HIGH);
      } else if (command == '2') {
        moveDoor(directionPin, LOW);
      } else if (command == '3') {
        calibrate();
      }
    }
  }
}

void moveDoor(int directionPin, int direction) {
  digitalWrite(directionPin, direction);

  for (int i = 0; i < stepsPerRevolution; i++) {
    unsigned long currentMillis = millis();

    if (currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;
      ledState = !ledState;
      digitalWrite(ledPin, ledState);
    }

    digitalWrite(pulsePin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(pulsePin, LOW);
    delayMicroseconds(1000);
    tone(buzzerPin, 1000);
  }
  digitalWrite(ledPin, LOW); // Éteindre la LED à la fin
  noTone(buzzerPin);
}
