// Global Options
Chart.defaults.global.defaultFontFamily = 'Do Hyeon';
Chart.defaults.global.defaultFontSize = 16;
Chart.defaults.global.defaultFontColor = '#075E54';


function chartData(canvasId, data, title, label, color) {
    return {
        canvasId: canvasId,
        data: data.replace(/&#3[94];/g, '\"'),
        title: title,
        label: label,
        color: color
    }
}

function createChart(chartObject) {
    canvas = document.getElementById(chartObject.canvasId).getContext('2d');
    chartObject.data = JSON.parse(chartObject.data);

    new Chart(canvas, {
        type: 'bar', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
        data: {
            labels: Object.keys(chartObject.data),
            datasets: [{
                label: chartObject.label,
                data: Object.values(chartObject.data).concat([0]),
                backgroundColor: chartObject.color,
                borderWidth: 2,
                borderColor: '#fff',
                hoverBorderWidth: 3,
                hoverBorderColor: '#25D366'
            }]
        },
        options: {
            title: {
                display: true,
                text: chartObject.title,
                fontSize: 18
            },
            legend: {
                display: false,
                position: 'right',
                labels: {
                    fontColor: '#000'
                }
            },
            layout: {
                padding: {
                    left: 10,
                    right: 0,
                    bottom: 0,
                    top: 0
                }
            },
            tooltips: {
                enabled: true
            }
        }
    });
}