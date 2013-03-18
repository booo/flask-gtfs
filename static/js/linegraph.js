var onLoad = function onLoad() {
  console.log("foo");
  $.getJSON('./api/trips/20869792/stops', function(data){
    var stops = [];
    $.each(data.stops,
      function(){
        stops.push("<li>" + this.name + " </li>");
      }
      );
    $('<ul/>', {
      'class': 'my-new-list',
      html: stops.join('')
    }).appendTo('body');
    console.log(data);
  });
};
