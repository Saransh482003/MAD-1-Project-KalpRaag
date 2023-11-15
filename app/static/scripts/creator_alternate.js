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
    let albumPlayers = document.getElementsByClassName("albumPlayer");
    console.log(albumPlayers);

    for (let i = 0; i < albumPlayers.length; i++) {
        let currentAlbumPlayer = albumPlayers[i];

        currentAlbumPlayer.addEventListener("click", () => {
            window.location.href = `/user/${currentAlbumPlayer.getAttribute("data-user-name")}/album?album_id=${currentAlbumPlayer.getAttribute("data-album-id")}`;
        });
    }
});