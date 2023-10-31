$(document).ready(function () {
    $('.update-content-link').click(function (event) {
        event.preventDefault();

        var songId = $(this).data('song-id');

        $.get('/update-section?song_id=' + songId, function (data) {
            $('#musicImgBottom').html(data["song_name"][0].toUpperCase());
            $('#musicNameBottom').html(data["song_name"][0].toUpperCase()+data["song_name"].slice(1,));
            $('#musicArtistBottom').html(data["artist_id"]);
            $('#musicDurationBottom').html(data["duration"]);
            $('#lyrics').attr("href",`./{{user_name}}/lyrics?song_id=${songId}`)
        });
    });
});

var controlClicked = false
var controler = document.getElementById("musicBarControl")
var controlerCont = document.getElementById("controler")
controlerCont.addEventListener("click", ()=>{
    controlClicked = !controlClicked
    if (controlClicked){
        controler.src = "pause.png"
        controler.alt = "Pause"
    }
    else{
        controler.src = "play.png"
        controler.alt = "Play"
    }
})