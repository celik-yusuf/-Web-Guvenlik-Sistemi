<html>
 <head>
  <title>Ofis Güvenlik Sistemi</title>
 </head>
 <body>
<?php

ini_set('display_errors', 'On');
error_reporting(E_ALL|E_STRICT);
$database = new SQLite3 ('/home/pi/Desktop/zaman1.db');
   

$sql = "SELECT zaman,tarih FROM hareket";
$result = $database -> query($sql);
if (!$result) die("Cannot execute query.");
while ($row = $result -> fetcharray())
{
echo $row['zaman']." ** ".$row['tarih'];
echo "<br>";
}
$database -> close();
date_default_timezone_set('UTC');
echo "<p>Güncel Tarih ve Saat: " . date("r") . "</p>";
echo '<p style="text-align: center;">~> Gömülü Sistemler <~</p>';
?>
</body>
</html>