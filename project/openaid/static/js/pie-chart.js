// JavaScript Document

var slug = function(str) {
    var $slug = '';
    var trimmed = $.trim(str);
    $slug = trimmed.replace(/[^a-z0-9-]/gi, '-').
    replace(/-+/g, '-').
    replace(/^-|-$/g, '');
    return $slug.toLowerCase();
};

//colori del pie chart, dal più scuro al più chiaro
    var array_colori = [
        "#82040c",
        "#b40b15",
        "#ac0808",
        "#bb0a0a",
        "#d00909",
        "#ff0000",
        "#f43030",
        "#f24949",
        "#f05757",
        "#f74f59",
        "#f74f59",
    ];


function SetChartDonutDrilldown(id_donut){
    var objs=[];
    var drilldown=[];
    var total = 0;
    var number_tr = 0;
    var number_tr2 = 0;
    var chart;
    var array_valori_no_ripetuti = [];
    var cont_colori=0;

    var table_parent_tr = $("table[data-container='"+id_donut+"'] tr.parent");

    table_parent_tr.each(function() {

        function getTooltip(element, x)
        {
            element.hover(
                function () {
                    if(typeof chart.series[0].data[x]!= 'undefined' ){
                        chart.series[0].data[x].setState('hover');
                        chart.tooltip.refresh(chart.series[0].data[x]);
                    }

                },
                function () {
                    if(typeof chart.series[0].data[x]!= 'undefined' ){
                        chart.series[0].data[x].setState("");
                        chart.tooltip.hide();
                    }
                }
            );
        }

        //calcolo somma totale
        var valore = $(this).find("*[data-value]").data('value');

        if (valore != "") {
            //gestione tooltip
            getTooltip($(this), number_tr);

            total = total + parseFloat(valore);
            number_tr++;
        }
    });

    //prelevo i dati dalla tabella e creo l'array
    table_parent_tr.each(function() {
        var parent_name = $(this).find("*[data-title]").data('title');
        var parent_value = $(this).find("*[data-value]").data('value');
        var parent_percent = (parseFloat(parent_value) * 100) / total;
        parent_percent = parseFloat(parent_percent.toFixed(2));

        if (parent_value != "") {
            //ricavo i valori della tabella senza ripetizioni (per la gestione dei colori)
            if(jQuery.inArray(parent_value, array_valori_no_ripetuti) == -1) {
                array_valori_no_ripetuti.push(parent_value);
                cont_colori++;
            }

            var obj_dict = {y:parent_percent, name:parent_name, drilldown:null};
            number_tr2++;

            // look for children
            var drilldown_name = slug(parent_name+"-dd");
            var drill_obj = {name: parent_name, id:drilldown_name, data:[]};

            $(this).nextUntil('tr.parent').each(
                function(){
                    var child_name = $(this).find("*[data-title]").data('title');
                    var child_value = $(this).find("*[data-value]").data('value');
                    var child_percent = (parseFloat(child_value) * 100) / parseFloat(parent_value);
                    child_percent = parseFloat(child_percent.toFixed(2));
                    drill_obj.data.push([child_name, child_percent]);
                }
            );
            if(drill_obj.data.length > 0 ){
                drilldown.push(drill_obj);
                obj_dict.drilldown = drilldown_name;
            }
            objs.push(obj_dict);

        }
    });

    // Create the chart
     Highcharts.setOptions({
        colors: array_colori
    });
    Highcharts.setOptions({
        lang: {
            drillUpText: '◁'
        }
    });
    chart = new Highcharts.Chart({
        chart: {
            renderTo: id_donut,
            type: 'pie',
            width: 300,
            height: 300,
            margin: [0, 0, 0, 0],
            events:{
                drillup: function(){
                     //hides child elements of legend if they are opened
                     $("#legend-"+id_donut+" tr.child").hide(500);
                },
                drilldown:function(){
                     console.log("expand accordion");
                }
            }
        },
        title: {text: ''},
        legend: {enabled: false},
        credits: { enabled: false},
        exporting: {enabled: false},
        plotOptions: {
            pie: {
                shadow: false
            },
            series: {
                dataLabels: {
                    enabled: false,
                    format: '{point.name}: {point.y:.1f}%'
                }
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
            showInLegend:false
        }],
        drilldown:{
            series: drilldown
        }

    });

}

function SetChartDonut(id_donut) {
    var objs=[];
    var total = 0;
    var number_tr = 0;
    var number_tr2 = 0;
    var chart;
    var array_valori_no_ripetuti = [];
    var cont_colori=0;

    var table_tr = $("table[data-container='"+id_donut+"'] tr");

    table_tr.each(function() {

        function getTooltip(element, x)
        {
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


        //calcolo somma totale
        var valore = $(this).find("*[data-value]").data('value');

        if (valore != "") {
            //gestione tooltip
            getTooltip($(this), number_tr);

            total = total + parseFloat(valore);
            number_tr++;
        }
    });

    //prelevo i dati dalla tabella e creo l'array
    table_tr.each(function() {
        var titolo = $(this).find("*[data-title]").data('title');
        var valore = $(this).find("*[data-value]").data('value');

        var percent = (parseFloat(valore) * 100) / total;
        percent = percent.toFixed(2);

        if (valore != "") {

            //ricavo i valori della tabella senza ripetizioni (per la gestione dei colori)
            if(jQuery.inArray(valore, array_valori_no_ripetuti) == -1) {
                array_valori_no_ripetuti.push(valore);
                var colore = array_colori[cont_colori];
                cont_colori++;
            }

            var single_obj = {y: parseFloat(percent), name:titolo, color: colore};

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

}
