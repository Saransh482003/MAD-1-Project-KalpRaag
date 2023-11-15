document.addEventListener("DOMContentLoaded", function () {
    let inHead = document.getElementById("signin")
    let upHead = document.getElementById("signup")
    let logTitle = document.getElementById("loggerHead")
    let form = document.getElementById("logger")
    let messenger = document.getElementById("messenger")

    signup = () => {
        upHead.style.color = "black"
        upHead.style.backgroundColor = "white"
        inHead.style.color = "white"
        inHead.style.backgroundColor = "#141414"
        logTitle.innerHTML = "Join the <span>Raag</span> Now!!"
        form.action = "/signup"
        messenger.innerHTML = ""
    }
    signin = () => {
        upHead.style.color = "white"
        upHead.style.backgroundColor = "#141414"
        inHead.style.color = "black"
        inHead.style.backgroundColor = "white"
        logTitle.innerHTML = "Welcome Back to the <span>Raag!!</span>"
        form.action = "/signin"
        messenger.innerHTML = ""
    }
})