<?php
require("model.php");

if (isset($_REQUEST['act'])) {
    $act=$_REQUEST['act'];
} else $act='';

switch($act) {
    case "check":
        $courseName = $_POST['courseName'];
        $data = isExist($courseName);
        if ((int)$data['count(*)'] == 0) {
            crawler($courseName);
        }
        $data = getcid($courseName);
        header("Location: showUI.html?cid=" . $data['cid'] . "&n=" . $courseName);
        break;
    case "getInfo":

    default;
}
?>
