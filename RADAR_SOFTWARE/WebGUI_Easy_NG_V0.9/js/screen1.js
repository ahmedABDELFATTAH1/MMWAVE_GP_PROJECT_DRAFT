

/**
 * @fileOverview script for Everything what needs to be drawn in the 3D-Scene from Three.js
 * 
 */

/**
 *  Initialize the Scene
 */
function initscreen1() {
    
    // creating the Scene
    scene1 = new THREE.Scene();
    scene1.id = 'scene1';

    // Define the perspective camera's attributes.
    var fieldofview = 70; // the vertical angle of the FoV
    var scenewidth = window.innerWidth;
    var sceneheight = window.innerHeight;
    var aspectratio = scenewidth / sceneheight;
    
    var near = 0.1; var far = 5000;
    camera1 = new THREE.PerspectiveCamera(fieldofview, aspectratio, near, far);

    // Fallback to canvas renderer, if necessary.
    renderer1 = window.WebGLRenderingContext ? new THREE.WebGLRenderer({alpha: true}) : new THREE.CanvasRenderer({alpha: true});
    renderer1.id = "renderer1";
    //renderer1.setPixelRatio( window.devicePixelRatio );

    // Append the WebGL viewport to the DOM.
    c = $("#canvascontainer").prepend(renderer1.domElement);

    // set the Color of the background color, 2. parameter for opacity
    renderer1.setClearColor(0x000000, 0);

    //add Orbitcontrols
    controls = new THREE.OrbitControls(camera1, renderer1.domElement);
//    mousewheelzoom();    
//    MoveCam();
//    touchstart();
    

    // set the camera position, set the size of the WebGL viewport.
    resetview();
    addDatGUI();
    

    // Start the rendering of the animation frames.
    render1();
    
}


/**
 *   @description 
 *   function for the rendering loop,
 *   call the render() function up to 60 times per second (i.e., up to 60 animation frames per second). 
 */
function render1() {
    
   
        renderer1.render(scene1, camera1);                
        if ($('#rotateSceneX').is(':checked')) 
        {
            // scene1.rotation.x += 0.001; 
            controls.autoRotate = true;
            controls.update();
        }
                        
    animationreq = requestAnimationFrame(render1);         
    

}

/**
 * function to let the old data go to the background each time new data comes in
 * @param {int} abstand the distance to go back each time data comes in
 * @param {int} maxlength the maximal distance to display on the z-axis
 */
function fadeaway(abstand, maxlength, itemtype) {

    
    // loeschen des lots und des distanzlabels, wenn datenreihe nach hinten geschoben wird
//    for (i = scene1.children.length - 1; i > 0; i--)
//    {
//        if (scene1.children[i].className == "lot" || scene1.children[i].className == "distanzlabel" || scene1.children[i].position.z < -maxlength) {
//            scene1.remove(scene1.children[i])
//        }
//
//    }
   

    //if (linecount !== 0)
    {
        
        linecount = 0;
        for (var x = scene1.children.length - 1; x > 0; x--)
        {

            //console.log('verschiebe: '+itemtype)
            
            if (scene1.children[x].className == itemtype)
            {
                scene1.children[x].position.z -= abstand;
                                
                if (scene1.children[x].position.z < -maxlength)
                {
                    scene1.remove(scene1.children[x]);
                    scene1.children[x].geometry.dispose();
                    scene1.children[x].material.dispose();
                     
                }
            }

        }


    }
    //maketransparent(abstand, maxlength);


}


/**
 * makes the objects more and more transparent when they move to the background
 * @param {Number} abstand the z-distance between two datasets
 * @param {Number} maxlength the maximum distance things are going to be displayed
 * @param {string} datatype what kind of datatype, for example 'cfar'
 * @returns {undefined}
 */
function maketransparent(abstand, maxlength, datatype)
{
    var anzahl = parseInt(maxlength / abstand);
    var transpdiff = 1 / (anzahl + (abstand / 2));
    
    //make Waves transparent in Background
     if ($('#3Dradio').is(":checked") == true)
     {
     scene1.children.forEach(function(l)
     {
        if (l.className == datatype && spectrogramm === false)
        {
        //console.log(l.material.transparent);
        l.material.transparent = true;
        l.material.opacity -= transpdiff*2;
        }
     });

   }
   
   for (i = 0; i < scene1.children.length; i++)
    {

        if (scene1.children[i].className !== "Achse")
        {
            
            if (($('#targetview').is(":checked")) == true)
            {
                scene1.children[i].children.forEach(function (s)
                {
                    //console.log(s.material);
                    s.material.transparent = true;
                    s.material.opacity -= transpdiff;
                });
            }



        }
    }
}
/**
 * deletes the old data if the "2D"-View is activated
 */
