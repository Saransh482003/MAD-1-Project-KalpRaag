document.addEventListener("DOMContentLoaded", function () {
    let agree = document.getElementById("agree")
    agree.addEventListener("click", () => {
        $.get(`/creator-save?user_name=${agree.getAttribute("data-user")}`, function (data) {

        });
        window.location.href = `/user/${agree.getAttribute("data-user")}`
    })
})