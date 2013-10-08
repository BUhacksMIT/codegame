<?PHP
require("client.php");

$c = new Client("169.254.115.63", 1337);
$c->ConnectToGame();

for ($i = 0; $i < $c->max_ships; $i++) {
    $added = false;
    $offset = 0;
    while ($added == false) {
        $x = rand(0, $c->board_width-1)+$offset;
        $y = rand(0, intval(($c->board_height-1)/2))+$offset;
        print("init ship at ".$x.",".$y."\r\n");
        $res = $c->InitializeShip($x, $y);
        print("init gave".$res[0]." and ".$res[1]."\r\n");
        if ($res[0] == resultcodes::success) {
            $myships[] = $res[1];
            $mycoords[] = array($x, $y);
            $added = true;
            print ("added ship to ".$x. ",".$y."\r\n");
        } else {
            $added = false;
            $offset = rand(-3, 3);
            print ("error adding ship\r\n");
        }
    }
}

$i = 0;
$k = 0;
while (1==1) {
    print("getting delay\r\n");
    $ret = $c->GetMyDelay();
    if ($ret[1] > 0) {
        print("I can't move for another ".$ret[1]." ticks!\r\n");
    }
    print("delay is ".$ret[1]." with code ".$ret[0]."\r\n");
    if ($k % 2==0) {
        $fx = ($mycoords[$i % count($mycoords)][0]+rand(-5, 5)) % 20;
        $fy = ($mycoords[$i % count($mycoords)][1]+rand(-5, 5)) % 20;
        print("fire  ".$i." to ".$fx.",".$fy);
        $res = $c->Fire($myships[$i % count($myships)], $fx, $fy);
        print("fire  ".$i." to ".$fx.",".$fy." with result ".$res[0]." and value ".$res[1]."\r\n");
        print("\r\nfired\r\n");
    } else {
        $sid = $i % count($myships);
        $res = $c->Move($myships[$sid], 1);
        print("move  ".$i." to random dir with result ".$res[0]." and value ".$res[1]."\r\n");
        if ($res[0] == 1) {
            $mycoords[$sid][1] += 1;
        }
    }
    $k += 1;
    $i += 1;
    sleep(0.1);
}
?>