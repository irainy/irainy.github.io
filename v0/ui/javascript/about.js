$('document').ready(function(){



	setTimeout('animation.step_one()', 1000);

	animation = {
		step_one: function(){
			$('.left-side').animate({
				duration: 1000,
				step: function(now, fx){
					
				}
			})
		}
	}
})