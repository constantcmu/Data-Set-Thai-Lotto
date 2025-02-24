document.addEventListener('DOMContentLoaded', function() {
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
        colorNumbers(prize2DigitsCount); // Call the function to color the numbers
        addTooltips(prize2DigitsCount); // Call the function to add tooltips
    });

    function createPrize2DigitsGraph(prize2DigitsCount) {
        const prizes = Object.keys(prize2DigitsCount);
        const counts = Object.values(prize2DigitsCount);

        const ctx = document.getElementById('prize2DigitsChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',  // Change the type to 'line' for line graph
            data: {
                labels: prizes,
                datasets: [{
                    label: 'Freq.',
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

    // Function to color the numbers in the index page based on frequency
    function colorNumbers(prize2DigitsCount) {
        const numbers = document.querySelectorAll('.row span');
        numbers.forEach(number => {
            const num = number.textContent;
            if (prize2DigitsCount[num]) {
                let color;
                // if (prize2DigitsCount[num] > 8) {
                //     color = 'red';
                // } else 
                if (prize2DigitsCount[num] ) {
                    const clarity = prize2DigitsCount[num] / 8; // Normalize to range 0-1
                    color = `rgba(250, 80, 80, ${clarity})`; // Yellow color with varying clarity
                } else {
                    color = 'transparent'; // Default color if not in range
                }
                number.style.backgroundColor = color;
            }
        });
    }

    // Function to add tooltips to display the frequency count
    function addTooltips(prize2DigitsCount) {
        const numbers = document.querySelectorAll('.number');
        numbers.forEach(number => {
            const num = number.getAttribute('data-number');
            if (prize2DigitsCount[num]) {
                number.setAttribute('data-frequency', prize2DigitsCount[num]);
            } else {
                number.setAttribute('data-frequency', '0');
            }
        });
    }
});