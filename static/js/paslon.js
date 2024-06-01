let xcapres = ['positif','netral','negatif'];
let ycapres = [40,10,50];
let colorcapres = ['rgb(14,116,144)','rgb(234,179,8)','rgb(185,28,28)'];

const capres = new Chart(
    document.getElementById('capres'), {
    type: "doughnut",
    data: {
        labels: xcapres,
        datasets: [{
            backgroundColor: colorcapres,
            data: ycapres
        }]
    },
    options:{
        legend:{
            display: false
        }
    }
});

let xcawa = ['positif','netral','negatif'];
let ycawa = [40,10,50];
let colorcawa = ['rgb(14,116,144)','rgb(234,179,8)','rgb(185,28,28)'];

const cawapres = new Chart(
    document.getElementById('cawapresx'), {
    type: "doughnut",
    data: {
        labels: xcawa,
        datasets: [{
            backgroundColor: colorcawa,
            data: ycawa
        }]
    },
    options:{
        legend:{
            display: false
        }
    }
});