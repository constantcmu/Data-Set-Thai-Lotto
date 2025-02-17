document.addEventListener('DOMContentLoaded', function () {
    fetch('lotto_prize_combined.csv')
        .then(response => response.text())
        .then(data => {
            const rows = data.split('\n').slice(1);
            const frequency = {};

            rows.forEach(row => {
                const columns = row.split(',');
                const prize2digits = columns[2].replace(/[\[\]']/g, '').split(' ');

                prize2digits.forEach(prize => {
                    if (prize) {
                        frequency[prize] = (frequency[prize] || 0) + 1;
                    }
                });
            });

            const categories = Object.keys(frequency);
            const dataSeries = categories.map(prize => frequency[prize]);

            Highcharts.chart('chart', {
                chart: {
                    type: 'column'
                },
                title: {
                    text: 'Prize 2 Digits Frequency'
                },
                xAxis: {
                    categories: categories,
                    title: {
                        text: 'Prize 2 Digits'
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Frequency'
                    }
                },
                series: [{
                    name: 'Frequency',
                    data: dataSeries
                }]
            });
        });
});

function getColor(count) {
    if (count > 10) return 'red';
    if (count > 5) return 'orange';
    return 'lightblue';
}
