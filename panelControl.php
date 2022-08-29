<?php 
    require_once 'functionPHP.php';

    //Check if is required a check on host in the network
    if(isset($_POST["sendToAll"])){
        publish_MQTT("test.mosquitto.org", 1883, "checkFromWebServer/all");
    }
    //Else check if is the case in which want to check 1 host on the network
    else if(isset($_POST["checkOneHost"])){
        publish_MQTT("test.mosquitto.org", 1883, "checkFromWebServer/".$_POST["host"]);
    }
?>

<html>
    <head>
        <title> Panel Control </title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script> 
        <link rel="stylesheet" href="panelControl.css"> 
    </head>
    <body>

        <!-- Page container start -->
        <div class="container-xl"></div>

            <!-- Header -->
            <h1 id="pageTitle" style="background-color:#e6ffe6;text-align:center"> Request information about host in listening </h1>
            
            <!-- Body with 2 forms -->
            <div style="text-align:center;">
                
                <!-- Form to check all hosts -->
                <?php
                    $connection = connectToDB();
                    $hostInArray = retrieveHost($connection);
                    showCheckAllHosts($hostInArray);
                ?>
                
                <!-- Form to check one specified host -->
                <form name="dataRequest" action="panelControl.php" method="POST">
                    <?php
                        #Here show the menu
                        showHost($hostInArray);
                    ?>
                    <br/>
                    <input type="submit" value="Check host" class="btn btn-outline-info">
                </form>
            </div>
        
        </div> <!-- Page container end -->
         
    </body>
</html>