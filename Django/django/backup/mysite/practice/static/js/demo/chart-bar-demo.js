// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}

// html -> JS로 데이터 가지고 오는 부분
function barchartsss(data) {

    min = Math.min(Number(data.arima),Number(data.fbprophet),Number(data.lstm),Number(data.close));
    max = Math.max(Number(data.arima),Number(data.fbprophet),Number(data.lstm),Number(data.close));

    if (min>100000){
        min = 100000;
    }else{
        min = 50000;
    }

    if(max>100000){
        max = Math.round(max/100000)*100000;
    }else{
        max = Math.round(max/10000)*10000;
    }
    myBarChart.options.scales.yAxes[0].ticks.min = Number(min);
    myBarChart.options.scales.yAxes[0].ticks.max = Number(max);
    myBarChart.data.datasets[1].data = [data.arima,data.fbprophet,data.lstm];
    myBarChart.data.datasets[0].data = [data.close,data.close,data.close];
    myBarChart.update();
}


// Bar Chart Example
var ctx = document.getElementById("myBarChart");

var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ["ARIMA", "FBProphet", "LSTM"],
    datasets: [

    {
//   종가 선
        type : 'line',
        fill : false,
        lineTension : 0.2,
        pointRadius : 0,
        backgroundColor: 'rgb(255, 204, 0)',
        borderColor: 'rgb(255, 204, 0)',
        data: [0,0,0],
    },
    {
//      label: "Revenue",
      backgroundColor: "#4e73df",
      hoverBackgroundColor: "#2e59d9",
      borderColor: "#4e73df",
      data: [0,0,0],
    }
    ],
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        time: {
          unit: 'month'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 6
        },
        maxBarThickness: 25,
      }],
      yAxes: [{
        ticks: {
          min: 70000,
          max: 76000,
          maxTicksLimit: 5,
          padding: 10,
          // Include a dollar sign in the ticks
          callback: function(value, index, values) {
            return '$' + number_format(value);
          }
        },
        gridLines: {
          color: "rgb(234, 236, 244)",
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: false
    },
    tooltips: {
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';

//          return datasetLabel + ': ' + number_format(tooltipItem.yLabel)+'원';
            return number_format(tooltipItem.yLabel)+'원';
        }
      }
    },
  }
});
