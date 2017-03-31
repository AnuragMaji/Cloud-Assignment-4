$(function () {

  $('#Datebutton').on('click', function() {
   var Dateentered = document.getElementById("Text").value;
   $.ajax({
    type: 'GET',
    url: '/forecast/'+ Dateentered,
    success: function(data) {
      var datelist = [];
      for(var i=0; i<6; i++) {
      	x = {};
      	x.label = data[i].DATE;
      	x.y = [];
      	x.y.push(data[i].TMIN);
      	x.y.push(data[i].TMAX);
        datelist.push(x);
      }

      var chart = new CanvasJS.Chart("chartContainer",{
		title:{
			text: "Weather Forecasting Application",
		},
		axisY: {
			includeZero: false,
			suffix: "°F",
			maximum: 100,
			gridThickness: 0
		},
		toolTip:{
			shared: true,
			content: "<br> <strong>Temperature: </strong> </br> Min: {y[0]}°F, Max: {y[1]}°F",
		},
		data: [
		{
			type: "rangeSplineArea",
			fillOpacity: 0,
			color: "#91AAB1",
			dataPoints: datelist
		}]
	});
	chart.render();
    }

  });
  });

});