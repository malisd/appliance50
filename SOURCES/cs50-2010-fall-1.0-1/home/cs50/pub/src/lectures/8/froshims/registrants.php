<?
    // connect to database
    mysql_connect("mysql.localdomain", "malan", "12345");
    mysql_select_db("malan_lecture");

    // prepare query
    $sql = "SELECT * FROM registrants";

    // execute query
    $result = mysql_query($sql);


?>

<!DOCTYPE html>

<html>
  <head>
    <title>Frosh IMs</title>
  </head>
  <body>
    <ul>
      <?
          // iterate over results
          while ($row = mysql_fetch_array($result))
          {
              print("<li>");
              print(htmlspecialchars($row["name"]));
              print("</li>");
          }
      ?>
    </ul>
  </body>
</html>
