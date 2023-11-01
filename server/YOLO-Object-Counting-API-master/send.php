<?php
$conn= mysqli_connect('192.168.0.63', 'root', 'pi','mysql');
      if(mysqli_connect_error($conn)){
          echo "error!"
          exit();
      }
      $sql="SELECT * FROM counting";
      $result=mysqli_query($conn,$sql);

      $board = mysqli_fetch_array($result);
       echo $board['datatime'];
       echo $board['counting'];
    ?>
