function update_notification(token) {
    $.ajax({
        method: "POST",
        url: "/api/notification/",
        data: {"csrfmiddlewaretoken": token, "action": "get"},
        success: function (data) {
            if (data.unwatched_count > 0) {
                $('.nav-link-notifications').append(`<span class="nav-link-notification-number">${data.unwatched_count}</span>`)
            }
            for (let i = 0; i < data.objects.length; i++) {
                if (data.objects[i].notification_status === "unwatched") {
                    $('.list-group').append(
                    `<a href="#" class="list-group-item list-group-item-action unread">` + 
                        `<p class="mb-1"><strong class="text-danger">${data.objects[i].notification_header}</strong><br />${data.objects[i].notification_text}</p>` +
                        `<small>${humanized_time_span(data.objects[i].notification_time)}</small>` +
                    `</a>`)
                } else {
                    $('.list-group').append(
                        `<a href="#" class="list-group-item list-group-item-action">` +
                        `<p class="mb-1"><strong class="text-danger">${data.objects[i].notification_header}</strong><br />${data.objects[i].notification_text}</p>` +
                        `<small>${humanized_time_span(data.objects[i].notification_time)}</small>` +
                    `</a>`)
                }
            }
            ;
        }
    })
}
function read_all(token) {
    $.ajax({
        method: "POST",
        url: "/api/notification/",
        data: {"csrfmiddlewaretoken": token, "action": "read_all"},
        success: function (data) {
            $('.unread').removeClass("unread")
            $('.nav-link-notification-number').remove()
            console.log(data)
        }
    })
}

const reformatNumber = (n, t = ' ') => {
    let a = n.toString().split('').reverse()
    a.forEach(function (item, index, array) {
        if((index + 1) % 3 === 0) array[index] = t+item;
    });
    return a.reverse().join('');
};