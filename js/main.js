$(document).ready(function() {
	$(window).scroll(function(){
        if ($(this).scrollTop() > 200) {
            $('.scroll-up').fadeIn();
        } else {
            $('.scroll-up').fadeOut();
        }
    });
    $('.scroll-up').click(function(){
    	$("html, body").animate({ scrollTop: 0 }, 500);
    	return false;
    });
})
