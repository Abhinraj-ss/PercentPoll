$(document).ready(function() {
	var max_fields      = 10; 
	var wrapper   		= $(".input_fields_wrap");
	var add_button      = $(".add_field_button"); 
	
	var x = 2;
	$(add_button).click(function(e){ 
		e.preventDefault();
		if(x < max_fields){ 
			x++; 
			$(wrapper).append('<div class="form-group" id="topPad"><label for="polloption"></label><input type="text" class="form-control" name="pollOption[]" id="polloption" placeholder="Poll option" required/><a href="#" class="remove_field">Remove</a></div> ');
		}
	});
	
	$(wrapper).on("click",".remove_field", function(e){ 
		e.preventDefault(); $(this).parent('div').remove(); x--;
	})
});


function copyLink() {
 
  var copyText = document.getElementById("link");
  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */
  document.execCommand("copy");
  alert("Copied the text: " + copyText.value);
} 


var today = new Date().toISOString().split('T')[0];
document.getElementsByName("closing")[0].setAttribute('min', today);


