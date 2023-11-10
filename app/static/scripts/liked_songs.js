var audio = new Audio('../../static/songs/Badshaho.mp3');
var controlClicked = false
var playClicked = false
var songId = 0
var userName = ""

let song_menu = document.getElementById("song_menu")
song_menu.addEventListener("click", () => {
    window.location.href = `/user/${song_menu.getAttribute("data-user")}`
})


$(document).ready(function () {
    $('.update-content-link').click(function (event) {
        event.preventDefault();
        controlClicked = true
        playClicked = true
        musicBarPlayPause.src = "../../static/images/pause.png"
        musicBarPlayPause.alt = "Pause"

        songId = $(this).data('song-id');
        userName = $(this).data('user-name');
        console.log(userName)
        if (!audio.paused) {
            audio.pause()
            audio.currentTime = 0
            audio.play()
        }
        else {
            audio.currentTime = 0
            audio.play()
        }

        // alert(current_time)
        $.get('/update-section?song_id=' + songId, function (data) {
            $('#musicImgBottom').html(data["song_name"][0].toUpperCase());
            $('#musicNameBottom').html(data["song_name"][0].toUpperCase() + data["song_name"].slice(1,));
            $('#musicArtistBottom').html(data["artist_id"]);
            $('#musicDurationBottom').html(data["duration"]);
            // $('#lyrics').attr("href", `./${userName}/lyrics?song_id=${songId}`)
        });
    });
});

let lyrics = document.getElementById("lyrics")
lyrics.addEventListener("click", ()=> {
    if (playClicked){
        window.location.href =  `../${userName}/lyrics?song_id=${songId}&current_time=${audio.currentTime}&paused=${audio.paused}`;
    }
})

let musicBarPlayPause = document.getElementById("musicBarPlayPause")
let playPause = document.getElementById("playPause")
playPause.addEventListener("click", () => {
    controlClicked = !controlClicked
    if (controlClicked) {
        musicBarPlayPause.src = "../../static/images/pause.png"
        musicBarPlayPause.alt = "Pause"
        if (audio.paused) {
            audio.play()

            console.log(audio.currentTime)
        }
    }
    else {
        musicBarPlayPause.src = "../../static/images/play.png"
        musicBarPlayPause.alt = "Play"
        if (!audio.paused) {
            audio.pause()
        }
    }
})

let previous = document.getElementById("previous")
previous.addEventListener("click", () => {
    audio.currentTime = 0
    if (audio.paused) {
        audio.play()
    }
})

let forward = document.getElementById("forward")
forward.addEventListener("click", () => {
    audio.currentTime = audio.duration - 1
})

let previous10Sec = document.getElementById("previous10Sec")
previous10Sec.addEventListener("click", () => {
    audio.currentTime = (audio.currentTime - 10 >= 0) ? audio.currentTime - 10 : 0;
    if (audio.paused) {
        audio.play()
    }
})

let forward10Sec = document.getElementById("forward10Sec")
forward10Sec.addEventListener("click", () => {
    audio.currentTime = (audio.currentTime + 10 <= audio.duration) ? audio.currentTime + 10 : audio.duration - 1;
    if (audio.paused) {
        audio.play()
    }
})

let deleteSong = document.getElementsByClassName('musicDeleter')
for (let i=0;i<deleteSong.length;i++){
    deleteSong[i].addEventListener("click",()=>{
        $.get(`/unlike-song?user_name=${deleteSong[i].getAttribute("data-user-name")}&song_id=${deleteSong[i].getAttribute("data-song-id")}`, function (data) {
            
        });
        window.location.href = `/user/${deleteSong[i].getAttribute("data-user-name")}`
    })
}