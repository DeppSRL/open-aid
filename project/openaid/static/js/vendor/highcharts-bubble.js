

function SetChartBubble(id_bubble) {
		// JavaScript Document
		var objs=[];	
		var x = 90;
		var y = 100;
		var z = 120;
		var total = 0;
		var number_tr = 0;
		var number_tr2 = 0;
		var points = [{x:40, y:40}, {x:40, y:100}, {x:40, y:160},
									{x:100, y:40}, {x:100, y:100}, {x:100, y:160},
									{x:160, y:40}, {x:160, y:100}, {x:160, y:160},
		];

		function randomIntFromInterval(min,max) {
				return Math.floor(Math.random()*(max-min+1)+min);
		}
		
		function getTooltip(element, x) {
			element.hover(
					function () {
						 chart.series[x].data[0].setState('hover');
						 chart.tooltip.refresh(chart.series[x].data[0]);
					}, 
					function () {
					   chart.series[x].data[0].setState("");
						 chart.tooltip.hide();
					}
			);
		}
		
		$("table[data-container='"+id_bubble+"'] tr").each(function() {
				//calcolo somma totale
				var valore = $(this).find("*[data-value]").html();
				
				valore = valore.replace('.', '');
				valore = valore.replace('.', '');

				if (valore != "") {
						//gestione tooltip
						getTooltip($(this), number_tr);
						
						total = total + parseInt(valore);
						number_tr++;
				}
		});
		
		//prelevo i dati dalla tabella e creo l'array
		$("table[data-container='"+id_bubble+"'] tr").each(function() {
				var titolo = $(this).find("*[data-title]").html();
				var valore = $(this).find("*[data-value]").html();
				var percent = (parseInt(valore) * 100) / total;
				
				if (valore != "") {
					x= points[number_tr2].x;
					y= points[number_tr2].y;
					z= z;
					
					var single_obj = {
						name: titolo,
						data: [
								{x:x, y:y, z:z + percent, numb:valore, type:titolo}
						],
						color: '#A1B1C1',
						marker: {
							states: {
								select: {
									fillColor: '#f7505a',
									fillOpacity: 1,
									lineWidth: 1,
									lineColor: '#000'
								}
							}
						}
					}
				
					objs.push(single_obj);
					number_tr2++;
				}
		});

		
		
		
		
		var chart = new Highcharts.Chart({
				chart: {
					renderTo: id_bubble,
					type: 'bubble',
					width: 300,
					height: 300,
					margin: [0, 0, 0, 0]
				},
			
				title: {
				text: ' '
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
					style: {
						padding: 0,
						fontWeight: 'bold',
						borderWidth: 1,
						borderColor:'#000000',
						borderRadius:5,
						shadow:false
								},
								shared: true,
								useHTML: true,
								headerFormat: '<p style="text-align:left; background: {series.color}">{series.name}</p><table>',
								pointFormat: '<tr><td style="text-align:left;color:{series.color};font-size:22px;padding:10px 40px 10px 10px; line-height:12px;"><strong>€ {point.numb}</strong></td></tr>',
								footerFormat: '</table>',
								valueDecimals: 2
						},
				plotOptions: {
						series: {
							shadow: false,
							borderWidth: 1,
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
				
				
				series: objs
		});
		
		
		
		function addHoverTable(element, numero_riga) {
			element.hover(
				function () {
					element.css('cursor', 'pointer');
					$("table[data-container='"+id_bubble+"'] tr:nth-child("+numero_riga+")").addClass('hov');
				}, 
				function () {
					$("table[data-container='"+id_bubble+"'] tr:nth-child("+numero_riga+")").removeClass('hov');
				}
			);
		}
		function bubbleClick(element, numero_riga) {
				element.on( "click", function() {
						var link = $("table[data-container='"+id_bubble+"'] tr:nth-child("+numero_riga+")").find("a[href]").attr('href');
						window.location.href = link;
						//alert("test " + link);
				});
		}
		
		var numero_riga = 1;
		$("#"+id_bubble+" .highcharts-series-group .highcharts-series").each(function() {
			addHoverTable($(this), numero_riga);
			bubbleClick($(this), numero_riga);
			numero_riga++;
		});

}









