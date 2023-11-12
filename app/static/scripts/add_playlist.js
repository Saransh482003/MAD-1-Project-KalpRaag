let createBtn = document.getElementById("createBtn")
var newName = ""
var user_name = createBtn.getAttribute("data-user")

createBtn.addEventListener("click", ()=>{
    newName = document.getElementById("newName").value
    if (newName){
        $.get(`/add-playlist?playlist_name=${newName}&user_name=${user_name}`, function (data) {
        
        });
        window.location.href = `/user/${user_name}/liked_songs`
    }
})

let search = document.getElementById("searchIcon")
search.addEventListener("click",()=>{
    window.location.href = "/user/Saransh%20Saini/search"
})