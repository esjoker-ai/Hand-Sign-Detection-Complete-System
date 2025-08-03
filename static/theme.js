document.addEventListener('DOMContentLoaded', function () {
    const body = document.body;
    const toggle = document.getElementById('theme-toggle');
    
    // Load theme from localStorage
    if (localStorage.getItem('theme') === 'dark') {
        body.classList.replace('light-mode', 'dark-mode');
    }

    toggle.addEventListener('click', function () {
        if (body.classList.contains('light-mode')) {
            body.classList.replace('light-mode', 'dark-mode');
            localStorage.setItem('theme', 'dark');
        } else {
            body.classList.replace('dark-mode', 'light-mode');
            localStorage.setItem('theme', 'light');
        }
    });
});
