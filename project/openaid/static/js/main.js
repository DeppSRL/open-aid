// JavaScript Document




$(document).ready(function(){
	
	function setPieChart(holder, x, y, radius, data)
	{
		x = x || 0;
		y = y || 0;
		radius = radius || 0;
		data = data || [];
	
		var r = Raphael(holder),
			pie = r.piechart(x, y, radius, data, {init: true, colors:['#f74f59', '#2b6a7c'], stroke: 'none'});
		pie.rotate(225);
	}

    $('*[data-chart=pie]').each(function(i, el){
        setPieChart($(el).prop('id'), 25, 25, 20, [270, 90]);
    });

    $('*[data-chart=donut]').each(function(i, el){
       // Create the chart
        chart = new Highcharts.Chart({
            chart: {
                renderTo: $(el).prop('id'),
                type: 'pie',
                width: 300,
                height: 300,
                margin: [0, 0, 0, 0]
            },
            title: {
                text: 'Browser market share, April, 2011'
            },
            legend: { enabled: false },
            credits: { enabled: false },
            exporting: { enabled: false },
            yAxis: {
                title: {
                    text: 'Total percent market share'
                }
            },
            plotOptions: {
                pie: { shadow: false }
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

	$('.collapse-menu a').click(function() {
		$(this).toggleClass('current');
		$(this).find('.fa').toggleClass('fa-chevron-down fa-chevron-up');
	});

    // activate popover
    $('a[rel=info-popover]').popover();
});
