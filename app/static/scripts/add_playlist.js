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
    let key = document.getElementById("typeIn").value
    let searchType = document.getElementById("filterList").value
    console(key,searchType)
    window.location.href = `/user/${search.getAttribute("data-user-name")}/search?filter=${searchType}&key=${key}`
})