const ctx = document.getElementById('myChart').getContext('2d');
const ct = document.getElementById('ct').innerHTML;
const ct1 = document.getElementById('ct1').innerHTML;
// console.log(ct,"wkeebefbq")
const myChart = new Chart(ctx, {
    type: 'doughnut', 
    data: {
        labels: ['Influencers', 'Sponsors'], 
        datasets: [{
            label: '# of Votes',
            data: [ct, ct1], 
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
               
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});