<?php
    //echo file_put_contents("/home/corentin/Documents/phptest/gpsdata.txt","Hello World. Testing!");
    $Longitude = $_POST['Xcoordinates'];
    $Lattitude = $_POST['Ycoordinates'];
    $file ="/home/pi/Documents/gpsdata.txt";
    $old_content=file_get_contents($file);
    file_put_contents($file, "[".$Longitude.", ".$Lattitude."]\n".$old_content);

    readfile('coord.html');
?>
