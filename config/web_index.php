<?
 $localfile = "cache";
 if ((!file_exists($localfile)) || (((time()-filemtime($localfile))/60)>5)) {
  $contents = file_get_contents("http://www.torservers.net/anonymizer.html");
  $fp = fopen($localfile, "w");
  fwrite($fp, $contents);
  fclose($fp);
 } else {
  $contents = file_get_contents($localfile);
 }
 echo $contents;
?>

