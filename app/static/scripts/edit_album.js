document.addEventListener("DOMContentLoaded", function () {
    let deleteSong = document.getElementsByClassName('musicDeleter')
    for (let i = 0; i < deleteSong.length; i++) {
        deleteSong[i].addEventListener("click", () => {
            $.get(`/delete-song-from-album?album_id=${deleteSong[i].getAttribute("data-album-id")}&user_name=${deleteSong[i].getAttribute("data-user-name")}&song_id=${deleteSong[i].getAttribute("data-song-id")}`, function (data) {

            });
        })
    }
})