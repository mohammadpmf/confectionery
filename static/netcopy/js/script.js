(function($){
"use strict";

/*========== Loader start ================*/
$(window).on('load', function() {
	$('#loader-wrapper').fadeIn();
	setTimeout(function() {
		$('#loader-wrapper').fadeOut();
	}, 500);
});
document.addEventListener('contextmenu', function(e) {
  e.preventDefault();
});
document.onkeydown = function(e) {
  if(event.keyCode == 123) {
     return false;
  }
  if(e.ctrlKey && e.shiftKey && e.keyCode == 'I'.charCodeAt(0)) {
     return false;
  }
  if(e.ctrlKey && e.shiftKey && e.keyCode == 'C'.charCodeAt(0)) {
     return false;
  }
  if(e.ctrlKey && e.shiftKey && e.keyCode == 'J'.charCodeAt(0)) {
     return false;
  }
  if(e.ctrlKey && e.keyCode == 'U'.charCodeAt(0)) {
     return false;
  }
}
})(jQuery);