let album = document.getElementById("saver")
var album_name = album.getAttribute("data-album-name")
var user_name = album.getAttribute("data-user-name")
var saved = album.getAttribute("data-status")
album.addEventListener("click",()=>{
    if (saved==1){
        album.src = "../../static/images/save_blank.png"
        saved = 0
    }
    else{
        album.src = "../../static/images/save_full.png"
        saved = 1
    }
    $.get(`/save-album?album_name=${album_name}&user_name=${user_name}&status=${saved}`, function (data) {
        
    });
    window.location.href = `/user/${user_name}/liked_songs`
})

// let search = document.getElementById("searchIcon")
// search.addEventListener("click",()=>{
//     let key = document.getElementById("typeIn").value
//     let searchType = document.getElementById("filterList").value
//     window.location.href = `/user/${search.getAttribute("data-user-name")}/search?filter=${searchType}&key=${key}`
// })