function deleteolddata(datatype)
{
    // delete the old Data ==> so no fadeaway to the background
   
        for (var x = scene1.children.length - 1; x > 0; x--)
        {
            
            if (scene1.children[x].className == datatype)
            {                                                
                    scene1.remove(scene1.children[x]);
                    //scene1.children[x].geometry.dispose();
                    //scene1.children[x].material.dispose();
                     
            }

        }
        
        
        //deleting again: one after the other
        scene1.children.forEach(function (item, index, object)
        {
            if (item.className == datatype) 
            {   
                //object.splice(index, 1);                
                scene1.remove(item);
                item.geometry.dispose();
                item.material.dispose();
                //item.texture.dispose();                
                //item = null;
                
            }
        });
    
   
}
/**
 * deletes all old arrows, when the View is 2D
 * @returns {undefined}
 */
function deleteOldArrows()
{
    for (var i = scene1.children.length - 1; i > 0; i--)
        {
            if (scene1.children[i].className == "targetarrows") 
            {
                scene1.remove(scene1.children[i])
//                scene1.children[i].geometry.dispose();
//                scene1.children[i].material.dispose();                        
//                scene1.children[i] = null;
            }

        }
}

/**
 * drawing the axis and Labels
 */
function zeichneachsen(size, step, fontsize, TextYcoord) {
    size = parseFloat(size);
    step = parseFloat(step);
    //console.log('zeichne Achsen')
    // mehr Genauigkeit/Nachkommastellen bei kleinerer maxrange
	
    if (size < 128)
    {
        addaxeslabels(size, parseFloat(step), fontsize, TextYcoord);
    } else
    {
        addaxeslabels(size, parseInt(step, 10), fontsize, TextYcoord);
    }
	

    
}


/**
 * function for drawing the 3D-Grid
 * @param {number} size the maximal size of the grid
 * @param {number} step the size of steps on the x-axis
 * @param {number} y    the y-coordinate for where the grid is going to be drawn
 * @returns {undefined}
 */
function drawGrid(size, step, y, Scale)
{
    var timedelta = Backsteps / Scale;
    var GridGroupXZ = new THREE.Group();
    var GridGroupYZ = new THREE.Group();
    var transparency = 0.2;
    
    //add lines from the x-axis to the background
    for (i = 0; i <= size; i += step)
    {
        var material = new THREE.LineBasicMaterial({color: 'white', transparent: true});
        material.opacity = transparency;
        var geometry = new THREE.Geometry();
        geometry.vertices.push(new THREE.Vector3(i,y,0));
        geometry.vertices.push(new THREE.Vector3(i,y, -size));

        var line = new THREE.Line(geometry, material);
        line.className =  'tobackground';
        GridGroupXZ.add(line);
    }
    // add horizontal lines
    for (var i = timedelta * Scale; i < size; i += timedelta * Scale)
    {
        var material = new THREE.LineBasicMaterial({color: 'white', transparent: true});
        material.opacity = transparency;
        var geometry = new THREE.Geometry();
        geometry.vertices.push(new THREE.Vector3(0,y,-i));
        geometry.vertices.push(new THREE.Vector3(size,y, -i));

        var line = new THREE.Line(geometry, material);
        line.className =  'horizontal';
        GridGroupXZ.add(line);
    }
    
    // add GridYZ
    // horizontal lines
    for (var i = y; i <= (140 * Scale * 2); i += 20 * Scale * 2)
    {
        var material = new THREE.LineBasicMaterial({color: 'white', transparent: true});
        material.opacity = transparency;
        var geometry = new THREE.Geometry();
        geometry.vertices.push(new THREE.Vector3(0,i,0));
        geometry.vertices.push(new THREE.Vector3(0,i, -size));

        var line = new THREE.Line(geometry, material);
        //line.className = 'Achse';
        GridGroupYZ.add(line);
    }
    
    //  vertical lines
    for (var i = timedelta * Scale; i <= size; i += timedelta * Scale)
    {
        var material = new THREE.LineBasicMaterial({color: 'white', transparent: true});
        material.opacity = transparency;
        var geometry = new THREE.Geometry();
        geometry.vertices.push(new THREE.Vector3(0, y , -i));
        geometry.vertices.push(new THREE.Vector3(0, 140 * Scale * 2, -i));
        var line = new THREE.Line(geometry, material);
        //line.className = 'Achse';
        GridGroupYZ.add(line);
    }
    GridGroupXZ.className = 'Achse'; GridGroupYZ.className = 'Achse';
    GridGroupXZ.name = 'GridXZ'; GridGroupYZ.name = 'GridYZ';
    scene1.add(GridGroupXZ);
    scene1.add(GridGroupYZ)
}
/**
 * drawing the x, y and z- axis using the three.js "axishelper"
 * @param {number} size the maximal length of the axis
 * @param {number} y the y-coordinate where the axis should be drawn
 * @returns {undefined}
 */
