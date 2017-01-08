$(function () {
    var graph = new Q.Graph("canvas");

    function onDataCollected(txt) {
        var json = JSON.parse(txt);
        translateToQuneeElements(json, graph);
    }

    function translateToQuneeElements(json, graph) {
        var map = {};
        if (json.nodes) {
            Q.forEach(json.nodes, function (data) {
                var node = graph.createNode(data.name, data.x || 0, data.y || 0);
                node.set("data", data);
                map[data.id] = node;
            });
        }
        if (json.edges) {
            Q.forEach(json.edges, function (data) {
                var from = map[data.from];
                var to = map[data.to];
                if (!from || !to) {
                    return;
                }
                var edge = graph.createEdge(data.name, from, to);
                edge.set("data", data);
            }, graph);
        }
    }

    graph.ondblclick = function (evt) {
        var node = evt.data;
        if (node) {
            var newName = prompt("New Name:");
            if (newName) {
                node.name = newName;
            }
        }
    }
    request("/static/js/virtual/data-server", "", onDataCollected);


    var defaultnode = graph.createNode("default node", -150, -10);

    var layouter = new Q.TreeLayouter(graph);
    layouter.parentChildrenDirection = Q.Consts.DIRECTION_RIGHT;
    layouter.layoutType = Q.Consts.LAYOUT_TYPE_EVEN_HORIZONTAL;

    // layouter.doLayout({
    //     callback: function () {
    //         graph.zoomToOverview();
    //     }
    // });

    graph.styles = {};
    graph.styles[Q.Styles.SELECTION_TYPE] = Q.Styles.SELECTION_TYPE_BORDER;
    graph.styles[Q.Styles.SELECTION_COLOR] = '#FAO';
    graph.styles[Q.Styles.SELECTION_TYPE_BORDER] = 3;

    graph.isMovable = function () {  // 图中元素不可移动
        return false;
    };
    graph.moveToCenter();       // 图中元素自动放置在中心位置

    var hgap = 250;
    var vgap = 40;
    var center_node = createNode(-55, 80, 'Center', null, 0, '#FAO');
    var edge0 = createEdge(center_node, defaultnode);

    // var a = createNode(0, 0, 'Web LB 1', null, 0, '#FA0');
    // a.parentChildrenDirection = Q.Consts.DIRECTION_RIGHT;
    // a.layoutType = Q.Consts.LAYOUT_TYPE_EVEN_VERTICAL;
    var b1 = createNode(hgap, -vgap, 'Web LB 2', '#FF0', 0, '#FF0');
    var b2 = createNode(hgap, vgap, 'Web LB 3', null, 0, '#00F');
    var c1 = createNode(hgap * 2, 0, 'Web LB 4', '#FF0', 0, '#0FF');
    var c2 = createNode(hgap * 2, vgap / 3 + 2 * vgap, 'Web LB 5', null, 0, '#0F0');

    // var edge1 = createEdge(a, b1);
    // var edge2 = createEdge(a, b2);
    // var edge3 = createEdge(a, c1);
    // var edge4 = createEdge(a, c2);
    var edge5 = createEdge(b1, c1);
//            var edge6 = createEdge(b1, c2);
    var edge7 = createEdge(b2, c1);
    var edge8 = createEdge(b2, center_node);
    // var edge9 = createEdge(a, c2);
    // edge9.edgeType = Q.Consts.EDGE_TYPE_ORTHOGONAL_HORIZONTAL;

    initDatas();
    function createNode(x, y, text, fillColor, number, lampColor, parent) {
        var width = 150;
        var height = 24;
        var padding = 4;
        var node = graph.createNode(text, x, y);
        // node.image = 'interaction/web.png';//cloud.svg';
        node.size = {height: height};
        node.setStyle(Q.Styles.LABEL_ANCHOR_POSITION, Q.Position.CENTER_MIDDLE);
        node.setStyle(Q.Styles.LABEL_POSITION, {x: width / 2, y: height / 2});
        node.setStyle(Q.Styles.BACKGROUND_COLOR, fillColor || '#FFF');
        node.setStyle(Q.Styles.BORDER, 1);
        node.setStyle(Q.Styles.BORDER_COLOR, '#FA0');
        node.setStyle(Q.Styles.PADDING, padding);

        // node.image = randomIcon();
        if (parent) {
            node.parent = parent;
        }

        var numberLabel = new Q.LabelUI();
        numberLabel.position = {x: width - 10, y: height / 2 - 6};
        numberLabel.fontSize = 10;
        numberLabel.fontStyle = 'bold';
        node.addUI(numberLabel, {
            property: "number",
            propertyType: Q.Consts.PROPERTY_TYPE_CLIENT,
            bindingProperty: "data"
        });
        node.set('number', '' + number);
        var lamp = new Q.ImageUI(Q.Shapes.getShape(Q.Consts.SHAPE_CIRCLE, -3.5, -3.5, 7, 7));
        lamp.fillGradient = new Q.Gradient(Q.Consts.GRADIENT_TYPE_RADIAL, [Q.toColor(0xAAFFFFFF), Q.toColor(0x33EEEEEE), Q.toColor(0x44888888), Q.toColor(0x33666666)],
            [0.1, 0.3, 0.7, 0.9], 0, -0.2, -0.2);
        lamp.lineWidth = 0.5;
        lamp.strokeStyle = '#CCC';
        lamp.position = {x: width - 10, y: height / 2 + 6};
        node.addUI(lamp, {
            property: "lampColor",
            propertyType: Q.Consts.PROPERTY_TYPE_CLIENT,
            bindingProperty: "fillColor"
        });
        node.set('lampColor', lampColor);

        return node;
    }

    function createEdge(from, to) {
        var edge = graph.createEdge(from, to);
        edge.setStyle(Q.Styles.ARROW_TO_SIZE, {width: 5, height: 8});
        edge.edgeType = Q.Consts.EDGE_TYPE_ORTHOGONAL_HORIZONTAL;  // 连线为折线
        edge.setStyle(Q.Styles.EDGE_SPLIT_BY_PERCENT, false);
        edge.setStyle(Q.Styles.EDGE_SPLIT_VALUE, 30);
        edge.setStyle(Q.Styles.EDGE_CORNER, Q.Consts.EDGE_CORNER_NONE);
        return edge;
    }

    function createNodes(start, numbers, parent, callback) {
        for (var i0 = 0; i0 < numbers; i0++) {
            var node = createNode(parent);
            var edge;
            if (start) {
                edge = createEdge(start, node);//
                node.parentChildrenDirection = start.parentChildrenDirection;
                if (start.layoutType == Q.Consts.LAYOUT_TYPE_TWO_SIDE) {
                    edge.edgeType = Q.isHorizontalDirection(start.parentChildrenDirection) ? Q.Consts.EDGE_TYPE_HORIZONTAL_VERTICAL : Q.Consts.EDGE_TYPE_VERTICAL_HORIZONTAL;
                } else {
                    edge.edgeType = Q.isHorizontalDirection(start.parentChildrenDirection) ? Q.Consts.EDGE_TYPE_ORTHOGONAL_HORIZONTAL : Q.Consts.EDGE_TYPE_ORTHOGONAL_VERTICAL;
                    edge.setStyle(Q.Styles.EDGE_SPLIT_BY_PERCENT, false);
                    edge.setStyle(Q.Styles.EDGE_SPLIT_VALUE, 30);
                }
            }
            if (callback) {
                callback(node, edge, start);
            }
        }
    }

    function initDatas() {
        createTreeDatas(Q.Consts.DIRECTION_RIGHT);
        // createTreeDatas(Q.Consts.DIRECTION_TOP);
    }

    function createTreeDatas(parentChildrenDirection) {
        var node = createNode(0, 0, 'root', null, 0, '#FA0');
        node.name = "root";
        node.parentChildrenDirection = parentChildrenDirection;

        var isHorizontal = parentChildrenDirection == Q.Consts.DIRECTION_RIGHT;

        node.layoutType = Q.Consts.LAYOUT_TYPE_EVEN;
        createNodes(node, 2, null, function (node, edge, start) {
            node.layoutType = Q.Consts.LAYOUT_TYPE_EVEN;
            createNodes(node, 2, null, function (node, edge, start) {
                node.layoutType = Q.Consts.LAYOUT_TYPE_TWO_SIDE;
                node.hGap = 20;
                node.vGap = 30;
                createNodes(node, Q.randomInt(4) + 5, null, function (node, edge, start) {
                    node.layoutType = Q.Consts.LAYOUT_TYPE_TWO_SIDE;
                    if (isHorizontal) {
                        node.hGap = 20;
                    } else {
                        node.vGap = 30;
                    }
                    createNodes(node, 3 + Q.randomInt(3));
                });
            });
        });

        Q.log(graph.graphModel.length);
    }


    //do layout
    // graph.callLater(function () {
    //     var fromBounds = graph.getUIBounds(edge3.from);
    //     var toBounds = graph.getUIBounds(edge3.to);
    //     edge3.addPathSegment([fromBounds.right, fromBounds.cy - 10]);
    //     edge3.addPathSegment([fromBounds.right + 15, fromBounds.cy - 10]);
    //     edge3.addPathSegment([fromBounds.right + 15, fromBounds.cy - 80]);
    //     edge3.addPathSegment([toBounds.x - 20, fromBounds.cy - 80]);
    //     edge3.addPathSegment([toBounds.x - 20, toBounds.cy - 5]);
    //     edge3.addPathSegment([toBounds.x, toBounds.cy - 5]);
    //
    //     var fromBounds = graph.getUIBounds(edge5.from);
    //     var toBounds = graph.getUIBounds(edge5.to);
    //     edge5.addPathSegment([fromBounds.right, fromBounds.cy]);
    //     edge5.addPathSegment([toBounds.x - 25, fromBounds.cy]);
    //     edge5.addPathSegment([toBounds.x - 25, toBounds.cy]);
    //     edge5.addPathSegment([toBounds.x, toBounds.cy]);
    //
    //     var fromBounds = graph.getUIBounds(edge7.from);
    //     var toBounds = graph.getUIBounds(edge7.to);
    //     edge7.addPathSegment([fromBounds.right, fromBounds.cy]);
    //     edge7.addPathSegment([toBounds.x - 25, fromBounds.cy]);
    //     edge7.addPathSegment([toBounds.x - 25, toBounds.cy + 5]);
    //     edge7.addPathSegment([toBounds.x, toBounds.cy + 5]);
    //
    //     edge2.setStyle(Q.Styles.EDGE_FROM_OFFSET, {y: 8});
    // })

    // graph.setSelection(b1);

    // var time = setTimeout(function A() {
    //     graph.forEach(function (a) {
    //         if (!(a instanceof Q.Node)) {
    //             return;
    //         }
    //         a.set('number', '' + Q.randomInt(10));
    //         a.set('lampColor', Q.randomColor());
    //     })
    //     time = setTimeout(A, 1000);
    // }, 1000);

    // function destroy() {
    //     clearTimeout(time);
    // }
});


function request(url, params, callback, callbackError) {
    try {
        var req = new XMLHttpRequest();
        req.open('GET', encodeURI(url));
        req.onreadystatechange = function (e) {
            if (req.readyState != 4) {
                return;
            }
            if (200 == req.status) {
                var code = req.responseText;
                if (code && callback) {
                    callback(req.responseText);
                }
                return;
            } else {
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