var rangeSlider = function(){
  var slider = $('.range-slider');
  var range = $('.range-slider__range');
  var value = $('.range-slider__value');

  range.on('change', function () {
      $(this).trigger('change');
      console.log("hello!!!!!!");
  });

};

rangeSlider();
