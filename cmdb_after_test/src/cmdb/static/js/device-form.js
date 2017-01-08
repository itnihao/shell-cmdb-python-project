/**
 *
 *
 * Created by roydong on 8/4/14.
 */

jQuery(document).ready(function ($) {
    frame_display();

    $("#device-cate").change(function() {
        frame_display();
    });

    function frame_display() {
        if($("#device-cate").val() == 1) {
            $("#frame").show();
        }
        else {
            $("#frame").hide();
        }
    }

    $.fn.getCursorPosition = function () {
        var elem = $(this).get(0);
        var pos = 0;
        if ('selectionStart' in elem) {
            pos = elem.selectionStart;
        } else if ('selection' in document) {
            elem.focus();
            var sel = document.selection.createRange();
            var selLength = document.selection.createRange().text.length;
            sel.moveStart('character', -elem.value.length);
            pos = sel.text.length - selLength;
        }

        return pos;
    };

    $.fn.setCursorPosition = function (pos) {
        var elem = $(this).get(0);

        if (elem.createTextRange) {
            var range = elem.createTextRange();
            range.move('character', pos);
            range.select();
        } else if (elem.selectionStart) {
            elem.setSelectionRange(pos, pos);
        }
    };

    function delete_row(e) {
        e.preventDefault();
        $(this).parent().parent().remove();
    }

    function number_only_filter(e) {
        var me = $(this);
        if (e.keyCode < 37 || e.keyCode > 40) {
            var pos = me.getCursorPosition();
            var value = me.val().replace(/[^\d\.]+/, '');
            if (value != me.val()) {
                pos = pos - me.val().length + value.length;
                me.val(value);
                me.setCursorPosition(pos);
            }
        }
    }

    function model_autocomplete(node) {
        node.autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: "/cmdb/device/autocomplete",
                    type: 'POST',
                    dataType: "json",
                    data: {
                        q: request.term
                    },
                    success: function (data) {
                        response($.map(data, function (item) {
                            return {
                                value: item
                            }
                        }));
                    }
                });
            },
            minChars: 1,
            max: 5,
            scroll: true,
            autoFill: true,
            mustMatch: true,
            matchContains: false,
            scrollHeight: 50,
            select: function (event, ui) {
                $("#model").val(ui.item.value);
            }
        });
    }
    model_autocomplete($('#model'));

    function ip_autocomplete(node) {
        node.find('input[name="net-ip[]"]').autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: "/cmdb/host/hostip/autocomplete",
                    type: 'POST',
                    dataType: "json",
                    data: {
                        q: request.term
                    },
                    success: function (data) {
                        response($.map(data, function (item) {
                            return {
                                label: item[1],
                                value: item[0]
                            }
                        }));
                    }
                });
            },
            minChars: 1,
            max: 5,
            scroll: true,
            autoFill: true,
            mustMatch: true,
            matchContains: false,
            scrollHeight: 50,
            select: function (event, ui) {
                $(this).val(ui.item.label);
                var input = $(this).parent().find('input[name="net-ip-id[]"]');
                input.val(ui.item.value);
                return false;
            }
        });
    }

    ip_autocomplete($('.net-row'));

    $('a.delete-row-btn').click(delete_row);

    $('input.number-only').keyup(number_only_filter);

    $('#cpu-add-btn').click(function (e) {
        e.preventDefault();
        var row = $('<div class="row cpu_row">' +
            '<div class="small-3 columns"><input class="number-only" name="cpu-num[]" type="text"/></div>' +
            '<div class="small-3 columns"><input name="cpu-model[]" type="text"/></div>' +
            '<div class="small-1 columns" style="text-align: center; line-height: 32px; height: 32px;">' +
            '<a href="#" class="delete-row-btn" style="fonts-size: 14px;">删除</a></div>' +
            '<div class="small-1 columns"></div>');

        row.find('a.delete-row-btn').click(delete_row);
        row.find('input.number-only').keyup(number_only_filter);
        row.insertBefore($(this));
    });

    $('#storage-add-btn').click(function (e) {
        e.preventDefault();
        var row = $('<div class="row storage_row">' +
            '<div class="small-2 columns"><input class="number-only" name="disk-capacity[]" type="text"/></div>' +
            '<div class="small-2 columns"><input class="number-only" name="disk-speed[]" type="hidden"/>' +
             '<select name="disk-type[]">'+
                '<option  value="">未登记</option>'+
                '<option value="0">Intel SSD DC S3710</option>'+
                '<option value="1">Intel SSD DC S3700</option>'+
                '<option value="2">Intel SSD DC S3610</option>'+
                '<option value="3">Intel SSD DC S3510</option>'+
                '<option value="4">Intel SSD DC S3500</option>'+
            '</select>'+
            '</div>' +
            '<div class="small-2 columns"><input name="disk-inter[]" type="text"/></div>' +
            '<div class="small-2 columns"><select name="disk-size[]">' +
            '<option value="">未登记</option>' +
            '<option value="1.8">1.8英寸</option>' +
            '<option value="2.5">2.5英寸</option>' +
            '<option value="3.5">3.5英寸</option>' +
            '<option value="5.25">5.25英寸</option></select></div>' +
            '<div class="small-1 columns" style="text-align: center; fonts-size: 25px;">×</div>' +
            '<div class="small-1 columns"><input class="number-only" name="disk-count[]" type="text"/></div>' +
            '<div class="small-1 columns" style="text-align: center; line-height: 32px; height: 32px;">' +
            '<a href="#" class="delete-row-btn"  style="fonts-size: 14px;">删除</a></div>' +
            '<div class="small-1 columns"></div>');

        row.find('a.delete-row-btn').click(delete_row);
        row.find('input.number-only').keyup(number_only_filter);
        row.insertBefore($(this));
    });

    var net_names = $('#net-names').val().split(' ');
    $('#net-add-btn').click(function (e) {
        e.preventDefault();

        var select = '<select name="net-name[]">';
        for (var i = 0; i < net_names.length; i++) {
            select += '<option value="' + i + '">' + net_names[i] + '</option>';
        }
        select += '</select>';

        var row = $('<div class="row net-row">' +
            '<div class="small-1 columns" style="text-align: center">' + select + '</div>' +
            '<div class="small-3 columns">' +
            '<input name="net-ip-id[]" type="hidden"/>' +
            '<input name="net-ip[]" class="number-only" type="text"/></div>' +
            '<div class="small-3 columns"><input name="net-mac[]" type="text"/></div>' +
            '<div class="small-1 columns" style="text-align: center; line-height: 32px; height: 32px;">' +
            '<a href="#" class="delete-row-btn" style="fonts-size: 14px;">删除</a></div>' +
            '<div class="small-1 columns"></div>');

        ip_autocomplete(row);
        row.find('a.delete-row-btn').click(delete_row);
        row.find('input.number-only').keyup(number_only_filter);
        row.insertBefore($(this));
    });

    $('#idc-droplist').change(function () {
        var idc_id = $(this).val();
        var rack = $('#rack-droplist-' + idc_id);
        var racks = $('.rack-droplist');
        racks.attr('name', '');
        racks.addClass('none');
        rack.removeClass('none');
        rack.attr('name', 'rack');
    });

    $('#buy-time').datepicker({
        changeMonth: true,
        changeYear: true,
        yearRange: 'c-30:c+10'
    });

    var submit = $('#device-form-submit');
    var form = submit.parent();
    var num = 0;
    var batch_add = $('#batch-add-form');
    var batch_stop = false;
    var batch_result = $('#batch-add-result');

    function recursive_add(i) {
        if (batch_stop || i > num) {
            return;
        }

        var div = $('<div class="batch-add-row">...</div>');
        div.insertBefore(batch_result);
        $.ajax({
            url: submit.data('batch-add'),
            type: 'post',
            data: form.serialize(),
            complete: function () {
                i++;
                recursive_add(i);
            },
            success: function (response) {
                if (response.id > 0) {
                    div.html(i + '. <span style="color: green">创建成功, id:' + response.id + ', 编号: ' + response.label + '</span>');
                } else {
                    div.html(i + '. <span style="color: red">失败</span>');
                }
            },
            failure: function (error) {
                div.html(i + '. <span style="color: red">失败</span>');
            }
        });
    }

    batch_add.bind('opened', function () {
        recursive_add(1);
    });

    batch_add.bind('closed', function () {
        $('.batch-add-row').remove();
    });

    submit.click(function (e) {
        e.preventDefault();
        num = $('#batch-num').val() || 0;
        if (num > 1) {
            batch_add.foundation('reveal', 'open');
        } else {
            form.submit();
        }
    });
});
