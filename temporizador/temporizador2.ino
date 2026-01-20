// =========================
// PINOS
// =========================
const int releEsteira = 6;     // Relé da esteira
const int releLuzVerde = 7;   // Relé da lâmpada verde

void setup() {
  Serial.begin(9600);

  pinMode(releEsteira, OUTPUT);
  pinMode(releLuzVerde, OUTPUT);

  // Relés desligados (módulo ativo em LOW)
  digitalWrite(releEsteira, HIGH);
  digitalWrite(releLuzVerde, HIGH);

  Serial.println("✅ Arduino pronto (Temporizador + Luz Verde)");
}


void loop() {

  if (Serial.available()) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    // ===== ESTEIRA =====
    if (comando == "ESTEIRA_ON") {
      digitalWrite(releEsteira, LOW);
      Serial.println("▶️ ESTEIRA LIGADA");
    }

    else if (comando == "ESTEIRA_OFF") {
      digitalWrite(releEsteira, HIGH);
      Serial.println("⏸ ESTEIRA PARADA");
    }

    // ===== LUZ VERDE (PULSO) =====
    else if (comando == "LUZ_VERDE_PULSO") {
      digitalWrite(releLuzVerde, LOW);
      delay(500); // 0,5 segundo
      digitalWrite(releLuzVerde, HIGH);
      Serial.println("💡 LUZ VERDE PULSO 0,5s");
    }
  }
}
