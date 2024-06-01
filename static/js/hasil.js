let x = ['positif','netral','negatif'];
let y = [40,10,50];
let color = ['rgb(14,116,144)','rgb(234,179,8)','rgb(185,28,28)']

const persen = new Chart(
    document.getElementById('persen'), {
    type: "doughnut",
    data: {
        labels: x,
        datasets: [{
            backgroundColor: color,
            data: y
        }]
    },
    options:{
        legend:{
            display: false
        }
    }
});