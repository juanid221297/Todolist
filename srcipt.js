function addTodo() {
    const todoInput = document.getElementById('todo-input');
    const todoText = todoInput.value.trim();
  
    if (todoText) {
      const todoList = document.getElementById('todo-list');
      const listItem = document.createElement('li');
  
      listItem.innerHTML = `
        ${todoText}
        <button class="delete-btn" onclick="deleteTodo(this)">Delete</button>
      `;
  
      todoList.appendChild(listItem);
      todoInput.value = '';
    }
  }
  
  function deleteTodo(button) {
    const listItem = button.parentElement;
    listItem.remove();
  }
  