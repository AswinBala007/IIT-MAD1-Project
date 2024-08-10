const ct_1 = document.getElementById('myCharts').getContext('2d');
const sp = document.getElementById('sport').innerHTML;
const an = document.getElementById('an').innerHTML;
const tr = document.getElementById('tr').innerHTML;
const food = document.getElementById('food').innerHTML;
const ent = document.getElementById('en').innerHTML;
const ot = document.getElementById('ot').innerHTML;
// console.log(ct,"wkeebefbq")     
const myCharts = new Chart(ct_1, {
    type: 'bar', 
    data: {
        labels: ['Sports', 'Animal','Travel','Food','Entertainment','Others'], 
        datasets: [{
            label: '# of Niches',
            data: [sp,an,tr,food,ent,ot], 
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