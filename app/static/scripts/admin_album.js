// document.addEventListener("DOMContentLoaded", function () {
//     deleteSong = document.getElementsByClassName("deleteSong")
//     for (let i=0;i<deleteSong.length;i++){
//         deleteSong[i].addEventListener("click",()=>{
//             window.location.href = `../../admin-song-delete?album_id=${deleteSong[i].getAttribute("data-album-id")}&user_name=${deleteSong[i].getAttribute("data-user-name")}`
//         })
//     }
//     flagSong = document.getElementsByClassName("flagSong")
//     for (let i=0;i<flagSong.length;i++){
//         flagSong[i].addEventListener("click",()=>{
//             window.location.href = `../../admin-song-flag?album_id=${flagSong[i].getAttribute("data-album-id")}&user_name=${deleteSong[i].getAttribute("data-user-name")}`
//         })
//     }
// })