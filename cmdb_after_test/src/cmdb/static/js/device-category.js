;
jQuery(document).ready(function ($) {
    var del_form = $('#device-cate-delete-form');
    $('.device-cate-delete-btn').click(function (e) {
        e.preventDefault();
        var id = $(this).data('id');
        var name = $(this).data('name');
        var url = $(this).attr('href');
        if (confirm('确定删除分类“' + name + '”？')) {
            del_form.attr('action', url);
            del_form.submit();
        }
    });
});
