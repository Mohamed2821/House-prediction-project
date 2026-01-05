let chart;

function predict() {
    let area = document.getElementById("area").value;
    let bedrooms = document.getElementById("bedrooms").value;
    let bathrooms = document.getElementById("bathrooms").value;

    let loader = document.getElementById("loader");
    let priceText = document.getElementById("price");

    loader.style.display = "block";
    priceText.innerHTML = "";

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `area=${area}&bedrooms=${bedrooms}&bathrooms=${bathrooms}`
    })
    .then(res => res.json())
    .then(data => {
        loader.style.display = "none";
        animatePrice(data.price);
        drawChart(area, data.price);
    });
}

function animatePrice(price) {
    let priceText = document.getElementById("price");
    let current = 0;
    let interval = setInterval(() => {
        current += price / 50;
        priceText.innerHTML = "₹ " + Math.round(current);
        if (current >= price) clearInterval(interval);
    }, 20);
}

function drawChart(area, price) {
    let ctx = document.getElementById("chart");
    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: ["Area"],
            datasets: [{
                label: "Price",
                data: [price],
                borderWidth: 3
            }]
        }
    });
}
