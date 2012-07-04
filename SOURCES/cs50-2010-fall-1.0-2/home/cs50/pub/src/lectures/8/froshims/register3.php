<?
    /***********************************************************************
     * register3.php
     *
     * Computer Science 50
     * David J. Malan
     *
     * Implements a registration form for Frosh IMs.  Reports registration 
     * via email.  Redirects user to froshims3.php upon error.
     **********************************************************************/

    // validate submission
    if ($_POST["name"] != "" && $_POST["gender"] != "" && $_POST["dorm"] != "")
    {

        $to = "malan@cs50.net";
        $subject = "Registration";
        $body = "This person just registered:\n\n" .
         $_POST["name"] . "\n" .
         $_POST["captain"] . "\n" .
         $_POST["gender"] . "\n" .
         $_POST["dorm"];
        $headers = "From: malan@cs50.net\r\n";
        mail($to, $subject, $body, $headers);
    }
    else
    {
        header("Location: http://cloud.cs50.net/~cs50/lectures/8/src/froshims/froshims3.php");
        exit;
    }
?>

<!DOCTYPE html>

<html>
  <head>
    <title>Frosh IMs</title>
  </head>
  <body>
    You are registered!  (Really.)
  </body>
</html>
