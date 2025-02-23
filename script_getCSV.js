d3.csv("CSV_lotto/lotto_prize_combined.csv").then(data => {
    const prize2DigitsCount = {};

    data.forEach(d => {
        d.prize_2digits = d.prize_2digits.replace(/[\[\]']/g, "").split(",");
        d.prize_2digits.forEach(prize => {
            if (prize2DigitsCount[prize]) {
                prize2DigitsCount[prize]++;
            } else {
                prize2DigitsCount[prize] = 1;
            }
        });
    });

    console.log(prize2DigitsCount);
    createPrize2DigitsGraph(prize2DigitsCount);
});

function createPrize2DigitsGraph(prize2DigitsCount) {
    const prizes = Object.keys(prize2DigitsCount);
    const counts = Object.values(prize2DigitsCount);

    const ctx = document.getElementById('prize2DigitsChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: prizes,
            datasets: [{
                label: 'Count of Prize 2 Digits',
                data: counts,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
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
}