function drawAxishelper(size, y)
{
    Achsen = new THREE.Group();
    Achsen.id = 'Axes';    
    
    var axes = new THREE.AxisHelper(size);
    axes.position.y = y;
    axes.className = "Achse";
    axes.id = "Achse" + size;
    axes.rotation.set(0, Math.PI/2, 0)
    scene1.add(axes);
}

/**
 * function for drawing the axes
 * @param {type} size
 * @param {type} y
 * @returns {undefined}
 */
function drawAxes(size, y)
{
    var colors = [];
    
    //var hwert = ( (DB-140+20) / -100)
    
    if ($('#DBcolorRadio').is(':checked'))
    {
        for (var i = -140; i < 0; i++)
        {
            colors[i+140] = new THREE.Color();            
            var hwert = ( i  / (-140));
            hwert = hwert * 100;
            colors[i+140].setHSL(hwert, 1.0, 0.5);
            
//            var hwert = ( (i+20) / -100)
//           colors[i+140].setHSL(hwert+0.2, 1.0, 0.5);
//            
//            
//            
            colors[i+140].setHex('0xFFFFFF')
            
        }
        //colors.forEach(function(item){ console.log(item.getHSL())  })
        
    }
    if ($('#PhaseRadio').is(':checked'))
    {
        
        for (var i = 0; i < 140; i++)
        {
            colors[i] = new THREE.Color();
            //colors[i].setHSL((100, 100, 100));
            colors[i].setHex('0xFFFFFF')
        }
    }
    
    
    
    var material = new THREE.LineBasicMaterial({
            transparent: true,
            vertexColors: THREE.VertexColors
        });
    var geometry = new THREE.Geometry();
    geometry.colors = colors;
    var Scale = scaleX(window.FFTSize)
    geometry.vertices.push(new THREE.Vector3(0,0,0));
    geometry.vertices.push(new THREE.Vector3(0, 140 * Scale * 2, 0));
    
    var line = new THREE.Line(geometry, material);
    line.className = 'Achse';
    scene1.add(line);
    
    //x-achse zeichnen
    zeichnelinie(new THREE.Vector3(0, 0, 0), new THREE.Vector3(size, 0, 0), '#FFFFFF', 'Achse' );
    //z-achse zeichnen
    if (($('#3Dradio').is(":checked")) == true)  { zeichnelinie(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, -size), '#404040', 'Achse' ) }
    
}

/**
 * adding Labels to the Axis
 * @param {number} size the size of the FFT in bin#
 * @param {number} step the size of the steps / same like for the gridhelper
 * @param {number} fontsize 
 * @returns {undefined}
 */
function addaxeslabels(size, step, fontsize)
{
    size = parseInt(size);
    //console.log(size)
    var width = parseInt($('#canvascontainer').css('width'));
    var hoehe = parseInt($('#canvascontainer').css('height'));
    var aspect = width / hoehe;
    //console.log('canvasheight : ' + hoehe)

    // vertikaler Blickwinkel
    var alpha = 70;
    var hFoV = size;
    var dist = (hFoV / Math.tan(alpha));
    var height = (dist * Math.tan(alpha));
    //console.log('height: ' + height);

    var Scale = scaleX(size);
    //add Labels for Y-Axis
    //addYLabels(-140, 0, 20, Scale, fontsize, size, Scale)
    addYLabels(0, 140, 20, Scale * 2, fontsize, size, Scale)
    //add Labels for X-Axis
    //addXLabels(step, size, -150 * Scale, fontsize, Scale)
    addXLabels(step, size, -10 * Scale, fontsize, Scale)
    //drawAxishelper(size, -140 * Scale );
    //drawAxishelper(size, 0.01 * Scale );
    drawAxes(size);
    //drawGridhelper(size, step, -140 * Scale, Scale);
    if (($('#3Dradio').is(":checked")) == true)
    {
//        drawGrid(size, step, -140 * Scale, Scale)
          drawGrid(size, step, 0, Scale)  
    }
    

}

