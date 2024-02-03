document.addEventListener("DOMContentLoaded", function(){

    document.querySelector("form").onsubmit = function(){
        fetch("https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_sJKxCClG60490W45K687O97aQKtZ81izMeSa4aXj&currencies=")
        .then(response => response.json())
        .then(data => {
            const currency = document.querySelector("#currency").value.toUpperCase();
            const rate = data.data[currency];
            if (rate !== undefined){
                document.querySelector("#result").innerHTML = `1 USD = ${rate.toFixed(3)} ${currency}`;
            } else {
                document.querySelector("#result").innerHTML = "Invalid Currency.";
            }  
        })
        .catch(error => {
            console.log("Error: ", error);
        });
        return false
    }
    });