let round = 1;
let index = 0;
let responses = { 1: [], 2: [] };

const display = document.getElementById("symbol-display");
const colorPicker = document.getElementById("color-picker");
const button = document.getElementById("confirmar-btn");
const contador = document.getElementById("contador");

function showNextSymbol() {
  if (index < sequence.length) {
    const symbol = sequence[index];
    display.textContent = symbol;
    contador.textContent = `Letra ${index + 1} de ${sequence.length}`;
  } else {
    if (round === 1) {
      round = 2;
      index = 0;
      alert("Ronda 2: Volverás a elegir colores para las mismas letras.");
      showNextSymbol();
    } else {
      enviarResultados();
    }
  }
}

colorPicker.addEventListener("input", () => {
  display.style.color = colorPicker.value;
});

button.addEventListener("click", () => {
  const symbol = sequence[index];
  const color = hexToRgb(colorPicker.value);
  responses[round].push([symbol, color]);
  index++;
  display.style.color = "black";  // Reset color
  showNextSymbol();
});

function hexToRgb(hex) {
  const bigint = parseInt(hex.slice(1), 16);
  return [bigint >> 16, (bigint >> 8) & 255, bigint & 255];
}

function enviarResultados() {
  fetch("/guardar", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sequence: sequence,
      round1: responses[1],
      round2: responses[2]
    })
  })
  .then(res => res.json())
  .then(data => {
    alert(
      `¡Gracias!\nTu consistencia promedio fue: ${data.promedio_usuario}\nPromedio histórico: ${data.promedio_historico}`
    );
    location.reload();
  });
}

// Iniciar
showNextSymbol();