/**
 * adding the Labels for the X-axis
 * @param {number} step the stepsize (going to be the X-coordinate)
 * @param {number} size the maximumsize, depending of the FFT-size
 * @param {number} y the y-coordinate where to draw the Label
 * @param {number} fontsize
 * @returns {undefined}
 */
function addXLabels(step, size, y, fontsize, Scale)
{
//	console.log("size " + size);
//	console.log("step " + step);
//	console.log(y);
//	console.log(fontsize);
//	console.log(Scale);
    
    for (j = step; j < size; j += step)
        {
            if ($('#EinheitsLabel').html() == 'bin')
            {
                addText((parseInt(j)).toString(), j, y , 0, fontsize, 'Achse', 'Achse' + size);
            }
            else
            {
                addText((parseInt(j * accuracy)).toString(), j, y , 0, fontsize, 'Achse', 'Achse' + size);
            }
            
            //add Markers to the axis
            zeichnelinie(new THREE.Vector3(j, 0, 0), new THREE.Vector3(j, (3 * Scale), 0), '#404040', 'Achse' )
        }
        // add Unit to the x-axes
        addText($('#EinheitsLabel').html().toString(), size, (15 * Scale) , 0, fontsize, 'Achse', 'Achse' + size);
}
/**
 * adding the Y-Labels to the scene
 * @param {type} min the minimum of the y-values to be displayed (-150)
 * @param {type} max the maximum of the y-values to be displayed (+80)
 * @param {type} step the steps between the Labels (actually 20)
 * @param {type} y the y-coordinate where to draw the Label, already scaled
 * @param {type} fontsize
 * @param {type} size
 * @returns {undefined}
 */
function addYLabels(min, max, step, y, fontsize, size, Scale)
{
    //Displaying the Labels left from the Y-axis depending on the scalelevel
    var x = -15 * Scale;
    
    for (i = min; i <= max; i += step)
        {
            addText((i - 140).toString(), x, i * y, 0, fontsize, 'Achse', 'Achse' + size);
            zeichnelinie(new THREE.Vector3(0, i * y, 0), new THREE.Vector3(3 * Scale, (i * y), 0), '#404040', 'Achse' )
        }

        addText('dB', 10 * Scale, 120 * Scale * 2, 0, fontsize, 'Achse', 'Achse' + size);
	
}


/**
 * function for generally adding Text to the scene
 * @param {string} textstr the string of Text to Add
 * @param {number} x the X-coordinate where the Text should be placed
 * @param {number} y the Y-coordinate where the Text should be placed
 * @param {number} z the Z-coordinate where the Text should be placed
 * @param {number} size the Fontsize
 * @param {string} label which className should the object get, needed later for deleting
 * @param {string} id not needed anymore, was used for deleting
 * @returns {undefined}
 */
function addText(textstr, x, y, z, size, label, id)
{
    var textGeo = new THREE.TextGeometry(textstr, {size: size, height: 0.05, curveSegments: 6, font: "helvetiker", style: "normal"});
    var color = new THREE.Color();
    color.setRGB(250, 250, 250);

    var textMaterial = new THREE.MeshBasicMaterial({color: color});
    var Text = new THREE.Mesh(textGeo, textMaterial);

    Text.position.x = x;
    Text.position.y = y;
    Text.position.z = z;
    
    
    // text.rotation = camera.rotation;
    Text.className = label;
    Text.name = 'AxisLabel'
    Text.id = id;

    scene1.add(Text);
}

