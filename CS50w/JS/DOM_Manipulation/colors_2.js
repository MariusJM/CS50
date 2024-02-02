document.addEventListener("DOMContentLoaded", () => { // ()=> is the same as funtion()

    document.querySelectorAll("button").forEach(button => { // button => is the same as funtion(button)
        button.onclick = function() {
            document.querySelector("#hello").style.color = button.dataset.color;
        }
    });
});