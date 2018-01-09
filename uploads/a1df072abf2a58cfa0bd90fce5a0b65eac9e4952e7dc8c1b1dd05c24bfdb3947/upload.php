<?php
	header('Content-type: application/json');
	header("Access-Control-Allow-Origin: *");
	$result = [];
	$url = 'http://localhost/uploads/a1df072abf2a58cfa0bd90fce5a0b65eac9e4952e7dc8c1b1dd05c24bfdb3947/images/';

	if ($_FILES['the_file']['error'] > 0){
		switch ($_FILES['the_file']['error']) {
			case 1:
				$result['error'] = 'Upload maximum file size exceeded';
				break;

			case 2:
				$result['error'] = 'Maximun file size exceeded';
				break;

			case 3:
				$result['error'] = 'File not fully uploaded';
				break;

			case 4:
				$result['error'] = 'Select a file to upload';
				break;

			case 6:
				$result['error'] = 'No temp dir specified';
				break;

			case 7:
				$result['error'] = 'Writing to disk failed';
				break;

			case 8:
				$result['error'] = 'Extension is blocking file upload';
				break;

		}
		echo json_encode($result, JSON_PRETTY_PRINT);
		exit();
	}

	if($_FILES['the_file']['type'] != 'image/jpeg'){
		$result['error'] = 'only jpeg files are allowed';
		$result['file_type'] = $_FILES['the_file']['type'];
		echo json_encode($result, JSON_PRETTY_PRINT);
		exit();
	}

	$upload_path = './images/'.md5($_FILES['the_file']['name'].time()).'.jpg';

	if(is_uploaded_file($_FILES['the_file']['tmp_name'])){
		if(!move_uploaded_file($_FILES['the_file']['tmp_name'], $upload_path)){
			$result['error'] = 'could not move file to the dir';
			echo json_encode($result, JSON_PRETTY_PRINT);
			exit();
		}
	}
	else{
		$result['error'] = 'file attack detected : '.$_FILES['the_file']['name'];
		echo json_encode($result, JSON_PRETTY_PRINT);
		exit();
	}

	$result['status'] = 'uploaded_successfully';
	$result['name'] = $_FILES['the_file']['name'];
	$result['new_name'] = md5($_FILES['the_file']['name'].time()).'.jpg';
	$result['link'] = $url.$result['new_name'];
	echo json_encode($result, JSON_PRETTY_PRINT);

?>