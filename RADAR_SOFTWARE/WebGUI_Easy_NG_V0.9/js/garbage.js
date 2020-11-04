// drawing Z-Lines between the rangedatasets
function drawZLines(x, y, laenge)
{
        
    var zline = new THREE.Group();
    zline.className = 'cfar';
            
    //console.log(item)
    var material = new THREE.LineBasicMaterial({color: '#ededed'});
    var geometry = new THREE.Geometry();
    geometry.vertices.push(new THREE.Vector3(x, y, 0));
    geometry.vertices.push(new THREE.Vector3(x, y, -(laenge)));

    var line = new THREE.Line(geometry, material);

    zline.add(line);
    scene1.add(zline)
    
    
    
}


// get all Gridlines on the bottom going to the background
for (i = 0; i < scene1.children.length; i++)
    {
        if (scene1.children[i].type == 'Group')
        {   
            
            if (scene1.children[i].name == 'GridXZ')
            {
                var GridXZ = scene1.children[i].children
                
                GridXZ.forEach(function(item)
                {
                    if (item.className == 'tobackground')
                    {
                                                
                        console.log(item.geometry.vertices[0].y)
                        //item.geometry.vertices[0].y = SplinePoint.y
                    }
                    
                })
            }
        }
    }



//Stringparser
function parsemultipleStringFrames(datastr)
{
    var data = datastr.split('!');
    data.forEach(function(item){
            parseStringData(item)
                })
}
function parseStringData(data)
{
    var cmd = data[0];
    if (cmd === 'R') {
        parseRangeString(data);
        
    }
    if (cmd === 'C') {
        parseCfarString(data);
    }
    if (cmd === 'T') {
        parseTargetString(data);
    }
    if (cmd === 'U') {
        parseStatusString(data);
    }
    if (cmd === 'P') {
        
    }
}


function parseRangeString(Rstring)
{
    var rangestr = "!"+ Rstring;
    
    var strData = rangestr.split('')
    var view = []
    strData.forEach(function(item){
        view.push(item.charCodeAt())
    })
    zeichneRangeFrame(view, '#0772a1', 'rangeframe')
}


function parseCfarString(CString)
{
    var CfarStr = "!"+ CString;
    
    var strData = CfarStr.split('')
    var view = []
    strData.forEach(function(item){
        view.push(item.charCodeAt())
    })
    zeichneRangeFrame(view, '#ededed', 'cfar')
}

function parseTargetString(targetstr)
{
    if (($('#2Dradio').is(":checked")) == true) { deleteOldArrows();}
    else 
    {
        fadeaway(Backsteps, Sichtweite, 'targetarrows');
    }
    
    var format = targetstr[1]; var formatstr = "";
    
//    if (format == 0) {  format = "raw A/D"   }
//    if (format == 1) {  format = "FFT comp"   }
//    if (format == 2) {  format = "FFT mag/ph"   }
//    if (format == 3) {  format = "CFAR"   }
    if (format == 4) {  formatstr = "bin"   }
    if (format == 5) {  formatstr = "mm"    }
    if (format == 6) {  formatstr = "cm"   }
    //if (format == 7) {  format = "reserved"}
    
    $('#EinheitsLabel').html(formatstr);
    //addText('distance in: ' + format, 200, -184, 0.1, 6, 'distanzlabel');
    
    var gainDB = targetstr[3];
    var targets = targetstr.substring(3, targetstr.length-4);
    
    parseTargetData(targets, format);
    

}
function parseStatusString(str)
{
    str = '!' + str;
    var gainDB = str.substring(1, 2);
    accuracy = parseInt(str.substring(2, 6), 16);
    accuracy /= 10;
    
    $('#accuracyLabel').html(accuracy);
    var laenge = parseInt(str.substring(6, 10), 16);
    $('#FFTsizeLabel').html(laenge);
    $('#StatusMaxRange').html(laenge);
        
    if (maxrange !== laenge)
    {
        maxrange = laenge;
        gridanpassen(maxrange);
    }
    
    
    var Ramptime = parseInt(str.substring(10, 14), 16);
    var Bandwith = parseInt(str.substring(14, 18), 16);
    var TSLM = parseInt(str.substring(18, 22), 16);

    var steps = parseInt(maxrange / accuracy, 10);

}









