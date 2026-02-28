// Theme Toggle
document.addEventListener('DOMContentLoaded', function () {
  const themeToggle = document.getElementById('theme-toggle');
  const html = document.documentElement;

  // Load saved theme or default to light
  const savedTheme = localStorage.getItem('theme') || 'light';
  html.setAttribute('data-theme', savedTheme);
  themeToggle.checked = savedTheme === 'dark';

  // Toggle theme
  themeToggle.addEventListener('change', function () {
    const newTheme = this.checked ? 'dark' : 'light';
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
  });
});

// Toast Notification Function
function showToast(message, type = 'info') {
  const toastContainer = document.getElementById('toast-container');

  const alertTypes = {
    success: 'alert-success',
    error: 'alert-error',
    warning: 'alert-warning',
    info: 'alert-info',
  };

  const toast = document.createElement('div');
  toast.className = `alert ${alertTypes[type]} shadow-lg`;
  toast.innerHTML = `
        <div>
            <span>${message}</span>
        </div>
    `;

  toastContainer.appendChild(toast);

  // Auto remove after 3 seconds
  setTimeout(() => {
    toast.classList.add('opacity-0');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
