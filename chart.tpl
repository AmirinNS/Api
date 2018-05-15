<!DOCTYPE html>
<html>
    <head>
        <script src="../../../js/Chart.bundle.min.js" ></script>
    </head>
    <body>
        <canvas id="profit_regression" width="200" height="200"></canvas>
        <canvas id="revenue_regression" width="200" height="200"></canvas>
    </body>
</html>

<script dataFromAPI="{{value}}" >

    chartColors = {
	red: 'rgb(255, 99, 132)',
	orange: 'rgb(255, 159, 64)',
	yellow: 'rgb(255, 205, 86)',
	green: 'rgb(75, 192, 192)',
	blue: 'rgb(54, 162, 235)',
	purple: 'rgb(153, 102, 255)',
	grey: 'rgb(201, 203, 207)'
    };


const drawChart = (data, chartTitle, chartMaType, chartFor, lineColor, ) => {

    var ctx = document.getElementById(chartFor).getContext('2d');
    var lineChartData = {
        labels: data['Date'],
        datasets: [
            {
                label: chartMaType,
                borderColor: chartColors[lineColor],
                backgroundColor: chartColors[lineColor],
                fill: false,
                data: data[chartMaType],
                pointRadius: 5, 
                pointBackgroundColor: 'rgba(0, 0, 0, 0)',
                pointBorderColor: 'rgba(0, 0, 0, 0)'
            }, 
            {
                label: 'Projection',
                borderColor: chartColors.red,
                backgroundColor: window.chartColors.red,
                fill: false,
                data: data[chartFor],
                pointRadius: 0
            }
        ]
    };

    chartLine = Chart.Line(ctx, {
        data: lineChartData,
        options: {
            responsive: true,
            hoverMode: 'index',
            stacked: false,
            legend:{
                display:false
            },
            title: {
                display: true,
                text: chartTitle
            },
            scales: {
                yAxes: [{
                    type: 'linear',
                    display: true,
                    ticks: {
                        min: 0
                    },
                    gridLines: {
                        display: false
                    }
                }],
            }
        }
    });
}


data = document.getElementsByTagName("script")[1].getAttribute("dataFromAPI");
dataParsed = JSON.parse(data)
drawChart(dataParsed, 'Profit Indicator' , 'Profit MA', 'profit_regression', 'blue')
drawChart(dataParsed, 'Revenue Indicator', 'Revenue MA', 'revenue_regression', 'green')
</script>