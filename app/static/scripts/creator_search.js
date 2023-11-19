document.addEventListener("DOMContentLoaded", function () {
    let search = document.getElementById("searchIcon")
    search.addEventListener("click", () => {
        let key = document.getElementById("typeIn").value
        let searchType = document.getElementById("filterList").value

        window.location.href = `../${search.getAttribute("data-user-name")}/search?filter=${searchType}&key=${key}`
    })
})