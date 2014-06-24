// JavaScript Document


$(function() {
        // Create the chart
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'highcharts-donut',
                type: 'pie',
								width: 300,
								height: 300,
								margin: [0, 0, 0, 0]
            },
            title: {
                text: 'Browser market share, April, 2011'
            },
						legend: {
								 enabled: false
						 },
						 credits: {
								 enabled: false
						 },
						 exporting: {
								 enabled: false
						 },
            yAxis: {
                title: {
                    text: 'Total percent market share'
                }
            },
            plotOptions: {
                pie: {
                    shadow: false
                }
            },
            tooltip: {
								useHTML: true,
                formatter: function() {
                    return '<div id="highcharts-tooltip"><b>'+ this.point.name +'</b>: '+ this.y +' % <br/> </div>';
                },
								style: {
										padding: 0
								}
            },
            series: [{
                name: 'Browsers',
                data: [["Firefox",6],["MSIE",4],["Chrome",7]],
                size: '60%',
                innerSize: '30%',
                showInLegend:false,
                dataLabels: {
                    enabled: false
                }
            }]
        });
    });