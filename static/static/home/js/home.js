$(document).ready(function () {
	$('#feed_up_btn').click(function(){
		var loading_btn = '<span class="fa fa-refresh fa-spin"></span>';
		var normal_btn = 'Publish';
		$(this).html(loading_btn);
		if($('#say_something').val() == "" || $('#say_something').val().length < 10){
			$('#form-error').html('Empty Feed');
			$(this).html(normal_btn);
			return false;
		}
		if($('#upload_pic').val() != "" && $('#upload_video').val() != ""){
			$('#form-error').html('Choose Video / Image');
			$(this).html(normal_btn);
			return false;
		}
		$(this).attr('disabled', 'disabled');
		$('#feed_form').submit();
    });
});

var d_link = "";

$("#up_img_btn").on("change", function(){
    console.log('Image added');
    var formData = new FormData();
    formData.append('the_file', $('#up_img_btn')[0].files[0]);
    $.ajax({
       url : 'http://techtrendz.in/uploads/a1df072abf2a58cfa0bd90fce5a0b65eac9e4952e7dc8c1b1dd05c24bfdb3947/upload.php',
       type : 'POST',
       data : formData,
       processData: false,  // tell jQuery not to process the data
       contentType: false,  // tell jQuery not to set contentType
       success : function(data) {
            if(data.status == "uploaded_successfully"){
                $("#upload_pic").val(data.link);
                d_link=data.link;
                $('#up_img').show();
                $('#up_img').attr('src', data.link);
            }
            else{
                alert("Image Upload Failed -> "+ data.error);
                console.log(data);
               $("#upload_pic").val('');
            }
       }
    });
});