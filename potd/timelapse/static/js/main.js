$(document).ready(function () {
	$('#fullpage').fullpage({
		fixedElements: '.overlay, .header',
		continuousVertical: true,
		slidesNavigation: true,
	    slidesNavPosition: 'bottom',
	    scrollingSpeed: 400,
	    scrollOverflow: true
	});

	$('#nav').click(function() {
		$('.overlay').toggleClass('hidden');
		$(this).find('i').toggleClass('fa-bars fa-close')
	});

	$("img.lazy").lazyload({
		container: $("#fullpage"),
		effect : "fadeIn",
		event : "mouseover"

	});
});