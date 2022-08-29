<?php

    require __DIR__ . '/vendor/autoload.php';
    use PhpMqtt\Client\Exceptions\ConnectingToBrokerFailedException;
    use PhpMqtt\Client\Exceptions\DataTransferException;
    use PhpMqtt\Client\Exceptions\UnexpectedAcknowledgementException;
    use PhpMqtt\Client\MQTTClient;
    use Psr\Log\LogLevel;

    function publish_MQTT($server, $port, $topic){

        $mqtt = new MQTTClient($server, $port, null);
        $mqtt->connect();
        $mqtt->publish($topic, 'Check', 1);
        $mqtt->close();
    }

    function connectToDB() {
        $servername = "127.0.0.1";
        $username = "root";
        $password = "DavideMacbook1996";

        $conn = new PDO("mysql:host=$servername;dbname=networkMonitoring", $username, $password);

        // Set the PDO error mode to exception
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        return $conn;
    }

    function retrieveHost(){
        $hostInArray= array();
        $connection = connectToDB();

        $QUERY = "SELECT * FROM `hostSeen`";
        $statement = $connection->prepare($QUERY);
        $statement->execute(); 
        $resultFromStatement = $statement->fetchAll();
        foreach($resultFromStatement as $row){
            array_push($hostInArray, $row["MacAddress"]);
        }

        return $hostInArray;
    }

    function showHost($hostInArray){
        if(sizeof($hostInArray) > 0) {
            echo'
                <p> <b> Select specified host to check: </b> </p>
                <div id="formHost">
                <input type="hidden" id="checkOneHost" name="checkOneHost" value="checkOneHost">
            ';

            for ($i = 0; $i < sizeof($hostInArray); $i++) {
                echo '
                    <input type="radio" id="'.strval($i).'" name="host" value="'.$hostInArray[$i].'">
                    <label for="'.strval($i).'">'.$hostInArray[$i].' </label>
                ';
            }
            echo '</div>';
        }
        else {
            echo '<h1> There are no host to contact </h1>';
        }
    }

    function showCheckAllHosts($hostInArray){
        if(sizeof($hostInArray) > 0){
            echo '
                <form name="dataRequest" method="POST" action="panelControl.php">
                    <input type="hidden" id="sendToAll" name="sendToAll" value="sendToAll">
                    <p> <b> Tap "check all" to verify the status of all hosts seen </b> </p>
                    <input type="submit" class="btn btn-outline-info" value="Check all">
                </form>
            ';
        }
        else{
            echo '
                <p> There are no hosts! </p>
            ';
        }
    }
?>