function drawtargetpoints(targets)
{   
    var colors = [];
    
    for (var i = 0; i < targets.length; i++)
    {
        colors[i] = new THREE.Color();
        if ($('#RangeRadio').is(":checked"))
        {
            colors[i].setHex("0x" + (TargetColors[i]).replace("#", ""));
        }
        if ($('#DBcolorRadio').is(":checked"))
        {
            var DB = (targets[i].substring(5, 6).charCodeAt(0) - 174);
            
            var hwert = ( (DB+20) / -100)
            //console.log(hwert)
            colors[i].setHSL(hwert+0.2, 1.0, 0.5);
            //colors[i].setHex("0x" + (TargetColors[i]).replace("#", ""));
        }
        
    }
    
    var particles = new THREE.Geometry;
    particles.colors = colors; 
    
    
    var particleMaterial = new THREE.PointsMaterial(
    { 
        vertexColors: THREE.VertexColors, 
        size: 1 

    });
    var ScaleY = scaleY(window.FFTSize);
    var particleSystem = new THREE.Points(particles, particleMaterial);
    targets.forEach(function(targetstr, index){
        var targetnum = parseInt(targetstr.substring(0, 1), 16);
        var distanz = parseInt(targetstr.substring(1, 5), 16);
        var DBWert = (targetstr.substring(5, 6).charCodeAt(0) - 174);        
        DBWert = ((DBWert + 140) * ScaleY);        
        var particle = new THREE.Vector3( distanz / accuracy, DBWert, 0);
        if (distanz > 1) {particles.vertices.push(particle);}
        //if (targetnum === 15) {window.TTCounter++;}
    });
    particleSystem.className = "targetpoint";
    if (particles.vertices.length > 0) {  scene1.add(particleSystem); }
    
    shiftTargetPoints();
}
function drawTargetPoint(targetnum, distance, accuracy)
{
    
    var opa = 1;    
    var hexcolor = TargetColors[targetnum];
    //console.log(hexcolor);
    var material = new THREE.MeshBasicMaterial({transparent: true, opacity: opa, color: hexcolor});

    var radius = 1 * scaleX(window.FFTSize);
    var segments = 12;		// wieviel Teilflaechen der Kreis hat
    var thetaStart = 0;   //wo der Winkel anfaengt
    var thetaLength = Math.PI * 2;
    

    //console.log(radius);
    var circleGeometry = new THREE.CircleGeometry(radius, segments, thetaStart, thetaLength);
    var circle = new THREE.Mesh(circleGeometry, material);
    circle.position.x = distance / accuracy;
    circle.position.y = (0.1 * window.TTCounter);
    circle.position.z = 0;
    circle.className = "targetpoint";
    //circle.material.opacity = "0.2";
    scene1.add(circle);

}

function shiftTargetPoints()
{
    for (var x = scene1.children.length - 1; x > 0; x--)
        {

            //console.log('verschiebe: '+itemtype)
            if (scene1.children[x].className == "targetpoint")
            {
                scene1.children[x].position.z -= 0.1;
                                
                if (scene1.children[x].position.z < -(100))
                {
                    scene1.remove(scene1.children[x]);
                    scene1.children[x].geometry.dispose();
                    scene1.children[x].material.dispose();
                    
                }
            }

        }
}
/**
 * @deprecated not needed, 
 * function for drawing the phaseangles as parts of a circle
 * @param {type} distanz
 * @param {type} winkel
 * @param {type} DBWert
 * @param {type} hexcolor
 * @returns {undefined}
 */
function zeichnewinkel(distanz, winkel, DBWert, hexcolor) {
    //display targets with different opacity --> target 1 full, target 10 with 0.1
    //var opa = 1.1 - (targetnum / 10);
    var opa = 1;
    // hexnum = parseInt(targetnum, 16);
    // hexcolor = '#'+ targetnum + targetnum + 'FF'
    //console.log(hexcolor);
    var material = new THREE.MeshBasicMaterial({transparent: true, opacity: opa, color: hexcolor});

    var radius = 50;
    var segments = 12;		// wieviel Teilflaechen der Kreis hat
    var thetaStart = 0;   //wo der Winkel anfaengt
    var thetaLength = winkel;
    var x = distanz;
    var y = DBWert;


    //console.log(radius);
    var circleGeometry = new THREE.CircleGeometry(radius, segments, thetaStart, thetaLength);
    var circle = new THREE.Mesh(circleGeometry, material);
    circle.position.x = x;
    circle.position.y = y;
    circle.position.z = 0;
    circle.className = "data";
    //circle.material.opacity = "0.2";
    scene1.add(circle);
    linecount++;



}


/**
 * returns a coefficient to for scaling depending on the FFT-Size
 * @param {number} FFTSize
 * @returns {Number}
 */
function scaleX(fftsize)
{
    var Scale = 1;
    
    if (2048 < fftsize && fftsize <= 4096)  { Scale =  Skalierungen[2]; }
    if (1024 < fftsize && fftsize <= 2048)  { Scale =  Skalierungen[1]; }
    if (512 < fftsize && fftsize <= 1024)  { Scale = Skalierungen[0]; }
    
    if (256 < fftsize && fftsize <= 512)  { Scale = 1 }
    
    if (128 < fftsize && fftsize <= 256)  { Scale = 1 / Skalierungen[0]; }
    if (64 < fftsize && fftsize <= 128)  { Scale = 1 / Skalierungen[1]; }
    if (32 < fftsize && fftsize <= 64)  { Scale = 1 / Skalierungen[2]; }
    if (16 < fftsize && fftsize <= 32)  { Scale = 1 / Skalierungen[3]; }
    if (8 < fftsize && fftsize <= 16)  { Scale = 1 / Skalierungen[4]; }
    return Scale;
}
/**
 * function for scaling the Y-values, depending on the fftsize
 * @param {type} fftsize
 * @returns {Number}
 */
