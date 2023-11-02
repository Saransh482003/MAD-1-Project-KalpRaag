var audio = new Audio('../static/songs/Badshaho.mp3');
var controlClicked = false
// var controler = document

$(document).ready(function () {
    $('.update-content-link').click(function (event) {
        event.preventDefault();
        controlClicked = true
        musicBarPlayPause.src = "../static/images/pause.png"
        musicBarPlayPause.alt = "Pause"

        var songId = $(this).data('song-id');
        var userName = $(this).data('user-name');
        console.log(userName)
        if (!audio.paused){
            audio.pause()
            audio.currentTime = 0
            audio.play()
        }
        else {
            audio.currentTime = 0
            audio.play()
        }
        $.get('/update-section?song_id=' + songId, function (data) {
            $('#musicImgBottom').html(data["song_name"][0].toUpperCase());
            $('#musicNameBottom').html(data["song_name"][0].toUpperCase()+data["song_name"].slice(1,));
            $('#musicArtistBottom').html(data["artist_id"]);
            $('#musicDurationBottom').html(data["duration"]);
            $('#lyrics').attr("href",`./${userName}/lyrics?song_id=${songId}&current_time=${audio.currentTime}`)
        });
    });
});


let musicBarPlayPause = document.getElementById("musicBarPlayPause")
let playPause = document.getElementById("playPause")
playPause.addEventListener("click", ()=>{
    controlClicked = !controlClicked
    if (controlClicked){
        musicBarPlayPause.src = "../static/images/pause.png"
        musicBarPlayPause.alt = "Pause"
        if (audio.paused){
            audio.play()
            
            console.log(audio.currentTime)
        }
    }
    else{
        musicBarPlayPause.src = "../static/images/play.png"
        musicBarPlayPause.alt = "Play"
        if (!audio.paused){
            audio.pause()
        }
    }
})

let previous = document.getElementById("previous")
previous.addEventListener("click", ()=>{
    audio.currentTime = 0
    if (audio.paused){
        audio.play()
    }
})

let forward = document.getElementById("forward")
forward.addEventListener("click", ()=>{
    audio.currentTime = audio.duration-1
})

let previous10Sec = document.getElementById("previous10Sec")
previous10Sec.addEventListener("click", ()=>{
    audio.currentTime = (audio.currentTime-10>=0) ? audio.currentTime-10 : 0;
    if (audio.paused){
        audio.play()
    }
})

let forward10Sec = document.getElementById("forward10Sec")
forward10Sec.addEventListener("click", ()=>{
    audio.currentTime = (audio.currentTime+10<=audio.duration) ? audio.currentTime+10 : audio.duration-1;
    if (audio.paused){
        audio.play()
    }
})