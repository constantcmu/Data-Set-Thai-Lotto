document.addEventListener('DOMContentLoaded', function () {
    fetch('CSV_lotto/lotto_prize_combined.csv')
        .then(response => response.text())
        .then(data => {
            const rows = data.split('\n').slice(1);
            const frequency = {};

            rows.forEach(row => {
                const cols = row.split(',');
                const prize2digits = cols[2].replace(/[\[\]']/g, '').split(' ');
                prize2digits.forEach(num => {
                    if (num) {
                        frequency[num] = (frequency[num] || 0) + 1;
                    }
                });
            });

            // D3.js code to create a bar chart
            const margin = { top: 20, right: 30, bottom: 40, left: 40 };
            const width = 800 - margin.left - margin.right;
            const height = 400 - margin.top - margin.bottom;

            const svg = d3.select("#chart")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", `translate(${margin.left},${margin.top})`);

            const x = d3.scaleBand()
                .domain(Object.keys(frequency))
                .range([0, width])
                .padding(0.1);

            const y = d3.scaleLinear()
                .domain([0, d3.max(Object.values(frequency))])
                .nice()
                .range([height, 0]);

            svg.append("g")
                .selectAll("rect")
                .data(Object.entries(frequency))
                .enter()
                .append("rect")
                .attr("x", d => x(d[0]))
                .attr("y", d => y(d[1]))
                .attr("width", x.bandwidth())
                .attr("height", d => height - y(d[1]))
                .attr("fill", "steelblue");

            svg.append("g")
                .attr("class", "x-axis")
                .attr("transform", `translate(0,${height})`)
                .call(d3.axisBottom(x));

            svg.append("g")
                .attr("class", "y-axis")
                .call(d3.axisLeft(y));
        })
        .catch(error => console.error('Error fetching data:', error));
});

function getColor(count) {
    if (count > 10) return 'red';
    if (count > 5) return 'orange';
    return 'lightblue';
}