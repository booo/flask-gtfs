var onLoad = function onLoad() {
  console.log("foo");
  $.getJSON('./api/trips/20869792/stops', function(data){
    console.log(data);
  });
};
