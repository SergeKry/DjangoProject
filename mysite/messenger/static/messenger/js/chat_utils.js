// Function for scroll to be in the bottom by default
var messageArea = document.querySelector('#messageArea');
        messageArea.scrollTop = messageArea.scrollHeight - messageArea.clientHeight;


// Tooltip
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
            tooltip.style.left = event.pageX + 10 + 'px'; // Offset to avoid covering the cursor
            tooltip.style.top = event.pageY + 10 + 'px';
        }

        function hideTooltip() {
            tooltip.style.display = 'none';
        }
    });

// Backend connection for online checker to be shown in a tooltip
$('.name').mouseover(function(){
    let author_id, user_data;
    author_id = $(this).attr('data-authorid');
    user_data = {author_id: author_id};
    $.ajax(
        {
            url: "/online_status",
            data: user_data,
            dataType: 'json',
            success: function(data){
                if (data.online_status) {
                    $('#tooltip-text').text('online')
                    $('#tooltip-text').removeClass('text-muted')
                    $('#tooltip-text').addClass('text-success')
                } else {
                    $('#tooltip-text').text('offline')
                    $('#tooltip-text').removeClass('text-success')
                    $('#tooltip-text').addClass('text-muted')
                }
            }
        }
    )
})