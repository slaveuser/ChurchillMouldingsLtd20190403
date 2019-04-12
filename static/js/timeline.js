window.onload = function() {
	$('.dot:nth-child(1)').click(function(){
		markComplete(1);
		$('.inside').animate({
			'width' : '20%'
		}, 500);
	});
	$('.dot:nth-child(2)').click(function(){
		markComplete(2);
		$('.inside').animate({
				'width' : '40%'
			}, 500);
	});
	$('.dot:nth-child(3)').click(function(){
		markComplete(3);
		$('.inside').animate({
				'width' : '60%'
			}, 500);
	});
	$('.dot:nth-child(4)').click(function(){
		markComplete(4);
		$('.inside').animate({
				'width' : '80%'
			}, 500);
	});
	$('.dot:nth-child(5)').click(function(){
		markComplete(5);
		$('.inside').animate({
				'width' : '90%'
			}, 500);
	});
	$('.dot:nth-child(6)').click(function(){
		markComplete(6);
		$('.inside').animate({
				'width' : '90%'
			}, 500);
	});

	$('.modal').unwrap('<div class="mask"></div>');
	$('.modal').hide();
	$('.modal').addClass('nobox');
	$('.dot').click(function(){
		var modal = $(this).attr('id');
		$('article.nobox').hide()
		$('article.nobox.' + modal).fadeIn(200)
	});

}

function markComplete(n){
	for (var i = 1; i <= 6; i++) {
		if (i <= n) {
			$('.dot:nth-child('+i+')').removeClass('red');
			$('.dot:nth-child('+i+')').addClass('green');
		} else {
			$('.dot:nth-child('+i+')').removeClass('green');
			$('.dot:nth-child('+i+')').removeClass('red');
		}
	}
	//make next milestone red
	$('.dot:nth-child('+(n+1)+')').addClass('red');
	//if complete make tick img green
	if (n==5||n==6) {
		$('#tick').attr('src', '../static/images/tick.png');
   		} else {
		$('#tick').attr('src', '../static/images/untick.png');
	}
}