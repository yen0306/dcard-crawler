<?php
require("model.php");

if (isset($_REQUEST['act'])) {
    $act=$_REQUEST['act'];
} else $act='';

switch($act) {
    case "check":  //查看是否已有資料
        $courseName = $_POST['courseName'];
        $data = isExist($courseName);
        if ((int)$data['count(*)'] == 0) {  //如果沒有資料就執行爬蟲
            crawler($courseName);
        }
        $data = getcid($courseName);
        header("Location: showUI.html?cid=" . $data['cid'] . "&n=" . $courseName);
        break;
    case "getInfo":  //取得文章所有資訊
        $cid = $_GET['cid'];
        $list = getInfo($cid);
        echo json_encode($list);
        break;
    default;
}
?>
