var width = window.innerWidth * .8,
    height = window.innerHeight * .8,
    root,
    gravity = 0.2,
    charge = -1800,
    linkStrength = 1,
    count = 0,
    root_element, linkDistance = width * 0.05;

window.addEventListener("resize", updateWindow);

function updateWindow() {
    width = window.innerWidth;
    height = window.innerHeight;
    svg.attr("width", width * .8).attr("height", height * .8);
}
d3.select(window).on('resize', updateWindow);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("id", "graph");

var link = svg.selectAll("link"),
    node = svg.selectAll("node");

var div = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

var force = d3.layout.force()
    .linkDistance(linkDistance)
    .charge(charge)
    .gravity(gravity)
    .linkStrength(linkStrength)
    .size([width, height])
    .on("tick", tick);


d3.json("/graph_gen_sample.json", function(error, json) {
    if (error) throw error;
    root = json;
    // root.fixed = true;
    root_element = root.name;
    update();
});



function update() {
    var nodes = getNodes(root),
        links = d3.layout.tree().links(nodes);

    force
        .nodes(nodes)
        .links(links)
        .start();

    node = node.data(nodes, function(d) {
        return d.id;
    });

    var startTime;
    var endTime;

    var nodeEnter = node.enter().append("g")
        .attr("class", "node")
        .on('mousedown', function() { startTime = new Date(); })
        .on('mouseup', function(d) {
            endTime = new Date();
            if ((endTime - startTime) < 300) {
                click(d);
            }
        })
        .call(force.drag);

    nodeEnter.append('image')
        .attr('xlink:href', function(d) {
            return '/app/static/graph_imgs/' + get_name(d.name) + ".png";
        })
        .attr("x", function(d) { return -25; })
        .attr("y", function(d) { return -25; })
        .attr("height", 50)
        .attr("width", 50);

    nodeEnter.append("text")
        .attr("dy", function(d) { return 40; })
        .attr("dx", function(d) { return -25; })
        .attr("class", "texts")
        .text(function(d) {
            return d.name;
        });

    node.exit().remove();


    link = link.data(links, function(d) {
        return d.target.id;
    });

    link.exit().remove();

    link.enter().insert("line", ".node")
        .attr("class", "link");

}

function click(d) {

    if (d.children) {
        d._children = d.children;
        d.children = null;
    } else {
        d.children = d._children;
        d._children = null;
    }
    update();
}

function isDirectChild(val) {

    for (var key in root.children) {
        if ((root.children[key].name) == val)
            return true;
    }
    return false;

}

function tick() {

    link.attr("x1", function(d) {

            if (d.source.name.value == d.root_element && (isDirectChild(d.target.name))) {
                return width / 2;
            }
            return d.source.x;
        })
        .attr("y1", function(d) {
            if (d.target.name.value == d.root_element && (isDirectChild(d.target.name))) {
                return height / 2;
            }
            return d.source.y;
        })
        .attr("x2", function(d) {
            return d.target.x;
        })
        .attr("y2", function(d) {
            return d.target.y;
        });

    node.attr("transform", function(d) {
        let translate;
        if (root_element != d.name) {

            translate = "translate(" + d.x + "," + d.y + ")";
        } else if (d.y > height || d.x > width) {
            d.x = Math.max(50, Math.min(width, d.x));
            d.y = Math.max(25, Math.min(height - 25, d.y));
            translate = "translate(" + d.x + "," + d.y + ")";

        } else {
            translate = "translate(" + width / 2 + "," + height / 2 + ")";

        }
        return translate;
    });
}

function getNodes(root) {
    var nodes = [],
        i = 0;


    function recurse(node) {
        if (node.children) node.children.forEach(recurse);
        if (!node.id) node.id = ++i;
        nodes.push(node);
    }
    recurse(root);
    return nodes;
}

function get_name(name) {
    let isNum = false
    let lastChar;
    while (!isNum) {
        lastChar = name.substr(-1);
        if (isNaN(lastChar)) {
            return name;
        } else {
            name = name.substr(0, name.length - 1)
        }
    }
}

function update_nodeDistance(val) {
    let newLinkDistance = linkDistance * (val / 10);
    force
        .linkDistance(newLinkDistance)
        .start();
}


function update_attraction(val) {
    force
        .charge(val)
        .start();
}

function update_stiffness(val) {
    force
        .gravity(val)
        .start();
}