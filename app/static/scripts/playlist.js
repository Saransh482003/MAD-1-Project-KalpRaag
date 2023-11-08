
let deletePlaylist = document.getElementById("delete")
var playlistName = deletePlaylist.getAttribute("data-playlist-name")
var user_name = deletePlaylist.getAttribute("data-user-name")
deletePlaylist.addEventListener("click",()=>{
    $.get(`/delete-playlist?playlist_name=${playlistName}&user_name=${user_name}`, function (data) {
        
    });
    window.location.href = `/user/${user_name}/liked_songs`
})