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

export function showToast(message, type = 'info'){
  const toastContainer = document.getElementById('toast-container');
  const alertTypes = {
    'success': 'alert-success',
    'error': 'alert-error',
    'warning': 'alert-warning',
    'info': 'alert-info'
  }

  const toast = document.createElement('div');
  toast.className = `alert ${alertTypes[type]} shadow-lg`
  toast.innerHTML = `
    <div>
      <span>${message}</span>
    </div>
  `;

  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('opacity-0');
    setTimeout(() => toast.remove(), 500);
  }, 5000)
}

export function showError(message){
  const errorModal = document.getElementById("error-modal")
  const errorMessage = document.getElementById('error-message');
  errorMessage.textContent = message;
  showElement('error-alert');
  errorModal.showModal()
  setTimeout(() => {
    hideElement('error-alert');
    errorModal.close();
  } 
  , 10000);
}