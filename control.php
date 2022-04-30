<?php
require("model.php");

if (isset($_REQUEST['act'])) {
    $act=$_REQUEST['act'];
} else $act='';

switch($act) {
    case "getInfo":
        $courseName = $_POST['courseName'];
        $list = isExist($courseName);
        if ((int)$list['count(*)'] == 0) {
            crawler($courseName);
            echo "爬取完成";
            break;
        } else {
            echo"已有資料";
            break;
        }
    default;
}
?>