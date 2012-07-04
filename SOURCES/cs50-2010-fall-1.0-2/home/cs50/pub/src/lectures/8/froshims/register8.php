<?
    /***********************************************************************
     * register8.php
     *
     * Computer Science 50
     * David J. Malan
     *
     * Implements a registration form for Frosh IMs.  Records registration 
     * in database.  Redirects user to froshims8.php upon error.
     **********************************************************************/

    // validate submission
    if ($_POST["name"] == "" || $_POST["gender"] == "" || $_POST["dorm"] == "")
    {
        header("Location: http://cloud.cs50.net/~cs50/lectures/8/src/froshims/froshims8.php");
        exit;
    }

    // connect to database
    mysql_connect("localhost", "malan", "12345");
    mysql_select_db("malan_lecture");

    // scrub inputs
    $name = mysql_real_escape_string($_POST["name"]);
    if ($_POST["captain"])
        $captain = 1;
    else
        $captain = 0;
    $gender = mysql_real_escape_string($_POST["gender"]);
    $dorm = mysql_real_escape_string($_POST["dorm"]);

    // prepare query
    $sql = "INSERT INTO registrants (name, captain, gender, dorm)
     VALUES('$name', $captain, '$gender', '$dorm')";

    // execute query
    mysql_query($sql);
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
