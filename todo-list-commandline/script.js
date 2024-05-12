function completeTask(taskId) {
    // Send an AJAX request to mark the task as completed
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/complete/" + taskId, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // If the task is successfully marked as completed, move it to the "Completed" section
            var todoItem = document.querySelector('li input[value="' + taskId + '"]').parentNode;
            var completedList = document.getElementById("completed-list");
            completedList.appendChild(todoItem);
        }
    };
    xhr.send();
}
