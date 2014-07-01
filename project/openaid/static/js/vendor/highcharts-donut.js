// JavaScript Document

function SetChartDonut(id_donut) {
				var objs=[];	
				var total = 0;
				var number_tr = 0;
				var number_tr2 = 0;
				

				function getTooltip(element, x) {
					element.hover(
							function () {
								 chart.series[0].data[x].setState('hover');
								 chart.tooltip.refresh(chart.series[0].data[x]);
							}, 
							function () {
								 chart.series[0].data[x].setState("");
								 chart.tooltip.hide();
							}
					);
				}
		
				$("table[data-container='"+id_donut+"'] tr").each(function() {
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
				$("table[data-container='"+id_donut+"'] tr").each(function() {
						var titolo = $(this).find("*[data-title]").html();
						var valore = $(this).find("*[data-value]").html();
						
								valore = valore.replace('.', '');
								valore = valore.replace('.', '');
						
						var percent = (parseFloat(valore) * 100) / total;
percent = percent.toFixed(2).replace('.', ',');
							
						if (valore != "") {
							var single_obj = [titolo, parseFloat(percent)];
							
							objs.push(single_obj);
							number_tr2++;
						}
				});
		
								// Create the chart
								chart = new Highcharts.Chart({
										chart: {
												renderTo: id_donut,
												type: 'pie',
												width: 300,
												height: 300,
												margin: [0, 0, 0, 0]
										},
										title: {
												text: ''
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
																		return '<div id="highcharts-tooltip"><p style="text-align:left; background: #f7505a">'+ this.point.name +'</p><table><tr><td style="text-align:left;color:#f7505a;font-size:22px;padding:10px 40px 10px 10px; line-height:12px;"><strong>' + this.y + ' %</td></tr></table>';
																},
													style: {
													padding: 0,
													fontWeight: 'bold',
													borderWidth: 1,
													borderColor:'#000000',
													borderRadius:5,
													shadow:false
												},
												shared: true
																
										},
										series: [{
												name: 'Tipologie',
												data: objs,
												size: '60%',
												innerSize: '30%',
												showInLegend:false,
												dataLabels: {
														enabled: false
												}
										}]
								});

				
		function addHoverTable(element, numero_riga) {
			element.hover(
				function () {
					element.css('cursor', 'pointer');
					$("table[data-container='"+id_donut+"'] tr:nth-child("+numero_riga+")").addClass('hov');
				}, 
				function () {
					$("table[data-container='"+id_donut+"'] tr:nth-child("+numero_riga+")").removeClass('hov');
				}
			);
		}
		function bubbleClick(element, numero_riga) {
				element.on( "click", function() {
						var link = $("table[data-container='"+id_donut+"'] tr:nth-child("+numero_riga+")").find("a[href]").attr('href');
						window.location.href = link;
						//alert("test " + link);
				});
		}
		
		var numero_riga = 1;
		$("#donut1 .highcharts-series-group .highcharts-series path").each(function() {

			addHoverTable($(this), numero_riga);
			bubbleClick($(this), numero_riga);
			numero_riga++;
		});
}
