
//#1 we collected some points
function process( points ) {

    //not enough points: bail out
    if (points.length < 3)return;

    //there are enough points to compute something
    //first make sure there are no duplicates ( create a point set )
    points = cleanup(points);


//#2 second compute the delaunay triangulation on the set
    var tris = delaunay.compute(points);

//#3 compute the edges lengths and associate the endpoints
    edges = [];
    for (var i = 0; i < tris.length; i += 3) {
        var p0 = points[tris[i]];
        var p1 = points[tris[i+1]];
        var p2 = points[tris[i+2]];
        edges.push(
            [distance(p0, p1), p0, p1],
            [distance(p1, p2), p1, p2],
            [distance(p2, p0), p2, p0]
        );
    }

    render();
}

function render() {

    //reset the canvas
    ctx.restore();
    ctx.save();
    ctx.globalAlpha = 1;
    ctx.fillStyle = "#FFF";
    ctx.fillRect(0, 0, w, h);

//#4 draw the gradient
    ctx.save();
    var max = config.height;
    for (i = 0; i < max; i++) {

        //#4.1
        ctx.translate(0, 1);
        ctx.globalAlpha = ( 1 - i / max ) * 0.05;

        //#4.2
        renderEdges(edges, i);
    }
    ctx.restore();

//#5 render the wireframes
    if (config.wireframe) {

        var m = config.wireCount;
        for (i = 0; i < m; i++) {

            var t = ( i / m );
            ctx.globalAlpha = .05 + .15 * t;

            ctx.save();
            ctx.translate(0, max * ( 1 - t ));
            renderEdges(edges, (i * 10) );
            ctx.restore();
        }
    }

//#6 draw a color overlay
    ctx.save();
    ctx.globalAlpha = 1;
    ctx.globalCompositeOperation = "screen";
    var cw = canvas.width;
    var ch = canvas.height;
    //draw the image over the whole image
    ctx.drawImage(img, 0, 0, img.width, img.height, 0,0,cw,ch);
    ctx.restore();

//#7 white wireframe
    if( config.glow ){

        ctx.globalCompositeOperation = "source-over";
        ctx.strokeStyle = "#FFF";
        ctx.globalAlpha = .2;
        renderEdges(edges, config.glowSize / 2);

        //white glow
        ctx.globalCompositeOperation = "screen";
        ctx.globalAlpha = 1;
        ctx.filter = "blur( 6px )";
        renderEdges(edges, config.glowSize );
    }

}

//the method to render
function renderEdges(edges, min ){
    if( edges.length == 0 )return;
    ctx.beginPath();
    //for each edge of the list
    for( var i=0; i < edges.length; i++ ){
        var edge = edges[ i ];

        //if the edge's length is inferior to the given threshold
        if( edge[ 0 ] < min ){

            //draw a line between endpoints
            ctx.moveTo( edge[ 1 ].x, edge[ 1 ].y);
            ctx.lineTo( edge[ 2 ].x, edge[ 2 ].y);
        }
    }
    ctx.stroke();
}



var w = window.innerWidth;
var h = window.innerHeight;
var canvas,ctx,img, points =  [], edges, config;
window.onload = function() {

    //image used as overlay

    img = document.getElementById("img");
    document.body.removeChild( img );

    //canvas

    w = window.innerWidth;
    h = window.innerHeight;

    canvas = document.createElement("canvas");
    canvas.width  = w;
    canvas.height = h;
    ctx = canvas.getContext("2d");
    document.body.appendChild( canvas );

    //controls

    config = function(exports) {
        exports.radius = 25;
        exports.count = 5;
        exports.height = 0xFF;
        exports.wireframe = true;
        exports.wireCount = 4;
        exports.glow = true;
        exports.glowSize = 20;
        exports.clear = function () {
            points = [];
            edges = [];
            render();
        };
        return exports;
    }({});

    var gui = new dat.GUI();
    var draw = gui.addFolder( "draw");
    draw.add( config, 'radius', 1, 250);
    draw.add( config, 'count', 1, 25);
    draw.open();

    var rendering = gui.addFolder('render');
    rendering.add( config, 'height', 1, 512 ).onChange( function(){render();});
    rendering.add( config, 'wireframe').onChange( function(){render();});
    rendering.add( config, 'wireCount', 1, 15 ).onChange(function(){render();});

    rendering.add( config, 'glow' ).onChange(function(){render();});
    rendering.add( config, 'glowSize', 1, 60 ).onChange(function(){render();});


    rendering.add( config, 'clear');
    rendering.open();


    //mouse/touch

    var hammer = new Hammer( canvas );
    hammer.on( "tap pan panend", function(e){

        if( e.type == "tap" || e.type == "pan" ){
            var x,y;
            var radius = config.radius;
            var count = config.count;

            if( e.type == "pan" ){
                radius = 1;
                count = 1;
            }

            for( var i = 0; i < count; i++ ){

                x = e.center.x + ( Math.random() - .5 ) * radius;
                y = e.center.y + ( Math.random() - .5 ) * radius;
                points.push( {x:x, y:y } );

            }
            if( e.type == "tap" )process( points );

        }else{
            process( points );
        }

    });

};

//compute the distance between point A & B
function distance( a,b ){
    var dx = a.x - b.x;
    var dy = a.y - b.y;
    return Math.sqrt( dx*dx+dy*dy );
}

//remove duplicate points
function cleanup( ps ){
    var tmp = [];
    ps.forEach( function (p){
        var valid = true;
        tmp.forEach( function (o ){
            if( !valid )return;
            if( p.x == o.x && p.y == o.y )valid = false;
        });
        if( !valid )return;
        tmp.push( p );
    });
    return tmp;
}
