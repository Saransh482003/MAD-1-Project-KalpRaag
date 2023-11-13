let deletePlaylist = document.getElementById("delete")
var playlistName = deletePlaylist.getAttribute("data-playlist-name")
var user_name = deletePlaylist.getAttribute("data-user-name")
deletePlaylist.addEventListener("click",()=>{
    $.get(`/delete-playlist?playlist_name=${playlistName}&user_name=${user_name}`, function (data) {
        
    });
    window.location.href = `/user/${user_name}/liked_songs`
})

let deleteSong = document.getElementsByClassName('musicDeleter')
console.log(deleteSong)
for (let i=0;i<deleteSong.length;i++){
    deleteSong[i].addEventListener("click",()=>{

        $.get(`/delete-song-from-playlist?playlist_name=${deleteSong[i].getAttribute("data-playlist-name")}&user_name=${deleteSong[i].getAttribute("data-user-name")}&song_id=${deleteSong[i].getAttribute("data-song-id")}`, function (data) {
            
        });
        // window.location.href = `/user/${user_name}/playlists?playlist_id=${deleteSong[i].getAttribute("data-playlist-id")}&user_name=${deleteSong[i].getAttribute("data-playlist-name")}`
        window.location.href = `/user/${user_name}/liked_songs`
    })
}

let search = document.getElementById("searchIcon")
search.addEventListener("click",()=>{
    let key = document.getElementById("typeIn").value
    let searchType = document.getElementById("filterList").value
    window.location.href = `/user/${search.getAttribute("data-user-name")}/search?filter=${searchType}&key=${key}`
})