        function addUser() {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            if (username && password) {
                const users = JSON.parse(localStorage.getItem('users')) || [];
                users.push({ username, password });
                localStorage.setItem('users', JSON.stringify(users));
                renderUserList();
            } else {
                alert('Please enter username and password.');
            }
        }

        function renderUserList() {
            const users = JSON.parse(localStorage.getItem('users')) || [];
            const userList = document.getElementById('userList');
            userList.innerHTML = '';
            users.forEach((user, index) => {
                const li = document.createElement('li');
                li.textContent = `username: ${user.username}, password: ${user.password}`;
                const deleteBtn = document.createElement('button');
                deleteBtn.textContent = 'delete';
                deleteBtn.onclick = () => deleteUser(index);
                li.appendChild(deleteBtn);
                userList.appendChild(li);
            });
        }

        function deleteUser(index) {
            const users = JSON.parse(localStorage.getItem('users')) || [];
            users.splice(index, 1);
            localStorage.setItem('users', JSON.stringify(users));
            renderUserList();
        }

        window.onload = () => {
            renderUserList();
        };