function scaleY(fftsize)
{
    var Scale = scaleX(fftsize);
    return (2 * Scale);
}

/**
 * function for drawing an arrow, using the three.js arrowhelper class
 * @param {number} dist the distance of the target, going to be the x-value
 * @param {number} Phi the phaseangle of the target in radians, going to be the direction of the arrow
 * @param {number} DBWert the strenght of signal in DB, going to be the y-value
 * @param {string} hexcolor the color of the arrow to draw in hexadezimal, like '#ff000e'
 * @returns {undefined}
 */
function drawArrow(dist, Phi, DBWert, hexcolor, format)
{
    var Scale = 1;    if (dist === 0) {dist = 0.1;}

    Scale = scaleX(window.FFTSize);
    var ScaleY = scaleY(window.FFTSize);
    DBWert = ((DBWert + 140) * ScaleY);
    var length = 20 * Scale;
    var headlength = 15 * Scale;
    var headwidth = 5 * Scale;
    //dist *= Scale;
    
    //console.log ('dist: ' + dist + ' db: ' + DBWert + ' Phi: ' + Phi);
    var origin = new THREE.Vector3(dist, DBWert, 0.001);
    //var dir = calcdirectionvector(origin, length, winkel);
    var dir = new THREE.Vector3(10, 0.001, 0.001);

    var arrowHelper = new THREE.ArrowHelper(dir, origin, length, hexcolor, headlength, headwidth);

    arrowHelper.rotation.z += parseFloat(Phi);
    arrowHelper.className = "targetarrows";
    
    
    drawArrowPart2(dist, length, DBWert, Phi, hexcolor);    
    scene1.add(arrowHelper);
    
    // add lot to the actual target
    //zeichnelinie(new THREE.Vector3(dist, 0 - 150 * (Scale), 0.1), new THREE.Vector3(dist, DBWert, 0.1), hexcolor, 'lot');
    linecount++;

}


/**
 * used to draw a line from the X-axis to the y-value of the targetarrow
 * @param {THREE.Vector3} anfang an THREE.Vector3 object with the coordinates for the beginning of the line
 * @param {THREE.Vector3} ende   an THREE.Vector3 object with the coordinates for the end of the line
 * @param {string} hexcolor the color of the line in hexadezimal
 * @returns {undefined}
 */
function zeichnelinie(anfang, ende, hexcolor, classname)
{
    var material = new THREE.LineBasicMaterial({color: hexcolor});
    var geometry = new THREE.Geometry();
    geometry.vertices.push(anfang);
    geometry.vertices.push(ende);

    var line = new THREE.Line(geometry, material);
    line.className = classname;
    scene1.add(line);
 

}
/**
 *  duplicate the Line of the Arrow and extend the Arrow with it, so it looks like
 *  the arrow rotates arround its own center
 * @param {number} dist the x-value, where the center of the arrow will be
 * @@param {number} length the length of the arrow
 * @param {number} DBWert the y-value, where the center of the arrow will be
 * @param {number} Phi the phaseangle
 * @param {string} hexcolor the color in hex '#000000'
 * @returns {undefined}
 */
function drawArrowPart2(dist, length, DBWert, Phi, hexcolor)
{
    var x = calckartesianX(length / 2, Phi); 
    var y = calckartesianY(length / 2, Phi); 
    var anfang = new THREE.Vector3(dist, DBWert, 0.1);
    var ende = new THREE.Vector3(dist - x ,DBWert -y , 0.1);
    
    var material = new THREE.LineBasicMaterial({color: hexcolor});
    var geometry = new THREE.Geometry();
    geometry.vertices.push(anfang);
    geometry.vertices.push(ende);

    var line = new THREE.Line(geometry, material);
    line.className = "targetarrows";
    scene1.add(line);

}

/**
 * function for drawing the chart of the Range-Frame
 * drawing lines between points of an input-array "Arr"
 * @param {array} Arr an Array of integers with data from the Rangeframe
 * @param {string} hexcolor the color the line should have in hexadezimal
 * @returns {undefined}
 */
