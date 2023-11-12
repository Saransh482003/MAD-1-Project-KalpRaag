let press = document.getElementById("press")
var audio = new Audio('../../static/songs/Badshaho.mp3');
let time = press.getAttribute("data-time")
let paused = press.getAttribute("data-paused")
var controlClicked = false
// var playClicked = false
var userName = ""
audio.currentTime = time


let lyrics = document.getElementById("lyrics")
lyrics.addEventListener("click", () => {
    window.location.href = `/user/${lyrics.getAttribute("data-user")}`
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

            // console.log(audio.currentTime)
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

if (paused == "false") {
    audio.play()
    musicBarPlayPause.src = "../../static/images/pause.png"
    musicBarPlayPause.alt = "Pause"
}


let star0 = document.getElementById("star0")
let star1 = document.getElementById("star1")
let star2 = document.getElementById("star2")
let star3 = document.getElementById("star3")
let star4 = document.getElementById("star4")

for (let i = 0; i < 5; i++) {
    window["star" + i].addEventListener("mouseover", () => {
        for (let j = 0; j <= i; j++) {
            window["star" + j].src = "../../static/images/full_star.png"
        }
        for (let j = i + 1; j < 6; j++) {
            window["star" + j].src = "../../static/images/blank_star.png"
        }
    })
}

let musicStat = document.getElementById("musicStats")
var song_id = musicStat.getAttribute("data-songID")
var rate = musicStat.getAttribute("data-rating")
var user_name = musicStat.getAttribute("data-user")

musicStat.addEventListener("mouseout", () => {
    for (let i = 0; i < 5; i++) {
        if (i <= rate - 1) {
            window["star" + i].src = "../../static/images/full_star.png"
        }
        else {
            window["star" + i].src = "../../static/images/blank_star.png"
        }
    }
})
let rating = document.getElementById("rating")
for (let i = 0; i < 5; i++) {
    window["star" + i].addEventListener("click", (event) => {
        event.preventDefault()
        rate = i + 1
        rating.innerHTML = rate
        for (let j = 0; j <= i; j++) {
            window["star" + j].src = "../../static/images/full_star.png"
        }
        for (let j = i + 1; j < 6; j++) {
            window["star" + j].src = "../../static/images/blank_star.png"
        }

        let data = {
            "song_id": song_id,
            "rating": rate
        }
        alert(window["star"+i])
        fetch('/update-song-rating', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response from the server if needed
            console.log(data);
        })
        .catch(error => {
            // Handle errors here
            console.error(error);
        })
    })
}

let love = document.getElementById("love")
var loveVal = love.getAttribute("data-love")
love.addEventListener("click",()=>{
    loveVal = loveVal==0 ? 1 : 0
    if (loveVal==1){
        love.src = "../../static/images/full_heart.png"
    }
    else{
        love.src = "../../static/images/blank_heart.png"
    }
})


musicStat.addEventListener("click", () => {
    $.get(`/update-song-rating?song_id=${song_id}&rating=${rate}&user_name=${user_name}&love=${loveVal}`, function (data) {
        
    });
})

let addToPlaylist = document.getElementById("add")
addToPlaylist.addEventListener("click",()=>{
    let dropDown = document.getElementById("dropDown")
    let dropVal = dropDown.value
    $.get(`/add-song-to-playlist?song_id=${song_id}&user_name=${user_name}&playlist_name=${dropVal}`, function (data) {
        
    });
})

let search = document.getElementById("searchIcon")
search.addEventListener("click",()=>{
    window.location.href = "/user/Saransh%20Saini/search"
})