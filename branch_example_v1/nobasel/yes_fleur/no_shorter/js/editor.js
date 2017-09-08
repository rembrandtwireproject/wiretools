// editing image via css properties
function editImage() {
	var gs = $("#gs").val(); // grayscale
	var blur = $("#blur").val(); // blur
	var br = $("#br").val(); // brightness
	var ct = $("#ct").val(); // contrast
	var opacity = $("#opacity").val(); //opacity
	var invert = $("#invert").val(); //invert
	var saturate = $("#saturate").val(); //saturate
	var sepia = $("#sepia").val(); //sepia

	$("#imageContainer img").css("filter", 'grayscale(' + gs+
													 '%) blur(' + blur +
													 'px) brightness(' + br +
													 '%) contrast(' + ct +
													 '%) opacity(' + opacity +
													 '%) invert(' + invert +
													 '%) saturate(' + saturate +
													 '%) sepia(' + sepia + '%)');

	$("#imageContainer img").css("-webkit-filter", 'grayscale(' + gs+
													 '%) blur(' + blur +
													 'px) brightness(' + br +
													 '%) contrast(' + ct +
													 '%) opacity(' + opacity +
													 '%) invert(' + invert +
													 '%) saturate(' + saturate +
													 '%) sepia(' + sepia + '%)'); 
}

//When sliders change image will be updated via editImage() function
$("input[type=range]").change(editImage).mousemove(editImage);

// Reset sliders back to their original values on press of 'reset'
$('#imageEditor').on('reset', function () {
	setTimeout(function() {
		editImage();
	},0);
});

// For Rotation: vertical
function flipv() {
   var img = $('#imageContainer img');
    if(img.hasClass('f1')){
        img.attr('class','f4');
    }
    else if(img.hasClass('f4')){
        img.attr('class','f1');
    }
    else if(img.hasClass('f3')){
        img.attr('class','f2');
    }
    else if(img.hasClass('f2')){
        img.attr('class','f3');
    } 
    else {
        img.attr('class','f4');
    }
};

// For Rotation: horizontal
function fliph() {
   var img = $('#imageContainer img');
    if(img.hasClass('f1')){
        img.attr('class','f2');
    }
    else if(img.hasClass('f2')){
        img.attr('class','f1');
    }
    else if(img.hasClass('f3')){
        img.attr('class','f4');
    }
    else if(img.hasClass('f4')){
        img.attr('class','f3');
    } 
    else {
        img.attr('class','f2');
    }
};