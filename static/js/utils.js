export function hideElement(elementId) {
  document.getElementById(elementId).classList.add('hidden');
}

export function showElement(elementId) {
  document.getElementById(elementId).classList.remove('hidden');
}

export function setButtonState(buttonId, disabled, text) {
  const button = document.getElementById(buttonId);
  button.disabled = disabled;
  if (text) button.textContent = text;
}