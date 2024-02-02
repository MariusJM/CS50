document.addEventListener("DOMContentLoaded", () => { // ()=> is the same as funtion()

    document.querySelector("select").onchange = function() {
        document.querySelector("#hello").style.color = this.value; //this is equal to the value of select
    }
});