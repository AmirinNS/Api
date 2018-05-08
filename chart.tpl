<!DOCTYPE html>
<html>
    <head>
        <script src="../../../js/Chart.bundle.min.js" ></script>
    </head>
    <body>
        <canvas id="myChart" width="400" height="400"></canvas>
    </body>
</html>

<script anything="{{value}}" chartTitle="{{chartTitle}}">

    window.chartColors = {
	red: 'rgb(255, 99, 132)',
	orange: 'rgb(255, 159, 64)',
	yellow: 'rgb(255, 205, 86)',
	green: 'rgb(75, 192, 192)',
	blue: 'rgb(54, 162, 235)',
	purple: 'rgb(153, 102, 255)',
	grey: 'rgb(201, 203, 207)'
    };


const drawChart = (data, chartTitle) => {
    var ctx = document.getElementById("myChart").getContext('2d');

    var lineChartData = {
        labels: data['Date'],
        datasets: [{
            label: 'Profit MA',
            borderColor: window.chartColors.red,
            backgroundColor: window.chartColors.red,
            fill: false,
            data: data['Profit MA'],
            yAxisID: 'y-axis-1',
        }, {
            label: 'Revenue MA',
            borderColor: window.chartColors.blue,
            backgroundColor: window.chartColors.blue,
            fill: false,
            data: data['Revenue MA'],
            yAxisID: 'y-axis-2'
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

const getChartImage = () => {
    return url_base64jp = document.getElementById("myChart").toDataURL("image/jpg");
}

data = document.getElementsByTagName("script")[1].getAttribute("anything");
title = document.getElementsByTagName("script")[1].getAttribute("chartTitle");
drawChart(JSON.parse(data), title)

</script>