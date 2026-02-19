// Get the toggle button element
const toggle = document.getElementById('dark-mode-toggle');
const toggleIcon = document.querySelector('.toggle-icon');

// Check if user previously selected dark mode (saved in browser storage)
const currentTheme = localStorage.getItem('theme');

// If dark mode was previously enabled, apply it on page load
if (currentTheme === 'dark') {
  document.body.classList.add('dark-mode');
  toggleIcon.textContent = '☀️';
}

// Listen for clicks on the toggle button
toggle.addEventListener('click', () => {
  // Toggle the dark-mode class on the body element
  document.body.classList.toggle('dark-mode');
  
  // Check if dark mode is now active
  if (document.body.classList.contains('dark-mode')) {
    // Save preference to browser storage
    localStorage.setItem('theme', 'dark');
    // Change icon to sun (since we're in dark mode)
    toggleIcon.textContent = '☀️';
  } else {
    // Remove dark mode preference
    localStorage.setItem('theme', 'light');
    // Change icon back to moon
    toggleIcon.textContent = '🌙';
  }
});