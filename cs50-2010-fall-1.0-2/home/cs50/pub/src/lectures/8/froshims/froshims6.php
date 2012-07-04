<?
    /***********************************************************************
     * froshims6.php
     *
     * Computer Science 50
     * David J. Malan
     *
     * Implements a registration form for Frosh IMs.  Submits to itself.
     * Generates list of dorms via an array.
     **********************************************************************/

    // array of dorms
    $DORMS = array(
     "Apley Court",
     "Canaday",
     "Grays",
     "Greenough",
     "Hollis",
     "Holworthy",
     "Hurlbut",
     "Lionel",
     "Matthews",
     "Mower",
     "Pennypacker",
     "Stoughton",
     "Straus",
     "Thayer",
     "Weld",
     "Wigglesworth"
    );

    // if form was actually submitted, check for error
    if ($_POST["action"])
    {
        if ($_POST["name"] == "" || $_POST["gender"] == "" || $_POST["dorm"] == "")
            $error = TRUE;
    }
?>


<!DOCTYPE html>

<html>
  <head>
    <title>Frosh IMs</title>
  </head>
  <body>
    <div style="text-algin: center">
      <h1>Register for Frosh IMs</h1>
      <? if ($error): ?>
        <div style="color: red;">You must fill out the form!</div>
      <? endif ?>
      <br><br>
      <form action="froshims6.php" method="post">
        <table style="border: 0; margin-left: auto; margin-right: auto; text-align: left">
          <tr>
            <td>Name:</td>
            <td><input name="name" type="text" value="<?= htmlspecialchars($_POST["name"]) ?>"></td>
          </tr>
          <tr>
            <td>Captain:</td>
            <td><input name="captain" type="checkbox"></td>
          </tr>
          <tr>
            <td>Gender:</td>
            <td><input name="gender" type="radio" value="F"> F  <input name="gender" type="radio" value="M"> M</td>
          </tr>
          <tr>
            <td>Dorm:</td>
            <td>
              <select name="dorm" size="1">
                <option value=""></option>
                <? foreach ($DORMS as $dorm): ?>
                  <option value="<?= $dorm ?>"><?= $dorm ?></option>
                <? endforeach ?>
              </select>
            </td>
          </tr>
        </table>
        <br><br>
        <input name="action" type="submit" value="Register!">
      </form>
    </div>
  </body>
</html>
