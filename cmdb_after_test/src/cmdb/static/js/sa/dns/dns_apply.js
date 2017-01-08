;
prefixs = [];
var apply_dns = {
    apply_dns: function () {
        var that = this;
        $(".list").click(function () {
            var url = $(this).attr("data");
            window.location.href = url;
        });

        $("#searchBtn").click(function () {
            $("#zone_id").submit();
        });

        $("#switch_ip").click(function () {
            $("#ip").css('display', 'block');
            $("#domain").css('display', 'none');
            $("#ip_domain").attr('placeholder', '请输入要A记录到的IP')
        });
        $("#switch_cname").click(function () {
            $("#ip").css('display', 'none');
            $("#domain").css('display', 'block');
            $("#ip_domain").attr('placeholder', '请输入要CNAME到的域名')
        });

        $(".zone_type").change(function () {
            var type = $(this).val();
            apply_dns.get_type_zone(type);
        });

        $("#applydns").click(function () {
            var pre_domain = $("#pre_domain").val();
            var zone = $("#zone").val();
            var ip_domain = $("#ip_domain").val();
            var content = $("#content").val();
            var tmp_type = $('#ip').css('display');
            if (pre_domain.length <= 0 || !(/(^[a-z\d\*]+)\.?([a-z\d]+)?$/).test(pre_domain)) {
                that.msgtips("请输入正确的前缀", 0);
                return false;
            } else {
                that.msgtips("");
            }
            if (zone == -1) {
                that.msgtips("请选择zone", 0);
                return false;
            }
            if (ip_domain.length <= 0) {
                that.msgtips("请输入ip或域名", 0);
                return false;
            } else {
                that.msgtips("");
            }
            if (tmp_type == 'block') {
                var type = 1;

                if (!(/^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/).test(ip_domain)) {
                    that.msgtips("请输入正确的ip格式", 0);
                    return false;
                } else {
                    that.msgtips("");
                }
            }
            else {
                var type = 2;
                if (!(/^([a-z0-9]+\.)+[a-z0-9]+$/).test(ip_domain)) {
                    that.msgtips("请输入正确的域名格式", 0);
                    return false;
                } else {
                    that.msgtips("");
                }
            }
            if (content.length <= 0) {
                that.msgtips("请输入描述", 0);
                return false;
            } else {
                that.msgtips("");
            }

            $.ajax({
                'url': '/sa/dns/apply',
                'type': 'post',
                'dataType': 'json',
                'data': { "pre_domain": pre_domain, "zone": zone, "ip_domain": ip_domain, "content": content, "type": type, "ip_updated": 0},
                success: function (res) {
                    if (res.code == 1) {
                        that.msgtips(res.msg, 0);
                    } else {
                        that.msgtips(res.msg, 1);
                        window.location.href = '/user/mydapply'
                    }
                }
            })
        });

        $("#modifydns").click(function () {
            var modify_value = $("#modify_value").val();
            var tmp_type = $('#ip').css('display');
            if (tmp_type == 'block') {
                var type = 1;
            }
            else {
                var type = 2;
            }

            $.ajax({
                'url': '/sa/dns/apply',
                'type': 'post',
                'dataType': 'json',
                'data': { "modify_value": modify_value, "type": type},
                success: function (res) {
                    if (res.code == 1) {
                        that.msgtips(res.msg, 0);
                    } else {
                        that.msgtips(res.msg, 1);
                        window.location.href = '/user/mydapply'
                    }
                }
            })
        });
    },

    switch_cdn: function () {
        $("input[name='area']").click(function () {
            $("#pre_zone").val('');
        });
        $("#zone").change(function () {
            $("#pre_zone").val('');
            $("#pre_zone_list").empty();
            var zone = $("#zone").val();
            for (var z in zones) {
                if(zones[z].id == zone) {
                    for(var x in zones[z].prefix)
                    $("#pre_zone_list").append("<option>" + zones[z].prefix[x] + "</option>")
                }
            }

        });

        $("#pre_zone").blur(function () {
            var area = $("input[name='area']:checked").val();
            var prefix = $("#pre_zone").val();
            var dn = $("#zone").find("option:selected").text();

            if (area && prefix && dn) {
                $.ajax({
                    'url': '/sa/dns/zone_cdn',
                    'type': 'get',
                    'dataType': 'json',
                    'data': { "area": area, "dn": dn, "prefix": prefix},
                    success: function (data) {
                        apply_dns.msgtips("", 1);
                        switch (data.pro) {
                            case "tencent":
                                $("#now_tencent_cdn").prop("checked", true);
                                break;
                            case "dnion":
                                $("#now_dnion_cdn").prop("checked", true);
                                break;
                            default :
                                apply_dns.msgtips("未找到该域名前缀，请检查！", 0);
                                $("input[name='now_pro']").prop("checked", false);
                        }
                    }
                });
            }
        });

        $("#applycdn").click(function () {
            apply_dns.msgtips("", 0);
            var area = $("input[name='area']:checked").val();
            var prefix = $("#pre_zone").val();
            var dn = $("#zone").find("option:selected").text();
            var now_pro = $("input[name='now_pro']:checked").val();
            var new_pro = $("input[name='new_pro']:checked").val();

            if (apply_dns.isnull(area)) {
                apply_dns.msgtips("请选择CDN区域！", 0);
                return;
            }
            if (apply_dns.isnull(dn)) {
                apply_dns.msgtips("请选择域名！", 0);
                return;
            }
            if (apply_dns.isnull(prefix)) {
                apply_dns.msgtips("请输入域名前缀！", 0);
                return;
            }
            if (apply_dns.isnull(now_pro)) {
                apply_dns.msgtips("未找到该域名前缀，请修改！", 0);
                return;
            }
            if (apply_dns.isnull(new_pro)) {
                apply_dns.msgtips("请选择要切换到的CDN！", 0);
                return;
            }
            if (now_pro == new_pro) {
                apply_dns.msgtips("要切换到的CDN和现在的一样啦！！", 0);
                return;
            }

            $.ajax({
                'url': '/sa/dns/zone_cdn',
                'type': 'post',
                'dataType': 'json',
                'data': { "area": area, "dn": dn, "prefix": prefix, "now_pro": now_pro,"new_pro": new_pro},
                success: function (data) {
                    if (data.isOk) {
                        apply_dns.msgtips("CDN切换成功！", 1);
                        switch (data.pro) {
                            case "tencent":
                                $("#now_tencent_cdn").prop("checked", true);
                                break;
                            case "dnion":
                                $("#now_dnion_cdn").prop("checked", true);
                                break;
                        }
                    }
                    else {
                        apply_dns.msgtips("CDN切换错误，请联系管理员！", 0);
                    }
                }
            });
        });
    },

    show_list: function() {
//        for(var i=0;i<5;i++) {
//            var tabel = "<div>\
//            <table>\
//                <thead>\
//                <tr>\
//                    <th>前缀</th>\
//                    <th>域名</th>\
//                    <th>CDN</th>\
//                    <th>厂商</th>\
//                    <th>地区</th>\
//                    <th>更新日期</th>\
//                </tr>\
//                </thead>\
//                <tbody id='area'"+i+"></tbody>\
//            </table>\
//        </div>";
//            $("#area").append(html);
//        }
        for(var i in cdnlists) {
            var html = "<tr>\
                    <td>" + cdnlists[i].prefix + "</td>\
                    <td>" + cdnlists[i].zone + "</td>\
                    <td>" + cdnlists[i].cdn + "</td>\
                    <td>" + cdnlists[i].cdn_name + "</td>\
                    <td>" + cdnlists[i].area_descri + "</td>\
                    <td>" + cdnlists[i].updated + "</td>\
                    <td><a href='javascript:void(0)' cdn_details_id=" + cdnlists[i].id + " name='cdn_details_modify'>切换</a></td>\
                    </tr>";
            $("tbody[id=area"+cdnlists[i].area+"]").append(html)
        }

        $("a[name='cdn_details_modify']").click(function() {
            var id = $(this).attr('cdn_details_id');
            $.ajax({
                url: "/sa/dns/cdn_list",
                type: "POST",
                dataType: "json",
                data: {"id":id},
                success: function(data) {
                    if (data.isOk) {
                        window.location.reload();
                    }
                }
            });
        });

//        $("#cdn_seach").click(function() {
//            var prefix = $("#pre_zone").val();
//            if(prefix != "") {
//                $.ajax({
//                    url: "/sa/dns/cdn_list",
//                    type: "GET",
//                    dataType: "json",
//                    data: {"id":id},
//                    success: function(data) {
//                        if (data.isOk) {
//                            window.location.reload();
//                        }
//                }
//
//                });
//            }
//        });
    },

    isInArray: function (val, arr) {
        var a = false;
        if (arr == []) {
            return a;
        }
        for (var i in arr) {
            if (arr[i] == val) {
                a = true;
                break;
            }
        }
        return a;
    },

    isnull: function (v) {
        if (v == "" || v == null || v == undefined) {
            return true;
        }
        else {
            return false;
        }
    },

    msgtips: function (msg, type) {
        if (msg) {
            if (type == 0) {
                $("#msgtip").removeClass("success");
                $("#msgtip").addClass("alert");
            } else if (type == 1) {
                $("#msgtip").removeClass("alert");
                $("#msgtip").addClass("success");
            }
            $("#msgtip").html(msg);
            $("#msgtip").show();
        } else {
            $("#msgtip").hide();
        }
    },

    get_zone: function () {
        $("#zone").empty();
        for (var z in zones) {
            $("#zone").append("<option value=" + zones[z].id + ">" + zones[z].zone + "</option>")
        }
    },

    get_type_zone: function (type) {
        $("#zone").empty();
        for (var z in zones) {
            if(zones[z].type == type) {
                $("#zone").append("<option value=" + zones[z].id + ">" + zones[z].zone + "</option>")
            }
        }
    }
}

$(document).ready(function () {
    apply_dns.apply_dns();
    if (flag == "switch_cdn") {
        apply_dns.get_zone();
        apply_dns.switch_cdn();
        $("#zone").trigger('change');
    }
    else if (flag == "cdn_list") {
        apply_dns.show_list();
    }
});