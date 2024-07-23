// Function for scroll to be in the bottom by default
let messageArea = document.querySelector('#messageArea');
        messageArea.scrollTop = messageArea.scrollHeight - messageArea.clientHeight;


// Online checker
document.addEventListener('DOMContentLoaded', function () {
        const names = document.querySelectorAll('.name');
        const tooltip = document.getElementById('tooltip');

        names.forEach(function (name) {
            name.addEventListener('mouseover', function (event) {
                showTooltip(event);
            });

            name.addEventListener('mouseout', function () {
                hideTooltip();
            });
        });

        function showTooltip(event) {
            tooltip.style.display = 'block';
            moveTooltip(event); // Initial positioning
        }

        function hideTooltip() {
            tooltip.style.display = 'none';
        }

        function moveTooltip(event) {
            tooltip.style.left = event.pageX + 10 + 'px'; // Offset to avoid covering the cursor
            tooltip.style.top = event.pageY + 10 + 'px';
        }
    });

//Need to add communication with backend