function printchartRAW(Arr, hexcolor, datatype)
{
    

  
    var colors = [];
    for (var i = 0; i < Arr.length; i++)
        {
            colors[i] = new THREE.Color();
            colors[i].setHSL(0.2, 1.0, 0.8);
        }
        
        
        if ($('#RangeRadio').is(':checked'))
        {
            var laenge = Arr.length;
            for (var i = 0; i < Arr.length; i++)
            {
                colors[i] = new THREE.Color();
                var hwert = i / laenge;
                colors[i].setHSL(hwert, 0.5, 0.5);
            }
        }

    
        
        if ($('#DBcolorRadio').is(':checked'))
        {
            for (var i = 0; i < Arr.length; i++)
            {
                colors[i] = new THREE.Color();
                var DB = (Arr[i] - 34)
                var hwert = ( (DB-140+20) / -100)
                colors[i].setHSL(hwert+0.2, 1.0, 0.5);
            }
        }
        

        var material = new THREE.LineBasicMaterial({
            transparent: true,
            vertexColors: THREE.VertexColors
        });
        var geometry = new THREE.Geometry();
        geometry.colors = colors;
    
    var num = 0;

   // var Scale = scaleY(Arr.length)
	//console.log(Scale);
    Arr.forEach(function (datastr) {
        if (datastr != undefined)
        {
           num = (((parseInt(datastr, 10)-34) ));           

        }

        geometry.vertices.push(new THREE.Vector3(count, num, 0));
        count++;


    });
    
    var line = new THREE.Line(geometry, material);
    //line.id = "chart" + linecount.toString();
    line.className = datatype;    
    scene1.add(line);
    

    count = 0;
    linecount++;
}

function printchart(Arr, hexcolor, datatype)
{
    

    if (datatype !== "cfar")
    {
        var colors = [];
        for (var i = 0; i < Arr.length; i++)
        {
            colors[i] = new THREE.Color();
            colors[i].setHSL(0.2, 1.0, 0.8);
        }
        
        
        if ($('#RangeRadio').is(':checked'))
        {
            var laenge = Arr.length;
            for (var i = 0; i < Arr.length; i++)
            {
                colors[i] = new THREE.Color();
                var hwert = i / laenge;
                colors[i].setHSL(hwert, 0.5, 0.5);
            }
        }

         if ($('#PhaseRadio').is(':checked'))
        {
            var farbwert, delta = 0;
            
            if (usedPhaseArray == 0)
            {
                for( var i = 0; i < PhaseArray1.length; i++ ) 
                {
                    // get color from the PhaseArray
                    colors[i] = new THREE.Color();
                    colors[i].setHSL(PhaseArray1[i] * 1.5 , 1, 0.5);

                }
            }
            if (usedPhaseArray == 1)
            {
                for( var i = 0; i < PhaseArray0.length; i++ ) 
                {
                    // get color from the PhaseArray
                    colors[i] = new THREE.Color();
                    colors[i].setHSL(PhaseArray0[i] * 1.5, 1, 0.5);

                }
            }
            
        }
    
        
        if ($('#DBcolorRadio').is(':checked'))
        {
            for (var i = 0; i < Arr.length; i++)
            {
                colors[i] = new THREE.Color();
                var DB = (Arr[i] - 34)
                var hwert = ( (DB-140+20) / -100)
                colors[i].setHSL(hwert+0.2, 1.0, 0.5);
            }
        }
        

        var material = new THREE.LineBasicMaterial({
            transparent: true,
            vertexColors: THREE.VertexColors
        });
        var geometry = new THREE.Geometry();
        geometry.colors = colors;
    }
    else
    {
        var material = new THREE.LineBasicMaterial({transparent: true, color: hexcolor});
        var geometry = new THREE.Geometry();
    }
       
    var num = 0;

    var Scale = scaleY(Arr.length)
    Arr.forEach(function (datastr) {
        if (datastr != undefined)
        {
           num = (((parseInt(datastr, 10)-34) * Scale));           

        }

        geometry.vertices.push(new THREE.Vector3(count, num, 0));
        count++;


    });
    
    var line = new THREE.Line(geometry, material);
    //line.id = "chart" + linecount.toString();
    line.className = datatype;    
    scene1.add(line);


    count = 0;
    linecount++;
}

/**
 * function for drawing an interpolated Curve through the datapoints
 * @param {type} Arr the Array containing the Framedata
 * @param {type} hexcolor the color of the line
 * @param {type} datatype what kind of data: rangeframe or cfar
 * @returns {undefined}
 */
