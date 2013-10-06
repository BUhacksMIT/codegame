<?PHP
set_time_limit(0);

class Ship {
    var $x;
    var $y;
    var $alive;
    var $shipid;
    var $player;
    var $health;

    function __construct($x, $y, $alive, $shipid, $player, $health) {
        $this->x = $x;
        $this->y = $y;
        $this->alive = $alive;
        $this->shipid = $shipid;
        $this->player = $player;
        $this->health = $health;
    }
}

class Opcodes
{
    const initialize_ship = 1;
    const get_player_coords = 2;
    const choose_lang = 3;
    const move = 4;
    const get_delay = 5;
    const fire = 6;
    const get_my_alive_ships = 7;
    const get_game_status = 8;
}

class langs {
    const Python = 1;
    const PHP = 2;
    const Nolang = -1;
}

class Client {

    var $ip;
    var $port;
    var $game_started;
    var $s;

    function __construct($ip, $port) {
        $this->ip = $ip;
        $this->port = $port;
        $this->game_started = false;
    }

    private function SendCommand() {
        $args = func_get_args();
        $n = func_num_args();
        $opcode = intval($args[0]);
        $message = $opcode.",";
        for ($i=1; $i<$n; $i++) {
            $message .= $args[$i].",";
        }
        //die("value of opcode is ".$message);
      //  socket_write($this->s, $message, strlen($message));
        fputs($this->s, $message);
        //do {
        //    $line = fgets($this->s, 4096);
        //} while($line == '');
           /// while ( ( $buf = @socket_read( $this->s, 4, PHP_BINARY_READ ) ) === false  && strlen($buf) < 1) {
                //nothing

/*die("b:".$buf);
        while (1==1) {
    $header = fread($this->s, 4);
    print("d".$header);
    sleep(1);
}
    $len = $this->bytesToInt( $header );
    die("length:".$len);
    $message = unserialize( fread( $this->s, $len ) );
    die("msg".$message);*/
      //  $full = "";
       // while (strlen($full) < 5) {
       //     socket_recv($socket, $buf, 1, MSG_WAITALL);
        //    $full .= $buf;
       //     print($full);
       // }
        //die("bytes".$full);
    //}
//die();
    /*
while ($bytes == '') {
        $bytes = socket_recv($socket, $buf, 2048, MSG_WAITALL);
}
        print ("resp:".$bytes);
        return $bytes;*/
     //   while (!feof($fp)) {
        $h =fgets($this->s, 5);
        //print("h:".$h);
        $h = $this->bytesToInt($h);
        $d = fgets($this->s, $h+1);
        //print("returning ".$d);
        $d = explode(";", $d, 2);
        //print("\r\nd1:".$d[1].":".$d[1].substr(1,1).":".$d[1].substr(1,1)."\r\n");
        if (substr($d[1], 0, 1) == "[") {
            if (substr($d[1], 1, 1) == "(") {
                print ("special print");
                $vals = str_replace(" ", "", explode("),", str_replace("]", "", str_replace("[", "", $d[1]))));
                foreach ($vals as $s) {
                    $subvals = explode(",", str_replace(" ", "", str_replace("(", "", str_replace(")", "", $s))));
                    $x = intval($subvals[0]);
                    print("got x = ".$x);
                    $y = intval($subvals[1]);
                    $alive = $subvals[2] == "True" ? true : false;
                    $shipid= intval($subvals[3]);
                    $player = intval($subvals[4]);
                    $health = intval($subvals[5]);
                    $so = new Ship($x, $y, $alive, $shipid, $player, $health);
                    print("so:".$so);
                    $sos[] = $so;
                }
                $d[1] = $sos;
            } else {
                $vals = explode(",", str_replace(" ", "", str_replace("]", "", str_replace("[", "", $d[1]))));
                $d[1] = $vals;
            }
        } else if ($d[1].substr(0) == "(") {
            $vals = explode(",", str_replace(" ", "", str_replace("(", "", str_replace(")", "", $d[1]))));
            $d[1] = $vals;
        }
        return $d;
   // } 
        
    }

    public function bytesToInt($char) {
$num = ord($char[3]);
$num |= ord($char[2]) << 8;
$num |= ord($char[1]) << 16;
$num |= ord($char[0]) << 24;
return $num;
}
    function InitializeShip($x, $y) {
        print("init ship");
        return $this->SendCommand(Opcodes::initialize_ship, $x, $y);
    }

    function GetPlayerCoords() {
        $response = $this->SendCommand(Opcodes::get_player_coords);
        print("res:".$response);
        return $response;
    }

    function Move($shipid, $direction) {
        return $this->SendCommand(Opcodes::move, $shipid, $direction);
    }

    function GetMyDelay() {
        return $this->SendCommand(Opcodes::get_delay);
    }

    function Fire($shipid, $to_x, $to_y) {
        return $this->SendCommand(Opcodes::fire, $shipid, $to_x, $to_y);
    }

    function GetMyAliveShips() {
        return $this->SendCommand(Opcodes::get_my_alive_ships);
    }

    private function GetGameStatus() {
        return $this->SendCommand(Opcodes::get_game_status);
    }

    function ConnectToGame() {
      //  $this->s = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
       // socket_set_nonblock( $this->s );
        $this->s = pfsockopen($this->ip, $this->port);
        if (!$this->s) { 
            die("Error connecting to server");
        }
        //$result = socket_connect($this->s, $this->ip, $this->port);
       /* if (!$result) {
                $errorcode = socket_last_error();
    $errormsg = socket_strerror($errorcode);
            die("Error connecting".$errormsg);
      }*/
        $this->SendCommand(Opcodes::choose_lang, langs::PHP);
        while ($this->game_started == false) {
            $result = $this->GetGameStatus();
            sleep(1);
            $rescode = $result[0];
            $resval = $result[1];
            if ($resval[0] == true) {
                $this->board_width = intval($resval[1]);
                $this->board_height = intval($resval[2]);
                $this->max_range = intval($resval[3]);
                $this->max_ships = intval($resval[4]);
                $this->game_started = true;
                print("Game started!");
                return true;
            }
        }
    }
    
    function __destruct() {
        socket_close($this->s);
    }
}

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