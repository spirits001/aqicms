/*
Document: app-custom.js
Author: Rustheme
Description: Write your custom code here
*/

// Below is an example of function and its initialization
var AppCustom = function() {
	var showAppName = function() {
		console.log('AppUI - Admin & Frontend template');
	};

	return {
		init: function() {
			showAppName();
		}
	}
}();

// Initialize AppCustom when page loads
jQuery(function() {
	AppCustom.init();
});

$(window).scroll(function() {
	if ($(this).scrollTop() > 100) {
		$('.back-to-top').fadeIn('slow');
	} else {
		$('.back-to-top').fadeOut('slow');
	}
});

$('.back-to-top').click(function() {
	$('html, body').animate({
		scrollTop: 0
	}, 1500, 'easeInOutExpo');
	return false;
});
