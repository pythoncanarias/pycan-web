function initTheme() {
   console.log('initTheme starts');
   const theme = localStorage.getItem('theme');
   console.log('theme:', theme);
   if ((theme === 'light') || (theme === 'dark')) {
      const root = document.documentElement;
      root.setAttribute("data-theme", theme);
      }
   console.log('initTheme ends');
   }


function switchTheme() {
   console.log('switchTheme starts');
   const root = document.documentElement;
   const theme = root.dataset.theme;
   console.log('theme:', theme);
   if (theme === 'light') {
      localStorage.setItem('theme', 'dark');
      root.setAttribute('data-theme', 'dark');
   } else if (theme === 'dark') {
      localStorage.setItem('theme', 'light');
      root.setAttribute('data-theme', 'light');
   }
   console.log('switchTheme ends');
   }

document.addEventListener('DOMContentLoaded', initTheme);
document.getElementById('switch-theme-button').addEventListener(
    'click',
    switchTheme,
    );
