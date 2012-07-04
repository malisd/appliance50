<?
    /***************************************************************
     * register1.php
     *
     * Computer Science 50
     * David J. Malan
     *
     * Implements a registration form for Frosh IMs.  Redirects 
     * user to froshims1.php upon error.
     ***************************************************************/

    // validate submission
    if ($_POST["name"] == "" || $_POST["gender"] == "" || $_POST["dorm"] == "")
    {
        header("Location: http://cloud.cs50.net/~cs50/lectures/8/src/froshims/froshims1.php");
        exit;
    }

?>

<!DOCTYPE html>

<html>
  <head>
    <title>Frosh IMs</title>
  </head>
  <body>
    You are registered!  (Well, not really.)
  </body>
</html>
