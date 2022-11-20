$(document).ready(function () {
	var count = 1
	var fileTypes = ['jpg', 'jpeg', 'png'];  //acceptable file types
	$("input:file").change(function (evt) {
	    var parentEl = $(this).parent();
	    var tgt = evt.target || window.event.srcElement,
	                    files = tgt.files;

	    // FileReader support
	    if (FileReader && files && files.length) {
	        var fr = new FileReader();
	        var extension = files[0].name.split('.').pop().toLowerCase(); 
	        fr.onload = function (e) {
	        	success = fileTypes.indexOf(extension) > -1;
	        	if(success)
	        	if (count == 1) {
		        	$(parentEl).append('<img src="' + fr.result + '" class="preview" width="500px" height="250px" />');
	        } else if (count > 1) {
	            $("img.preview").replaceWith('<img src="' + fr.result + '" class="preview" width="500px" height="250px" />');}
	        }
	        fr.onloadend = function(e){
	            count += 1
	            console.debug("Load End");
	        }
	        fr.readAsDataURL(files[0]);
	    }
	});
});
