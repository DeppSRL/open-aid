// JavaScript Document

var load_small_map = function(iso_code) {
    country = geojson_layer_from_alpha3(iso_code);
    if ( country ) {
        map.fitBounds(country);
        country.setStyle({fillColor: "#901800"});
        //L.marker(country.getBounds().getCenter()).addTo(map);
    } // else { if ('console' in window) { console.log("Unable to find iso_code '{{ object.iso_code }}'"); }}
    //map.removeControl(map.zoomControl);
    map.removeControl(map.attributionControl);
    info.removeFrom(map);
    legend.removeFrom(map);
    geojson.eachLayer(function(layer){ layer.removeEventListener();});
    map.dragging.disable();
};


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
            return tot > 0.0 ? (v / tot) * 360.0 : 0.0
        });
        setPieChart($(el).prop('id'), 25, 25, 20, values);
    });

    $('*[data-chart=donut]').each(function(i, el){
        SetChartDonut($(el).data('container'));
    });

    $('*[data-chart=bubble]').each(function(i, el){
        SetChartBubble($(el).data('container'));
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
        $('#myModal').modal();
        $('#myModal').on('shown.bs.modal', function(){
            $('#myModal .modal-body').html(img);
        });
        $('#myModal').on('hidden.bs.modal', function(){
            $('#myModal .modal-body').html('');
        });
    });
});
