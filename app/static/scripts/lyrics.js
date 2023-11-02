let press = document.getElementById("press")
var audio = new Audio('../../static/songs/Badshaho.mp3');
let time = press.getAttribute("data-time")
audio.currentTime = time
audio.play()