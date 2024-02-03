document.addEventListener("DOMContentLoaded", function(){
            
    fetch("https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_sJKxCClG60490W45K687O97aQKtZ81izMeSa4aXj&currencies=")
    .then(response => response.json())
    .then(data => {
        const rate = data.data.BGN;
        document.querySelector("body").innerHTML = `1 USD = ${rate.toFixed(3)} BGN`;
    })
    })