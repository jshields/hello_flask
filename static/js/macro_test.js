(function($) {
  $(document).ready(function() {
    $('#nested-wrapper').append($('<pre></pre>').text('Got this data from jQuery:' + JSON.stringify($('#nested-wrapper button').data())));
  });
})(jQuery);
