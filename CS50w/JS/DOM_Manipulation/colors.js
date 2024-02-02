document.addEventListener("DOMContentLoaded", function(){
    document.querySelector("#red").onclick = function(){
        document.querySelector("#hello").style.color = "red";
    }
    document.querySelector("#blue").onclick = function(){
        document.querySelector("#hello").style.color = "blue";
    }
    document.querySelector("#green").onclick = function(){
        document.querySelector("#hello").style.color = "green";
    }
});