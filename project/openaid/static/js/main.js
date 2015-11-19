// JavaScript Document

var load_small_map = function(iso_code) {
    var iso_codes = iso_code.split(",");
    for (var i = 0; i < iso_codes.length; i++) {
        country = geojson_layer_from_alpha3(iso_codes[i]);
        if ( country ) {
            map.fitBounds(country);
            country.setStyle({fillColor: "#901800"});
        }
    }

    map.removeControl(map.attributionControl);
    info.removeFrom(map);
    legend.removeFrom(map);
    geojson.eachLayer(function(layer){ layer.removeEventListener();});
    map.dragging.disable();
};

var slug = function(str) {
    var $slug = '';
    var trimmed = $.trim(str);
    $slug = trimmed.replace(/[^a-z0-9-]/gi, '-').
    replace(/-+/g, '-').
    replace(/^-|-$/g, '');
    return $slug.toLowerCase();
};

$(document).ready(function(){

    // ACCORDION LOGIC START
    //activates accordion table where needed
    // show parents row, hides child rows
    var accordion_parents =$(".accordion tr.parent");

    $(".accordion tr.child").hide();
    accordion_parents.show();


    accordion_parents.click(function(event){
        //identifies the chart
        var element_triggered=null;
        if(event.target.tagName == "SPAN"){
            element_triggered = event.target.parentElement.parentElement.id;
        }
        else if(event.target.tagName == "TD"){
            element_triggered = event.target.parentElement.id;
        }
        if(element_triggered == null || element_triggered == ''){
            console.log("element is null, tag is:"+event.target.tagName);
            return;
        }

        var id_donut = element_triggered.replace("accordion-parent-","").substring(0, 6);
        var index=$("#"+id_donut).data('highchartsChart');
        var chart=Highcharts.charts[index];

        var class_to_toggle = "#legend-"+id_donut+" tr."+element_triggered;
        // when an element is clicked
        // 1) hides children row not from the row clicked: hides open rows if there are any, but doesnt' hide the rows relative to the row that has just been clicked
        $("#legend-"+id_donut+" tr.child").not( class_to_toggle ).filter(function() {
             return $(this).css('display') == 'table-row';
        }).fadeToggle(500);

        // 2) toggles the child rows relative to this click
        $(class_to_toggle).fadeToggle(500);

        var string_to_replace = "accordion-parent-"+id_donut +"-";
        var nome_serie_da_attivare = element_triggered.replace(string_to_replace,"")+"-dd";

        // se il grafico e' gia' in drilldown prende il nome della serie attiva e fa drillup
        var nome_serie_attiva = null;
        if(chart.hasOwnProperty('drilldownLevels')){
            if(typeof chart.drilldownLevels[0]!= 'undefined'){
                nome_serie_attiva = chart.ddDupes[0];
                chart.drillUp();
            }
        }

        if(nome_serie_attiva != nome_serie_da_attivare){
            for(var i=0; i < chart.series[0].data.length; i++){
                if(chart.series[0].data[i].drilldown == nome_serie_da_attivare){
                    chart.series[0].data[i].firePointEvent('click', event);
                }
            }

        }
    });

    // ACCORDION LOGIC END


    /*cookies consent start*/
    var cookie_consent = $.cookie('cookie_consent');
    if (cookie_consent != '1') {
        $('#accept-cookies').css("display", "block");
    }

    //hides the cookie banner when the button is clicked
    $('#dismiss-cookie-adv').click(function () {
        $('#accept-cookies').toggle();
        $.cookie('cookie_consent', '1', { expires: 7, path: '/' });
    });
    /*cookies consent end*/
	
	function setPieChart(holder, x, y, radius, data)
	{
		x = x || 0;
		y = y || 0;
		radius = radius || 0;
		data = data || [];
		var r = Raphael(holder);

        var pie = r.piechart(x, y, // center
                     radius,      // radius
                     data,
                     {  init: true,
                         matchColors : true,
                         colors       : [
                                            "#f74f59",
                                            "#2b6a7c",
                                        ],

                         stroke: 'none'
                     });
        pie.rotate(-90);
	}

    $('*[data-chart=map]').each(function(i, el){
        load_small_map($(el).data('iso-code'))
    });

    $('*[data-chart=pie]').each(function(i, el){
        var tot = 0.0, values = [];
        $.each($(el).data('values').split('|'), function( index, value ) {
            value = parseFloat(value.replace(',', '.'));
            tot += value;
            values.push(parseFloat(value));
        });
        values = $.map(values, function(v){
            if (v == 0.0) {
                return 1.0;
            }
            if (v==tot){
                return 359.0;
            }
            return tot > 0.0 ? (v / tot) * 360.0 : 0.0
        });
        setPieChart($(el).prop('id'), 25, 25, 20, values);
    });

    $('*[data-chart=donut]').each(function(i, el){
        SetChartDonut($(el).data('container'));
    });

    $('*[data-chart=donut-drilldown]').each(function(i, el){
        SetChartDonutDrilldown($(el).data('container'));
    });


    $('.readmore').each(function(){
        var opener = $(this).find('.readmore-open').remove();
        var closer = $(this).find('.readmore-close').remove();
        var maxHeight = parseInt($(this).data('max-height'), 10) || 55;
        var $this = $(this);
        setTimeout(function() {
            $this.readmore({
                maxHeight: maxHeight,
                moreLink: opener,
                lessLink: closer,
                afterToggle: function (trigger, element, expanded) {
                    if (!expanded && ($(window).scrollTop() > element.offset().top)) { // The "Close" link was clicked
                        $('html, body').animate({ scrollTop: element.offset().top }, {duration: 100 });
                    }
                }
            });
        }, 100);
    });

	$('.collapse-menu a').click(function() {
		$(this).toggleClass('current');
		$(this).find('.fa').toggleClass('fa-chevron-down fa-chevron-up');
	});

    // activate popover
    // enable popovers
    $('*[data-toggle="popover"]').popover({container: 'body'});
    // close all popovers on document click
    $('body').on('click', function (e) {
        $('[data-toggle="popover"]').each(function () {
            //the 'is' for buttons that trigger popups
            //the 'has' for icons within a button that triggers a popup
            if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
                $(this).popover('hide');
            }
        });
    });

    // photo gallery
    $('.gallery li img').on('click',function(){
        var src = $(this).attr('src');
        var img = '<img src="' + src + '" class="img-responsive"/>';

        //start of new code new code
        var index = $(this).parent('li').index();

        var html = '';
        html += img;
        html += '<div style="height:25px;clear:both;display:block;">';
        html += '<a class="controls next" href="'+ (index+2) + '">next &raquo;</a>';
        html += '<a class="controls previous" href="' + (index) + '">&laquo; prev</a>';
        html += '</div>';

        $('#myModal').modal();
        $('#myModal').on('shown.bs.modal', function(){
            $('#myModal .modal-body').html(html);
            //new code
            $('a.controls').trigger('click');
        });
        $('#myModal').on('hidden.bs.modal', function(){
            $('#myModal .modal-body').html('');
        });

    });

    //new code TODO: does what???
    $(document).on('click', 'a.controls', function(){
        var index = $(this).attr('href');
        var src = $('ul.gallery li:nth-child('+ index +') img').attr('src');

        $('.modal-body img').attr('src', src);

        var newPrevIndex = parseInt(index) - 1;
        var newNextIndex = parseInt(newPrevIndex) + 2;

        if($(this).hasClass('previous')){
            $(this).attr('href', newPrevIndex);
            $('a.next').attr('href', newNextIndex);
        }else{
            $(this).attr('href', newNextIndex);
            $('a.previous').attr('href', newPrevIndex);
        }

        var total = $('ul.gallery li').length + 1;
        //hide next button
        if(total === newNextIndex){
            $('a.next').hide();
        }else{
            $('a.next').show()
        }
        //hide previous button
        if(newPrevIndex === 0){
            $('a.previous').hide();
        }else{
            $('a.previous').show()
        }


        return false;
    });

});
