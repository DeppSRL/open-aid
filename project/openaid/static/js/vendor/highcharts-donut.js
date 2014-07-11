// JavaScript Document

function SetChartDonut(id_donut) {
    var objs=[];
    var total = 0;
    var number_tr = 0;
    var number_tr2 = 0;
    var chart;
    var array_valori_no_ripetuti = [];
    //dal più scuro al più chiaro
    var array_colori = ["#82040c", "#b40b15", "#ac0808", "#bb0a0a", "#d00909", "#ff0000", "#f43030", "#f24949", "#f05757", "#f74f59"];
    var cont_colori=0;


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
        var valore = $(this).find("*[data-value]").data('value');

//        valore = valore.replace(/\./g, '');

        if (valore != "") {
            //gestione tooltip
            getTooltip($(this), number_tr);

            total = total + parseInt(valore);
            number_tr++;
            //console.log(id_donut, 'Tot', total, number_tr);
        }
    });

    //prelevo i dati dalla tabella e creo l'array
    $("table[data-container='"+id_donut+"'] tr").each(function() {
        var titolo = $(this).find("*[data-title]").data('title');
        var valore = $(this).find("*[data-value]").data('value');

//        valore = valore.replace(/\./g, '');

        var percent = (parseFloat(valore) * 100) / total;
        percent = percent.toFixed(2);

        if (valore != "") {

            //ricavo i valori della tabella senza ripetizioni (per la gestione dei colori)
            if(jQuery.inArray(valore, array_valori_no_ripetuti) == -1) {
                array_valori_no_ripetuti.push(valore);
                colore = array_colori[cont_colori];
                cont_colori++;
            }

            var single_obj = {y: parseFloat(percent), name:titolo, color: colore};

            objs.push(single_obj);
            number_tr2++;
            //console.log(id_donut, '%', percent, number_tr2);
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
