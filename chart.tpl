<!DOCTYPE html>
<html>
    <head>
        <script src="../../../js/Chart.bundle.min.js" ></script>
        <script src="../../../js/regression.min.js" ></script>
    </head>
    <body>
        <canvas id="profitMA" width="400" height="400"></canvas>
        <canvas id="revenueMA" width="400" height="400"></canvas>
    </body>
</html>

<script anything="{{value}}" chartTitle="{{chartTitle}}" >

    window.chartColors = {
	red: 'rgb(255, 99, 132)',
	orange: 'rgb(255, 159, 64)',
	yellow: 'rgb(255, 205, 86)',
	green: 'rgb(75, 192, 192)',
	blue: 'rgb(54, 162, 235)',
	purple: 'rgb(153, 102, 255)',
	grey: 'rgb(201, 203, 207)'
    };


const drawChart = (data, chartTitle, chart, data2) => {
    
    const result = regression('linear', dataParsed['Profit MA'])
    var ctx = document.getElementById(chart).getContext('2d');
    var lineChartData = {
        labels: data['Date'],
        datasets: [{
            label: 'Profit MA',
            borderColor: window.chartColors.red,
            backgroundColor: window.chartColors.red,
            fill: false,
            data: data['Profit MA'],
            yAxisID: 'y-axis-1',
            pointRadius: 0
        }, {
            label: null,
            borderColor: window.chartColors.blue,
            backgroundColor: window.chartColors.blue,
            fill: false,
            data: data2,
            yAxisID: 'y-axis-2',
            pointRadius: 0
        }]
    };

    chartLine = Chart.Line(ctx, {
        data: lineChartData,
        options: {
            responsive: true,
            hoverMode: 'index',
            stacked: false,
            title: {
                display: true,
                text: chartTitle
            },
            scales: {
                yAxes: [{
                    type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                    display: true,
                    position: 'left',
                    id: 'y-axis-1',
                }, {
                    type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                    display: true,
                    position: 'right',
                    id: 'y-axis-2',

                    // grid line settings
                    gridLines: {
                        drawOnChartArea: false, // only want the grid lines for one axis to show up
                    },
                }],
            }
        }
    });
}


data = document.getElementsByTagName("script")[2].getAttribute("anything");
title = document.getElementsByTagName("script")[2].getAttribute("chartTitle");
dataParsed = JSON.parse(data)
test = dataParsed['Profit MA']
mappedAsNumber = test.map( (value, index) => {return [index, Number(value)]});
console.log(mappedAsNumber)
const result = regression('linear', mappedAsNumber)
const gradient = result.equation[0];
const yIntercept = result.equation[1];

mappedAsNumber2 = result.points.map( (value) => {return value[1]});
console.log(mappedAsNumber2)
drawChart(JSON.parse(data), title, "profitMA", mappedAsNumber2)

</script>