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

// Area Chart Example
// html -> JS로 데이터 가지고 오는 부분
function datasearch(data) {
    var values = document.getElementById("datasearch").value;
    var fin =[]
    var dates = []
    for (var i=0; i<data.length;i++){
        fin.push(data[i]['changes'])
//        if (data[i]['dates']){
//            continue;
//        }
        dates.push(data[i]['dates'])

        if (data[i]['changes']>0){
//             console.log('where',data[i]['changes'])
//        #########################################################파랑색
            myLineChart.data.datasets[0].pointBorderColor = "rgba(20, 118, 223, 1)"
        }else{
//        #########################################################빨간색
            myLineChart.data.datasets[0].pointBorderColor = "rgba(255, 0, 66, 1)"
        }

    }
    myLineChart.data.datasets[0].data = fin;
//    for(var i=0;i<data.length;i++){
//         a= myLineChart.data.datasets[0].data[i]
//         if(a<0){
//            console.log('?')
//            myLineChart.data.datasets[0].backgroundColor = "rgba(20, 118, 223, 1)"
//         }else{
//            console.log('!')
//            myLineChart.data.datasets[0].backgroundColor = "rgba(255, 0, 66, 1)"
//         }
//    }
    myLineChart.data.labels = dates;
    myLineChart.update();
}

var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
//    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    labels:[],
    datasets: [{
      label: "변동률",
      lineTension: 0.3,
//      backgroundColor: "rgba(78, 115, 223, 0.05)",
//      backgroundColor: barColors,
//      backgroundColor: fillJsFunc(myLineChart.data.datasets[0].data[0]),
      borderColor: "rgba(78, 115, 223, 1)",
      pointRadius: 3,
//      pointBackgroundColor: "rgba(78, 115, 223, 1)",
      pointBackgroundColor: "rgba(206, 141, 153, 1)",
      pointBorderColor: "rgba(78, 115, 223, 1)",
      pointHoverRadius: 3,
      pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
      pointHoverBorderColor: "rgba(78, 115, 223, 1)",
      pointHitRadius: 10,
      pointBorderWidth: 2,
//      line 아래쪽 색칠
      fill: true,
//      data: [5000, 10000, 5000, 15000, 10000, 20000, 15000, 25000, 20000, 30000, 25000, 100000],
      data:[],
//      data2:[],
    }],
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
          unit: 'date'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 7
        }
      }],
      yAxes: [{
      // y축
        ticks: {
          maxTicksLimit: 5,
          padding: 10,
          // Include a dollar sign in the ticks
          callback: function(value, index, values) {
//          y축 라벨 값
//            return number_format(value) + '원';
            return number_format(value);
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
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      intersect: false,
      mode: 'index',
      caretPadding: 10,

//      데이터 값 라벨 표시
      callbacks: {
        label: function(tooltipItem, chart) {
//            console.log(chart.datasets[tooltipItem.datasetIndex])
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
//          return datasetLabel + ' : ' + number_format(chart.datasets[tooltipItem.datasetIndex].data) + '%';
//          return datasetLabel + ' : ' + chart.datasets[tooltipItem.datasetIndex].data + '%';
//          return datasetLabel + ' : ' + number_format(tooltipItem.yLabel) + '%';
//            number_format(chart.datasets[tooltipItem.datasetIndex].data2)
//          팝라벨 값 표시
//            return datasetLabel + ' : ' + tooltipItem.value + '%';
            return datasetLabel + ' : ' + tooltipItem.value;
        }
      }
    }
  }
});
