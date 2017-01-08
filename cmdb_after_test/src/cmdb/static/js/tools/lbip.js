$(document).ready(function () {
    $("#list1").click(function () {
        var url = $(this).attr("data");
        window.location.href = url;
    });
    $("#list2").click(function () {
        var url = $(this).attr("data");
        window.location.href = url;
    });
    $("#force_refresh").click(function () {
        window.location.href=window.location.href;
    });
});