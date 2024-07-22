// Function for scroll to be in the bottom by default
var messageArea = document.querySelector('#messageArea');
        messageArea.scrollTop = messageArea.scrollHeight - messageArea.clientHeight;

// Online checker
// Function to run when the page has fully loaded
function setStatus() {

    // Select all status elements
    const statusElements = document.querySelectorAll('.status');

    // Iterate over each element and change its text content
    statusElements.forEach(function(element) {
        element.textContent = 'onfline';
    });
}

// Attach function to the window onload event
window.onload = setStatus;