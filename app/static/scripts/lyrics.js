let press = document.getElementById("press")
var audio = new Audio('../../static/songs/Badshaho.mp3');
let time = press.getAttribute("data-time")
let paused = press.getAttribute("data-paused")
var controlClicked = false
// var playClicked = false
var songId = 0
var userName = ""
audio.currentTime = time


let lyrics = document.getElementById("lyrics")
lyrics.addEventListener("click", ()=> {
    // if (playClicked){
        window.location.href =  `./${userName}`;
    // }
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

if (paused=="false"){
    audio.play()
    musicBarPlayPause.src = "../../static/images/pause.png"
    musicBarPlayPause.alt = "Pause"
}
