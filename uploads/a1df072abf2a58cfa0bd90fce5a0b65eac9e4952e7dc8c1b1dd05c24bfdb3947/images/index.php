<?php
	$dir = dir("./");
	while(false !== ($file = $dir->read())){
		if($file != '.' && $file != '..' && $file != 'index.php'){
			echo "<img src='./".$file."' style='height:150px;width:150px;padding:50px;' />";
		}
	}
	$dir->close();
?>