<?php
require("dbconfig.php");

function isExist($courseName) {  //查看是否已有資料
    global $db;
    $sql = "select count(*) from course where courseName = ?;";
    $stmt = mysqli_prepare($db, $sql);
    mysqli_stmt_bind_param($stmt, "s", $courseName);
    mysqli_stmt_execute($stmt);
    $result = mysqli_stmt_get_result($stmt);
    $rs = mysqli_fetch_assoc($result);
    return $rs;
}
function getcid($courseName) {  //取得cid
    global $db;
    $sql = "select cid from course where courseName = ?;";
    $stmt = mysqli_prepare($db, $sql);
    mysqli_stmt_bind_param($stmt, "s", $courseName);
    mysqli_stmt_execute($stmt);
    $result = mysqli_stmt_get_result($stmt);
    $rs = mysqli_fetch_assoc($result);
    return $rs;
}
function crawler($courseName) {  //執行爬蟲程式
    exec("python crawler.py $courseName");
}
?>
