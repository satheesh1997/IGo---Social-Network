<!DOCTYPE html>
<html>
<head>
	<title>iGo - Upload Image Server</title>
</head>
<body>
	<h1>Upload a file and generate a link</h1>
	<form action="./upload.php" method="POST" enctype="multipart/form-data">
		<input type="hidden" name="MAX_FILE_SIZE" value="1000000">
		<label for="the_file">Upload a image</label>
		<input type="file" name="the_file" id="the_file">
		<input type="submit" value="Upload">
	</form>
</body>
</html>