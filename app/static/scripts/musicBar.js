var audio = new Audio('../static/songs/Badshaho.mp3');
var controlClicked = false
$(document).ready(function () {
    $('.update-content-link').click(function (event) {
        event.preventDefault();
        controlClicked = true
        controler.src = "../static/images/pause.png"
        controler.alt = "Pause"

        var songId = $(this).data('song-id');
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
            $('#lyrics').attr("href",`./{{user_name}}/lyrics?song_id=${songId}`)
        });
    });
});




var controler = document.getElementById("musicBarControl")
var controlerCont = document.getElementById("controler")
controlerCont.addEventListener("click", ()=>{
    controlClicked = !controlClicked
    if (controlClicked){
        controler.src = "../static/images/pause.png"
        controler.alt = "Pause"
        if (audio.paused){
            audio.play()
        }
    }
    else{
        controler.src = "../static/images/play.png"
        controler.alt = "Play"
        if (!audio.paused){
            audio.pause()
        }
    }
})

var controlerBack = document.getElementById("musicBarControlBack")
var controlerContBack = document.getElementById("controlBack")
controlerContBack.addEventListener("click", ()=>{
    audio.currentTime = 0
})