function drawSpline(Arr, hexcolor, datatype){

    //console.log(datatype + ': ' + Arr.length)
    var material = new THREE.LineBasicMaterial({transparent: true, color: hexcolor});
    var geometry = new THREE.Geometry();
	   
    var num = 0;
    var Scale = scaleX(Arr.length);
    
    var points = [];
    
    var steps = parseInt(Arr.length / 10);
    Arr.forEach(function (datastr, index) {
        if (datastr != undefined)
        {
           num = (((parseInt(datastr, 10)-34) * Scale * 1.5)); 
           //if (index % steps == 0) { drawZLines(index, num, Arr.length/2) }
           //console.log((num + 174) + ': ' + String.fromCharCode(num));
        }

        points.push(new THREE.Vector3(count, num, 0));
        count++;


    });
       
    // smooth my curve over this many points
    if (window.FFTSize < 512)
    {
        var numPoints = window.FFTSize * 4;
    }
    else
    {
        var numPoints = parseInt(window.FFTSize / 2);
    }
    
    var spline = new THREE.CatmullRomCurve3(points);
    var splinePoints = spline.getPoints(numPoints);
    
     
    for(var i = 0; i < splinePoints.length; i++)
    {
        geometry.vertices.push(splinePoints[i]);         
    }

    var line = new THREE.Line(geometry, material);
    line.className = datatype;
    
    scene1.add(line);           
    
    count = 0;
    linecount++;
}


/**
 * deletes the old data of the phasediagramm
 * @returns {undefined}
 */
function phasendiagrammleeren()
{

    //delete old Data
    d3.selectAll('.phaseangle').remove();
        
        // make old data transparent end then delete next time
//        var opa = $('.phaseangle').css('opacity')
//        if (opa < 0.9) {$('.phaseangle').remove();}
//        else  { opa = opa - 0.5; $('.phaseangle').css('opacity', opa) } 
       
}
/**
 * drawing a line at the SVG-Tag for the phasediagramm
 * @param {int} targetnum the targetnumber
 * @param {number} x2 the X-coordinate
 * @param {number} y2 the Y-coordinate
 * @param {number} distanz the distance of the target ==> the radius
 * @param {int} format the format as an integer, for example 4 to display bin#
 * @returns {undefined}
 */
function drawsvgPhiLine(targetnum, x2, y2, distanz, format)
{
    //console.log(format)
    if (format == 4)
    //also in bin#
    {
        x2 /= 25; y2 /= 25;
        
    }
    if (format == 5)
    //also in mm
    {
        x2 /= 25; y2 /= 25;    
        // die svgflaeche ist 500px groß, zum Zentrum sinds 250px
    }
    if (format == 6)
    // also in cm
    {
        
    }
    
        //console.log(targetnum)
        //console.log ('x2: '+x2); console.log('y2: ' + y2)

        var svg = d3.select('#svgflaeche');

        svg.append('line')
                .attr('x1', center[0])
                .attr('x2', center[0] + x2)
                .attr('y1', center[1])
                .attr('y2', center[1] + y2)
                //.attr('id', 'phaseangle')
                .classed("phaseangle", true)
                .style('stroke', TargetColors[targetnum]);


        svg.append('circle')
                .attr('r', 5)
                .attr('cx', center[0] + x2)
                .attr('cy', center[1] + y2)
                .classed("phaseangle", true)
                .style('fill', TargetColors[targetnum]);

        if (format == 4)
        // in 'bin#'
        {
        svg.append("text")
                .attr("x", center[0] + x2)
                .attr("y", center[1] + y2)
                //.attr("dy", "0.1em")
                .classed("phaseangle", true)
                .text(distanz);
        }

        if (format == 5)
        // in 'mm'
        {
        svg.append("text")
                .attr("x", center[0] + x2)
                .attr("y", center[1] + y2)
                //.attr("dy", "0.1em")
                .classed("phaseangle", true)
                .text(distanz);
        }
        if (format == 6)
        // in 'cm'
        {
        svg.append("text")
                .attr("x", center[0] + x2)
                .attr("y", center[1] + y2)
                //.attr("dy", "0.1em")
                .classed("phaseangle", true)
                .text(distanz);
        }
        
    


}

/**
 * calculates the cartesian X-coordinates of a given angle Phi and a radius
 * @param {number} radius 
 * @param {number} Phi
 * @returns {Number}
 */
function calckartesianX(radius, Phi)
{
    var xcoord = radius * Math.cos(parseFloat(Phi));
    return xcoord;
}
/**
 * calculates the cartesian Y-coordinates of a given angle Phi and a radius
 * @param {number} radius 
 * @param {number} Phi
 * @returns {Number}
 */
function calckartesianY(radius, Phi)
{
    var ycoord = radius * Math.sin(parseFloat(Phi));
    return ycoord;
}


/**
 * clears all phaseangle-Arrays
 * @returns {undefined}
 */
function resetBuffers()
{
     PhaseArray0 = [];
     PhaseArray1 = [];
     usedPhaseArray = 0;
     DeltaPhase = [];
}