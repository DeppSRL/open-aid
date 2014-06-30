// JavaScript Document

var chart = new Highcharts.Chart({
		chart: {
					renderTo: 'highcharts-bubble2',
					type: 'bubble',
					width: 300,
					height: 300,
					margin: [0, 0, 0, 0]
		},
	
		title: {
					text: false
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
		tooltip: {
			enabled:true,
			backgroundColor: '#FFFFFF',
			borderWidth:0,
			borderRadius:3,
			style: {
				color: '#333333',
				fontSize: '12px',
				padding: '8px',
				zIndex: '100'
			},
			formatter: function(){
			var fontName='Benton Sans Condensed';
				var fontSize = 12;
				
				var labelTemplate='Example text 1'+'<br/>'+'Row example '+this.point.cnt+'</tspan>';
				return labelTemplate;
			}
		},
		plotOptions: {
				series: {
					shadow: false,
					borderWidth: 0,
					marker: {
						lineColor: 'rgba(200,200,200,1)',
						lineWidth: 1,
						fillOpacity: 1
					}
				},
			bubble: {
				minSize: 30,
				maxSize: 100
			}
    },
		xAxis: {
        min: 0,
        max: 200,
        lineWidth: 1,
        gridLineWidth: 0,
        title: {
            text: ''
        },
        labels: {
            enabled: false
        }
    },
    yAxis: {
		min: 0,
        max: 200,
        gridLineWidth: 0,
        title: {
            text: ''
        },
        labels: {
            enabled: false
        }
    },
		
		
		series: [
		{
			name: 'My test with very very long name >',
            data: [
                {x:90, y:100,z:170, cnt:1233}
            ],
			color: '#A1B1C1',
			marker: {
				states: {
					select: {
						fillColor: '#A2B2C2',
						fillOpacity: 1,
						lineWidth: 1,
						lineColor: 'black' //'#9B9B9B'
					}
				}
      }

    },

		{
			name: 'My test with long name',
            data: [
                {x:150,y:125,z:100, cnt:890}
            ],
			color: '#C11102',
			marker: {
				states: {
					select: {
						fillColor: '#B10801',
						fillOpacity: 1,
						lineWidth: 1,
						lineColor: 'black'
					}
				}
      }
    },
		
		{
			name: 'My test 222',
            data: [
                {x:70,y:25,z:10, cnt:'testo'}
            ],
			color: '#C11102',
			marker: {
				states: {
					select: {
						fillColor: '#B10801',
						fillOpacity: 1,
						lineWidth: 1,
						lineColor: 'black'
					}
				}
      }
    }
	]
});