//YLabels und Marker extra als THREE.Group

    var YLabels = new THREE.Group();
    YLabels.className = "Achse";
    for (var i = min; i <= max; i += step)
    {
        var textGeo = new THREE.TextGeometry(i.toString(), {size: fontsize, height: 0.05, curveSegments: 6, font: "helvetiker", style: "normal"});
        var color = new THREE.Color();
        color.setRGB(255, 250, 250);

        var textMaterial = new THREE.MeshBasicMaterial({color: color});
        var Text = new THREE.Mesh(textGeo, textMaterial);
        Text.position.set(x, i * y, 0);        
        if (($('#2Dradio').is(":checked")) == false) { Text.rotation.y = camera1.rotation.y}       
        YLabels.add(Text);
        //scene1.add(Text);
    }
    
    
    for (var i = min; i <= max; i += step)
    {
        var color = new THREE.Color(); color.setRGB(255, 250, 250);
        var material = new THREE.LineBasicMaterial({color: color});
        var geometry = new THREE.Geometry();
        geometry.vertices.push(new THREE.Vector3(0, i * y, 0));
        geometry.vertices.push(new THREE.Vector3(3 * Scale, (i * y), 0));
        var line = new THREE.Line(geometry, material);        
        YLabels.add(line);
    }
    scene1.add(YLabels);

/**
 * 
 * @param {number} size the maximal size of the grid
 * @param {number} step the size of rectangles of the grid / the spaces between the lines
 * @param {number} y    the y-coordinate for where the grid is going to be drawn
 * @returns {undefined}
 */
function drawGridhelper(size, step, y, Scale)
{
    if (($('#2Dradio').is(":checked")) == false)
    {

        var color = new THREE.Color(0x9B978C);
        color.setRGB(0.53333333, 0.53333333, 0.53333333);
        var gridXZ = new THREE.GridHelper(size/2, step);
        gridXZ.setColors(color, color);
        gridXZ.className = "Achse";
        //gridXZ.id = "gridXZ";
        gridXZ.position.y = y;
        gridXZ.position.x = parseInt(size/2);
        gridXZ.position.z = parseInt(-size/2);
        scene1.add(gridXZ);

	var gridYZ = new THREE.GridHelper(140 * Scale, 20 * Scale);
	gridYZ.setColors( color, color );
        gridYZ.position.set(0, -0.01 * Scale, -140*Scale)
	gridYZ.rotation.z = Math.PI/2;
	gridYZ.className = "Achse";
        gridYZ.id = "gridYZ"
	scene1.add(gridYZ);        
        
        // var gridXY = new THREE.GridHelper(500, 10);
        // gridXY.rotation.x = Math.PI/2;
        // scene.add(gridXY);
    }
}

//Spectrogramm mit partikelsystem

    var particles = new THREE.Geometry;
    particles.colors = colors;
    var particleMaterial = new THREE.PointsMaterial(
        { 
            vertexColors: THREE.VertexColors, 
            size: 0.1 
    
        });
        
    var particleSystem = new THREE.Points(particles, particleMaterial);
    Arr.forEach(function(item, index){
        var DB = (((parseInt(item, 10)-174) * Scale));
        
        var particle = new THREE.Vector3(index, DB, 0.1);
        particles.vertices.push(particle);
    });
    scene1.add(particleSystem);



 var TargetColorsOrange =
 [
 '#ff1a00', '#ff2a00', '#ff3a00', '#ff4a00',
 '#ff5a00', '#ff6a00', '#ff7a00', '#ff8a00',
 '#ff9a00', '#ffaa00', '#ffba00', '#ffca00',
 '#ffda00', '#ffea00', '#fffa00', '#f4ff00'
 ];
 var TargetColorsBlue =
 [
 '#00e2ff', '#00d2ff', '#00c2ff', '#00b2ff',
 '#00a2ff', '#0092ff', '#0082ff', '#0072ff',
 '#0062ff', '#0052ff', '#0042ff', '#0032ff',
 '#0022ff', '#0012ff', '#0002ff', '#0002ff'
 ]
 TargetColorsBlue.sort();



function vergleiche(char1, char2, char3, char4)
{
    var length, maxrange;
    var vergleicheRange = new Promise
            (
                    function (resolve, reject)
                    {
                        maxrange = $('#FFTsizeLabel').html();
                        length = parseInt(char1 + char2 + char3 + char4, 16);
                        window.setTimeout(function ()
                        {

                            if (length != 'undefined' && maxrange != 'undefined') {
                                resolve('success');
                            } else {
                                reject(Error("It broke"));
                            }

                        }, 0);

                    }
            );
    vergleicheRange.done(
            function (result)
            {
                if (result == 'success')
                {
                    //console.log ('vergleiche ' + maxrange + ' : ' + length)
                }
                if (length != maxrange)
                {
                    $('#FFTsizeLabel').html(length);
                    gridanpassen(length);
                }
            }
    , function (err)
    {
        console.log(err); // Error: "It broke"
    });
}

function hitborder()
{
    $('body').mousemove(function (ev)
    {
        if (parseInt(ev.pageX) < 10)
            showmenu();
        if (parseInt(ev.pageY) < 10)
            showinfobar();

    }
    )
}