document.addEventListener("DOMContentLoaded", function () {
    let signin = document.getElementById("signin")
    let signup = document.getElementById("signup")

    signup.addEventListener("click", () => {
        signup.style.color = "black"
        signup.style.backgroundColor = "white"
        signin.style.color = "white"
        signin.style.backgroundColor = "transparent"
        signin.style.borderBottom = "0.2rem solid white"
        var creator_id = signup.getAttribute("data-creator-id")
        var user_name = signup.getAttribute("data-user-name")
        window.location.href = `http://127.0.0.1:5000/creator/${user_name}?creator_id=${creator_id}&window=album`
    })
    signin.addEventListener("click", () => {
        signup.style.color = "black"
        signup.style.backgroundColor = "white"
        signin.style.color = "white"
        signin.style.backgroundColor = "transparent"
        signin.style.borderBottom = "0.2rem solid white"
        var creator_id = signin.getAttribute("data-creator-id")
        var user_name = signup.getAttribute("data-user-name")
        window.location.href = `http://127.0.0.1:5000/creator/${user_name}?creator_id=${creator_id}&window=songs`
    })

    let songPlayer = document.getElementsByClassName("songPlayer")
    for (let i = 0; i < songPlayer.length; i++) {
        songPlayer[i].addEventListener("click", () => {
            window.location.href = `/user/${songPlayer[i].getAttribute("data-user-name")}/lyrics?song_id=${songPlayer[i].getAttribute("data-song-id")}&current_time=0&paused=false`
        })
    }
    let songEditer = document.getElementsByClassName("songEditer")
    for (let i = 0; i < songEditer.length; i++) {
        songEditer[i].addEventListener("click", () => {
            window.location.href = `/creator/${songEditer[i].getAttribute("data-user-name")}/edit-song?song_id=${songEditer[i].getAttribute("data-song-id")}`
        })
    }
    let songDeleter = document.getElementsByClassName("songDeleter")
    for (let i = 0; i < songDeleter.length; i++) {
        songDeleter[i].addEventListener("click", () => {
            window.location.href = `/creator/${songDeleter[i].getAttribute("data-user-name")}/delete-song?song_id=${songDeleter[i].getAttribute("data-song-id")}`
        })
    }


    let albumPlayers = document.getElementsByClassName("albumPlayer");
    for (let i = 0; i < albumPlayers.length; i++) {
        let currentAlbumPlayer = albumPlayers[i];

        currentAlbumPlayer.addEventListener("click", () => {
            window.location.href = `/user/${currentAlbumPlayer.getAttribute("data-user-name")}/album?album_id=${currentAlbumPlayer.getAttribute("data-album-id")}`;
        });
    }
})

