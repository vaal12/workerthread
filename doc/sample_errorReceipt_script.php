<?php

echo "We have post parameter<br>";
echo $_POST["report"];
echo "<br>\nUser comment:";
echo $_POST["user_comment"];
echo "<br>\nProgramm version:";
echo $_POST["version"];

$mail_body1 = $_POST["report"]."\n\nUser comment:".$_POST["user_comment"]."\n\nProgramm version:".$_POST["version"];
echo "<br>\nMail body:";
echo $mail_body1;
mail("user@example.com", "Programm error", $mail_body1);

echo "Mail sent"

?>