// ==================
// Leaflet Map Setup
// ==================

home_url = 'https://curryscorer.azurewebsites.net/api/v1.0/'
map_url = home_url + 'map'
bar_url = home_url + 'top-cuisines?borough='
pie_url = home_url + 'cuisine-distributions'
table_url = home_url + 'borough-summaries'

const map = L.map('map').setView([40.7128, -74.0060], 9);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);


d3.json(map_url).then(data => {
  // Create a marker cluster group
  const markers = L.markerClusterGroup();
  const results = data.results;

  for (let i = 0; i < results.length; i++) {
    let loc = results[i];

    if (loc) {
      markers
        .addLayer(
          L.marker([loc.lat, loc.lng])
            .bindPopup(
              `<b>${loc.name}</b><br>Borough: ${loc.borough}<br>Cuisine: ${loc.cuisine}<br>Inspected: ${new Date(loc.inspection_date).toLocaleDateString()}`
            )
          );
      };
    };
  map.addLayer(markers);
  }
);

// ==================
// Bar Chart (Plotly)
// ==================


// List borough names needed
const boroughs = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island'];

// Function to perform API call and plot the data
function updatePlot(borough) {
  d3.json(bar_url + borough).then(data => {
    let results = data.results
    results = results.slice(0, 10);
    
    // Prepare the trace for the bar chart
    const barTrace = {
      x: results.map(item => item.cuisine),
      y: results.map(item => item.count),
      type: 'bar',
      marker: {
        color: 'rgba(55,128,191,0.7)',
        line: { color: 'rgba(55,128,191,1.0)', width: 2 }
      }
    };

    // Define the layout with a dynamic title
    const barLayout = {
      title: `Top Cuisines in ${borough}`,
      xaxis: {
        title: 'Cuisine',
        tickangle: 45 
      },
      yaxis: { title: 'Count' }
    };

    // Use Plotly.react to update the chart if it exists, or create it if not
    Plotly.react('barChart', [barTrace], barLayout);
  }).catch(error => {
    console.error('Error fetching data:', error);
  });
}

// Event listener for the dropdown to update the plot on selection change
document.getElementById('boroughSelect').addEventListener('change', function() {
  const selectedBorough = this.value;
  updatePlot(selectedBorough);
});

// Run the function on initial load for the default borough
updatePlot('Manhattan');


// ==================
// Pie Chart (Plotly)
// ==================
d3.json(pie_url).then(data => {
  // Limit to top 10 or 15 to avoid too many slices
  let results = data.results.slice(0, 10);

  // Optionally group very small slices into an "Other" category
  // This is just an example – adapt as needed
  // const threshold = 2; // 2%
  // const mainSlices = results.filter(d => d.percent >= threshold);
  // const otherSlices = results.filter(d => d.percent < threshold);
  // if (otherSlices.length > 1) {
  //   const otherSum = otherSlices.reduce((acc, cur) => acc + cur.percent, 0);
  //   mainSlices.push({ cuisine: 'Other', percent: otherSum });
  // }
  // results = mainSlices;

  const pieTrace = {
    labels: results.map(d => d.cuisine),
    values: results.map(d => d.percent),
    type: 'pie',
    hoverinfo: 'label+percent+value',
    textposition: 'inside',  // put labels outside each slice
    automargin: true,         // helps with label cutoff
    marker: {
      line: { color: '#fff', width: 1 } // thin border between slices
    },
    // You can also adjust the domain if you want extra space for a legend on the side:
    // domain: { x: [0, 0.7], y: [0, 1] }
  };

  const pieLayout = {
    title: 'Ethnic Cuisine Distribution',
    // Give the chart a larger footprint
    width: 500,
    height: 400,
    margin: { t: 40, b: 40, l: 20, r: 20 },
  };

  Plotly.newPlot('pieChart', [pieTrace], pieLayout);
});

// ==================
// Borough Summary Table
// ==================

d3.json(table_url).then(data => {
  let results = data.results;

  const tableBody = document.getElementById("boroughTableBody");

  results.forEach(row => {
    let perCapita = row.restaurant_count/row.population;
  const tr = document.createElement("tr");
  tr.innerHTML = `
    <td>${row.borough}</td>
    <td>${row.restaurant_count}</td>
    <td>${perCapita.toFixed(3)}</td>
  `;
  tableBody.appendChild(tr);
});
})


