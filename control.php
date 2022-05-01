<?php
require("model.php");

if (isset($_REQUEST['act'])) {
    $act=$_REQUEST['act'];
} else $act='';

switch($act) {
    case "check":
        $courseName = $_POST['courseName'];
        $list = isExist($courseName);
        if ((int)$list['count(*)'] == 0) {
            crawler($courseName);
        }
        header("Location: showUI.html?n=" . $courseName);
        break;
    case "getInfo":

    default;
}
?>
