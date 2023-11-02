let press = document.getElementById("press")
var audio = new Audio('../static/songs/Badshaho.mp3');
press.addEventListener("click",()=>{
    let time = press.getAttribute("data-time")
    audio.currentTime = time
    audio.play()
})