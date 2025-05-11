       function authenticate() {
           const username = prompt('Please enter user name:');
           const password = prompt('Please enter password:');
           const res = await fetch('data/users.json');
           const users = res.ok ? await res.json() : [];
           const user = users.find(u => u.username === username && u.password === password);

           if (user) {
               alert('Authentication succeeded!');
               window.location.href = 'https://uchida16104.github.io/HealthAnalysis/';
           } else {
               alert('Authentication failed.');
               window.location.href = 'http://hirotoshiuchida.glitch.me/';
           }
       }

       function checkAuthStatus() {
           const isAuthenticated = localStorage.getItem('isAuthenticated');
           if (!isAuthenticated) {
               authenticate();
           }
       }

      function markAuthenticated() {
           localStorage.setItem('isAuthenticated', 'true');
       }

       window.onload = () => {
           checkAuthStatus();
       };
