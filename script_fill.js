document.addEventListener('DOMContentLoaded', function () {
    fetch('prize_2digits_counts.json')
        .then(response => response.json())
        .then(data => {
            const chartDiv = document.getElementById('chart');
            for (const [number, count] of Object.entries(data)) {
                const circle = document.createElement('div');
                circle.className = 'circle';
                circle.textContent = `${number}: ${count}`;
                chartDiv.appendChild(circle);
            }
        })
        .catch(error => console.error('Error fetching data:', error));
});

function getColor(count) {
    if (count > 10) return 'red';
    if (count > 5) return 'orange';
    return 'lightblue';
}