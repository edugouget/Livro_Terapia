<html>

<?php
$tmp = exec("python livro_terapia_py3.py", $output, $ret_code);

echo "<pre>";
print_r("===");
echo "<pre>";

echo "<pre>";
print_r($output[0]);
echo "<pre>";


$now = date("D, d M Y H:i:s T");
print_r($now);

?>

