$(function() {
	var graph = new Q.Graph("canvas");
    
    function onDataCollected(txt){
        var json = JSON.parse(txt);
        translateToQuneeElements(json, graph);
    }
    function translateToQuneeElements(json, graph){
        var map = {};
        if(json.nodes){
            Q.forEach(json.nodes, function(data){
                var node = graph.createNode(data.name, data.x || 0, data.y || 0);
                node.set("data", data);
                map[data.id] = node;
            });
        }
        if(json.edges){
            Q.forEach(json.edges, function(data){
                var from = map[data.from];
                var to = map[data.to];
                if(!from || !to){
                    return;
                }
                var edge = graph.createEdge(data.name, from, to);
                edge.set("data", data);
            }, graph);
        }
    }
    graph.ondblclick = function(evt){
        var node = evt.data;
        if(node){
            var newName = prompt("New Name:");
            if(newName){
            node.name = newName;
            }
        }
    }
    request("/static/js/virtual/data-server", "", onDataCollected);
});
function request(url, params, callback, callbackError) {
    try {
        var req = new XMLHttpRequest();
        req.open('GET', encodeURI(url));
        req.onreadystatechange = function(e) {
            if (req.readyState != 4) {
                return;
            }
            if (200 == req.status) {
                var code = req.responseText;
                if (code && callback) {
                    callback(req.responseText);
                }
                return;
            }else{
                if (callbackError) {
                    callbackError();
                }
            }
        }
        req.send(params);
    } catch (error) {
        if (callbackError) {
            callbackError();
        }
    }
}