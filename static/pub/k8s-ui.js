function refresh_dataTable(dt_elem) {
    var table = dt_elem.DataTable();

    // setInterval(function () {

    table.ajax.reload();

    // }, 3000);

}

function notification_success(message) {
    $.notify(message, {
        element: 'body',
        type: 'info',
        timeout: 3000,
        newest_on_top: true,
        animate: {
            enter: 'animated rollIn',
            exit: 'animated rollOut'
        }
    });
}

function notification_info() {

}

function notification_err(message) {
    $.notify(message, {
        element: 'body',
        type: 'danger',
        timeout: 3000,
        animate: {
            enter: 'animated bounceIn',
            exit: 'animated bounceOut'

        }
    })
}

function notification_warn() {

}


function render_svg(jdata, svg_elem) {
    var svg = d3.select(svg_elem),
        width = +svg.attr("width"),
        height = +svg.attr("height");

    var color = d3.scaleOrdinal(d3.schemeCategory20);

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) {
            return d.id;
        }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    /* Arrow start */
    svg.append("defs").selectAll("marker")
        .data(["suit", "licensing", "resolved"])
        .enter().append("marker")
        .attr("id", function (d) {
            return d;
        })
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 25)
        .attr("refY", 0)
        .attr("markerWidth", 4)
        .attr("markerHeight", 4)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5 L10,0 L0, -5")
        .style("stroke", "#4679BD")
        .style("opacity", "0.4");
    /* Arrow end */

    var link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(jdata.links)
        .enter().append("line")
        .style("stroke-width", function (d) {
            return Math.sqrt(2);
        })
        .style("marker-end", "url(#suit)");
    /* Arrow */

    var node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(jdata.nodes)
        .enter().append("circle")
        .attr("r", 7)
        .attr("fill", function (d) {
            return color(d.group);
        })

        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended))
        .on('dblclick', connectedNodes)
        .on('click', showProperty);


    node.append("title")
        .text(function (d) {
            return d.id
        })
        .attr("name", function (d) {
            return d.group
        });

    simulation
        .nodes(jdata.nodes)
        .on("tick", ticked);


    simulation.force("link")
        .links(jdata.links);


    function ticked() {
        link
            .attr("x1", function (d) {
                return d.source.x;
            })
            .attr("y1", function (d) {
                return d.source.y;
            })
            .attr("x2", function (d) {
                return d.target.x;
            })
            .attr("y2", function (d) {
                return d.target.y;
            });

        node
            .attr("cx", function (d) {
                return d.x;
            })
            .attr("cy", function (d) {
                return d.y;
            });
    }

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }


    var toggle = 0;
    //Toggle stores whether the highlighting is on
    //Create an array logging what is connected to what
    var linkedByIndex = {};
    for (i = 0; i < jdata.nodes.length; i++) {
        linkedByIndex[i + "," + i] = 1;
    }

    jdata.links.forEach(function (d) {
        linkedByIndex[d.source.index + "," + d.target.index] = 1;
    });

    //This function looks up whether a pair are neighbours
    function neighboring(a, b) {
        return linkedByIndex[a.index + "," + b.index];
    }

    function connectedNodes() {

        if (toggle === 0) {
            //Reduce the opacity of all but the neighbouring nodes
            d = d3.select(this).node().__data__;
            node.style("opacity", function (o) {
                return neighboring(d, o) | neighboring(o, d) ? 1 : 0.1;
            });
            link.style("opacity", function (o) {
                return d.index === o.source.index | d.index === o.target.index ? 1 : 0.1;
            });
            //Reduce the op
            toggle = 1;
        } else {
            //Put them back to opacity=1
            node.style("opacity", 1);
            link.style("opacity", 1);
            toggle = 0;
        }
        return true
    }


    searchNode(jdata, svg);
    /* Search resources in topology */

    $('#switch_move').on('click', function () {

        switchMovement(simulation)
    });

}


function searchNode(jdata, svg_obj) {

    var optArray = [];
    for (var i = 0; i < jdata.nodes.length - 1; i++) {
        optArray.push(jdata.nodes[i].id);
    }
    optArray = optArray.sort();
    $(function () {
        $("#search").autocomplete({
            source: optArray
        });
    });

    $('#searchnode').on('click', function () {

        var selectedVal = document.getElementById('search').value;
        var node = svg_obj.selectAll(".nodes circle");
        if (selectedVal === "none") {
            node.style("stroke", "red").style("stroke-width", "1");
        } else {
            var selected = node.filter(function (d, i) {
                return d.id !== selectedVal;
            });
            selected.style("opacity", "0");
            var link = svg_obj.selectAll(".links line");
            link.style("opacity", "0");
            d3.selectAll(".nodes circle, .links line").transition()
                .duration(35000)
                .style("opacity", 60);
        }
    });
}


