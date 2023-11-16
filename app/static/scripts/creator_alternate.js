document.addEventListener("DOMContentLoaded", function () {
    let songHead = document.getElementById("songs")
    let albumHead = document.getElementById("albums")
    albumHead.addEventListener("click", () => {
        alert("yo")
        songHead.style.color = "black"
        songHead.style.backgroundColor = "white"
        albumHead.style.color = "white"
        albumHead.style.backgroundColor = "transparent"
        albumHead.style.borderBottom = "0.2rem solid white"
        var creator_id = albumHead.getAttribute("data-creator-id")
        var user_name = albumHead.getAttribute("data-user-name")
        window.location.href = `http://127.0.0.1:5000/creator/${user_name}?creator_id=${creator_id}&window=album`
    })
    songHead.addEventListener("click", () => {
        songHead.style.color = "black"
        songHead.style.backgroundColor = "white"
        albumHead.style.color = "white"
        albumHead.style.backgroundColor = "transparent"
        albumHead.style.borderBottom = "0.2rem solid white"
        var creator_id = songHead.getAttribute("data-creator-id")
        var user_name = songHead.getAttribute("data-user-name")
        window.location.href = `http://127.0.0.1:5000/creator/${user_name}?creator_id=${creator_id}&window=songs`
    })


    // Your JavaScript code here
    let songPlayer = document.getElementsByClassName("songPlayer")
    for (let i = 0; i < songPlayer.length; i++) {
        songPlayer[i].addEventListener("click", () => {
            window.location.href = `/user/${songPlayer[i].getAttribute("data-user-name")}/lyrics?song_id=${songPlayer[i].getAttribute("data-song-id")}&current_time=0&paused=false`
        })
    }
    let albumPlayers = document.getElementsByClassName("albumPlayer");
    for (let i = 0; i < albumPlayers.length; i++) {
        let currentAlbumPlayer = albumPlayers[i];

        currentAlbumPlayer.addEventListener("click", () => {
            window.location.href = `/user/${currentAlbumPlayer.getAttribute("data-user-name")}/album?album_id=${currentAlbumPlayer.getAttribute("data-album-id")}`;
        });
    }
    let albumEditer = document.getElementsByClassName("albumEditer")
    for (let i = 0; i < albumEditer.length; i++) {
        albumEditer[i].addEventListener("click", () => {
            window.location.href = `/creator/${albumEditer[i].getAttribute("data-user-name")}/edit-album?album_id=${albumEditer[i].getAttribute("data-album-id")}`
        })
    }
    let albumDeleter = document.getElementsByClassName("albumDeleter")
    for (let i = 0; i < albumDeleter.length; i++) {
        albumDeleter[i].addEventListener("click", () => {
            window.location.href = `/creator/${albumDeleter[i].getAttribute("data-user-name")}/delete-album?album_id=${albumDeleter[i].getAttribute("data-album-id")}`
        })
    }
});