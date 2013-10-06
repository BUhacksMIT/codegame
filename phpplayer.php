<?PHP
require("client.php");

$c = new Client("localhost", 1337);
$c->ConnectToGame();
print("max ships:".$c->max_ships);
$res = $c->InitializeShip(5, 5);
$status = $res[0];
$val = $res[1];
print($res[1]);
//$res = $c->Fire(5, 5);
//$status = $res[0];
//$val = $res[1];
//print($res[1]);
$res = $c->GetPlayerCoords();
print("x:".$res[1][0]->x);

?>