/* Switch on/off D3 layout force start/stop - Freeze the circle or make it moving again */
function switchMovement(simulateObj) {
    var interval_id;
    var running = false;
    clearInterval(interval_id);
    running = !running;
    if (!running) return;

    interval_id = setInterval(function () {
        simulateObj.alpha(0.6);
    }, 500);

}


function showProperty() {

    $('#collapseProperty').collapse('show');

    selectItem = $(this).children('title').text();
    selectType = $(this).children().attr('name');
    ep = '/resources';
    if (selectType === 'Node') {
        ep = '/resources/nodes';
    }
    if (selectType === 'Pod') {
        ep = '/resources/pods';
    }
    if (selectType === 'ReplicationController') {
        ep = '/resources/rcontrollers';
    }
    if (selectType === 'Service') {
        ep = '/resources/services';
    }

    $.ajax({
        url: 'http://192.168.151.15:5555/cluster' + ep,
        type: 'get',
        success: function (response) {
            ret = response.resources;
            $.each(ret, function (idx, data) {
                if (selectType + ':' + data.id === selectItem) {
                    var html = '<tr><td>ID</td><td>' + data.id + '</td></tr>';

                    for (var key1 in data.properties.metadata.annotations) {
                        var value1 = data.properties.metadata.annotations[key1];
                        html += '<tr><td>Annotations</td><td>' + key1 + ' : ' + value1 + '</td></tr>';
                    }
                    for (var key2 in data.properties.metadata.labels) {
                        var value2 = data.properties.metadata.labels[key2];
                        html += '<tr><td>Label</td><td>' + key2 + ' : ' + value2 + '</td></tr>';
                    }

                    html += '<tr><td>Name</td><td>' + data.properties.metadata.name + '</td></tr>';
                    html += '<tr><td>selfLink</td><td>' + data.properties.metadata.selfLink + '</td></tr>';
                    html += '<tr><td>UID</td><td>' + data.properties.metadata.uid + '</td></tr>';
                    html += '<tr><td>Type</td><td>' + selectType + '</td></tr>';
                    $('#prop-tbody').empty().append(html)


                }
            })
        }
    })

}

function editTable(arr) {

    var table = $('#showAllHPA_table').DataTable();

    table.MakeCellsEditable({
        "onUpdate": onUpdateCallBack,
        "columns": [arr[0], arr[1], arr[2]],
        "inputCss": 'my-input-class',
        "confirmationButton": {
            "confirmCss": 'my-confirm-class',
            "cancelCss": 'my-cancel-class'
        },
        "inputTypes": [
            {
                "column": arr[0],
                "type": "text",
                "options": null
            },
            {
                "column": arr[1],
                "type": "text",
                "options": null

            },
            {
                "column": arr[2],
                "type": "text",
                "options": null

            }

        ]
    });


}

function onUpdateCallBack(updatedCell, updatedRow, oldValue) {
    var field_dict = {};
    var keys = Object.keys(updatedRow.data());

    for (i = 0; i < keys.length; i++) {
        if (updatedRow.data()[keys[i]]) {
            field_dict[keys[i]] = updatedRow.data()[keys[i]]
        }
    }

    update_table(field_dict); //field_list is Object to be passed.
}


function select_host_detail(uid, hostname) {

    $('#node_detail_modal').modal('show');
    $('#node_detail_modal_label').text(hostname);
    $('#node_detail_box').empty();
    $('#nodeDetailSaveChange').addClass('invisible');
    $.ajax({
        url: '/nodes/details/' + uid + '/',
        type: 'post',
        data: {'hostname': hostname},

        success: function (e) {

            ret = JSON.parse(e);

            $('#node_detail_modal').on('shown.bs.modal', function (e) {


                $('#node_detail_box').empty();

                var jsonbox = document.getElementById('node_detail_box');
                var options = {
                    "mode": "tree",
                    "indentation": 2,
                    "search": true,
                    "onChange": onchange
                };
                var editor = new JSONEditor(jsonbox, options);
                editor.set(ret.data);
                // editor.expandAll();

                function onchange() {
                    $('#nodeDetailSaveChange').removeClass('invisible')
                }
                $('#nodeDetailSaveChange').on('click', function () {
                    var jsonChanged = editor.get();

                    update_node_detail(jsonChanged, hostname, uid);
                });

            })

        }

    })
}

function get_all_ns(elem) {

        $.ajax({
            url: '/get_all_ns/',
            type: 'get',
            success: function (data) {
                ret = JSON.parse(data);
                $.each(ret.data, function (idex, e) {
                    $(elem).append("<option>"  + e.ns_name + "</option>")
                });

            }
        })

    }

