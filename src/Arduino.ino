const int BUTTON_PIN = 2;    
const int POT_PIN = A0;    
const unsigned long BLINK_INTERVAL_DEFAULT = 500; 

unsigned long lastToggleTime = 0;
unsigned long blinkInterval = BLINK_INTERVAL_DEFAULT;
bool ledState = false;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP); 
  Serial.begin(9600);
}

void loop() {
  int btn = digitalRead(BUTTON_PIN);

  if (btn == LOW) { 
    int potValue = analogRead(POT_PIN);
    Serial.println(potValue);

    const int thresholdHalf = 1023 / 2; 
    if (potValue <= thresholdHalf) {
      digitalWrite(LED_BUILTIN, HIGH); 
    } else {
      digitalWrite(LED_BUILTIN, LOW); 
    }

    delay(500); 
  } else { 
    unsigned long now = millis();
    if (now - lastToggleTime >= blinkInterval) {
      lastToggleTime = now;
      ledState = !ledState;
      digitalWrite(LED_BUILTIN, ledState ? HIGH : LOW);
    }
  }
}