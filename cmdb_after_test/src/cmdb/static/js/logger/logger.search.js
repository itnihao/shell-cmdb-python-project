;
String.prototype.format = function(args) {
    if (arguments.length > 0) {
        var result = this;
        if (arguments.length == 1 && typeof(args) == "object") {
            for (var key in args) {
                var reg = new RegExp("({" + key + "})", "g");
                result = result.replace(reg, args[key]);
            }
        } else {
            for (var i = 0; i < arguments.length; i++) {
                if (arguments[i] == undefined) {
                    return "";
                } else {
                    var reg = new RegExp("({[" + i + "]})", "g");
                    result = result.replace(reg, arguments[i]);
                }
            }
        }
        return result;
    } else {
        return this;
    }
};

function logFinder(opts) {
    var def = {
        tmFrom: 1217682548,
        tmEnd: 1917682848,
        host: '',
        kw: '*',
        page:1,
        offset:0,
        pageSize: 100
    }

    opts = opts || {};
    this.opts = def;
    for (var x in opts) {
        this.opts[x] = opts[x]
    }

    if (undefined == this.opts['container'] ) {
        var __e = new Error();
        throw new Error('container mast be setup');
    }

    this.opts['container'] = $(this.opts['container']);

}

logFinder.prototype.buildParams = function() {
    var qs = {
        "query": {
            "filtered": {
                "query": {
                    "bool": {
                        "should": [{
                            "query_string": {
                                "query": this.opts.kw
                            }
                        }]
                    }
                },
                "filter": {
                    "bool": {
                        "must": [{
                            "range": {
                                "@timestamp": {
                                    "from": 1217682548400,
                                    "to": 1517682848400
                                }
                            }
                        },
                        {
                            "fquery": {
                                "query": {
                                    "query_string": {
                                        "query": "@source_host:(\""+this.opts.host+"\")"
                                    }
                                },
                                "_cache": false
                            }
                        }]
                    }
                }
            }
        },
        "highlight": {
            "fields": {},
            "fragment_size": 2147483647,
            "pre_tags": ["@start-highlight@"],
            "post_tags": ["@end-highlight@"]
        },
        "size": this.opts.pageSize,
        "from":this.opts.offset,
        "sort": [{
            "@timestamp": {
                "order": "desc",
                "ignore_unmapped": true
            }
        },
        {
            "@timestamp": {
                "order": "desc",
                "ignore_unmapped": true
            }
        }]
    };

    return qs;
}

logFinder.prototype.find = function(page,obj) {
    var client = new $.es.Client({
        hosts: '10.10.3.156:9200'
    });

    var page = ~~page || 1;
    this.opts.page = page;
    this.opts.offset = (page-1) * this.opts.pageSize;


    var host = $("#txt-host-name").val().trim();
    var kw = $("#txt-kw").val().trim();
    var ps = $("#txt-pagesize").val();


    //checking if multi host
    if(/\,/.test(host)) {
    	host = host.split(",");
    	host = host.join('","');
    }

    this.opts.pageSize = ps;
    this.opts.kw = kw || '*';
    this.opts.host = host;

    if(! this.opts.host ) {
    	console.log("Host must be pass in ");
    	return false;
    }

    var qs = this.buildParams();

    var self = this;
    this.opts.container.html("");

    client.search({
        type: 'syslog',
        body: qs
    }).then(function(body) {
        var hits = body.hits.hits;
        var total = body.hits.total;
        if (total <= 0) {
            self.opts.container.html("<p style='color:red;fonts-weight:bold'>抱歉,没有查询到相关日志!</p>");
            return false;
        }

        var pages = Math.ceil(total / self.opts.pageSize);

        $("#pageInfo").html("共找到: <fonts color='#c0392b'>{0}</fonts> 条记录,每页显示: {1} 条记录,当前第 <fonts color='#d35400'>{2}</fonts> 页,共:{3}页".format(total, self.opts.pageSize, page,pages));

        for (var x in hits) {
        	var msg = hits[x]._source["@message"].replace(kw,'<fonts style="color:red">'+kw+'</fonts>');
            self.opts.container.append("<p class='log-row' style='color:green'><b style='margin-right:5px;color:#f39c12' > " + hits[x]._source["@source_host"] + "</b>" + msg + "</p>");
        }


        var prePage = ~~(~~page-1);
        var b = $('<a class="button info tiny" href="javascript:void 0;"  p='+ prePage +'>上一页</a>');
        if(nextPage >pages) {
        	b.html("首页");
        	b.attr('p',1);
        }else {
        	b.bind('click',function(){
	        	obj.find($(this).attr('p') ,obj);
	        });
        }

        $("#log-pagenation").html(b);

        var nextPage = ~~(~~page+1);
        var b = $('<a class="button info tiny" style="margin-left:15px" href="javascript:void 0;"  p='+ nextPage +'>下一页</a>');
        if(nextPage >pages) {
        	b.html("末页");
        	b.attr('disabled',true);
        }else {
        	b.bind('click',function(){
	        	obj.find($(this).attr('p') ,obj);
	        });
        }
        $("#log-pagenation").append(b);

    },
    function(error) {
        console.trace(error.message);
    });

}