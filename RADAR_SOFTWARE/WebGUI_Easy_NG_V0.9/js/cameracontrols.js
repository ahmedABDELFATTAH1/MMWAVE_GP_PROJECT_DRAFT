/**
 * @fileOverview script to control the camera
 * 
 */


/**
 * resets the cameras rotation to 0,0,0
 * @returns {undefined}
 */
function resetcamerarotation() {

    //animateRotateX(camera1.rotation.x, 0);
    camera1.rotation.x = 0; 
    window.camerarotation.CamRotX = 0;
    
    //animateRotateY(camera1.rotation.y, 0);
    camera1.rotation.y = 0; 
    window.camerarotation.CamRotY = 0;
    
    //animateRotateZ(camera1.rotation.z, 0);
    camera1.rotation.z = 0; 
    window.camerarotation.CamRotZ = 0;
    
    
}

/**
 * resets the cameras position to 0, -140, 0
 * @returns {undefined}
 */
function resetcameraposition() {
        
    camera1.position.x = 0; window.cameraposition.CamPosX = 0;
    camera1.position.y = -140; window.cameraposition.CamPosY = -140;
    camera1.position.z = 0; window.cameraposition.CamPosZ = 0;
}


/**
 * function for moving the camera with the mouse
 * , not used actually, because of Orbitcontrols.js
 * @returns {undefined}
 */
function MoveCam()
{
    //contextmenu bei rechtsklick ausschalten
    var el = document.getElementById('canvascontainer');
    el.addEventListener('contextmenu', function(ev) {
    ev.preventDefault();
    
    return false;
    }, false);
    $("#canvascontainer").on('mousedown', function (event) {
            event.preventDefault();
        $("#canvascontainer").mousemove(function (ev) {
            ev.preventDefault();
            //errechne differenz
            var deltaX = event.pageX - ev.pageX;
            var deltaY = event.pageY - ev.pageY;
            
            
            var button = ''
            if (browser == 'firefox') 
            {
                if(ev.buttons == 1){   button = 'links'}
                if(ev.buttons == 2){   button = 'rechts' }
            }
            if (browser === 'chrome')
            {
                if(ev.which == 1){   button = 'links'}
                if(ev.which == 3){   button = 'rechts' }
            }
            
            if (button == 'links')
                {
                    //camera1.position.x += deltaX / 100;
                    camera1.position.x += deltaX * window.FFTSize/5000;
                    camera1.position.y += -(deltaY * window.FFTSize/5000);
                    window.cameraposition.CamPosX = camera1.position.x;
                    window.cameraposition.CamPosY = camera1.position.y;


                    return false;

                }
            
            if (button == 'rechts')
                {
                    var Scale = scale (window.FFTSize)
                    camera1.lookAt(new THREE.Vector3(window.FFTSize / 2, -140 * Scale, -window.FFTSize / 2))
                    //console.log(deltaX / 25)
                    var anderungx = ((Math.cos( deltaX / 50 ))) * (window.FFTSize)/100
                    //console.log(anderungx)
                    camera1.position.x += anderungx
                    var aenderungz = -((Math.cos( deltaX / 50 ))) * (window.FFTSize)/100
                    camera1.position.z += aenderungz
//                    

//                    camera1.rotation.y += deltaX * window.FFTSize/500000;                 
//                    camera1.rotation.x += deltaY * window.FFTSize/500000;
//                    window.camerarotation.CamRotX = camera1.rotation.x;
//                    window.camerarotation.CamRotY = camera1.rotation.y;
                }            
            
            
            
            
            
        });

    });
    $("#canvascontainer").on('mouseup', function () {
        $("#canvascontainer").off('mousemove');
    });
}




/**
 * function for mousewheel zooming, changing the camera's z-position,
 * not used actually, because of Orbitcontrols.js
 * @returns {undefined}
 */
function mousewheelzoom()
{
    var cont = document.getElementById('canvascontainer');
    cont.onwheel = function(ev) 
    {
        //console.log(ev.deltaY)
        camera1.position.z += (ev.deltaY * (window.FFTSize/100)) 
        window.cameraposition.CamPosZ = camera1.position.z;
    }
    ;
    
}


/**
 * adds the eventlistener for touch-events to the scene
 * one finger -> Pan
 * two finger -> Zoom
 * not used actually, because of Orbitcontrols.js
 * @returns {undefined}
 */
function touchstart()
{
    var cont = document.getElementById('canvascontainer');
    cont.addEventListener( 'touchstart', function (ev)
    {
                       
        cont.addEventListener( 'touchmove', function(event){
        event.preventDefault();
    
            if (event.touches.length == 1)
            {
                //ein Finger Panning
                var dx = (ev.touches[ 0 ].pageX) - (event.touches[ 0 ].pageX);
                var dy = (ev.touches[ 0 ].pageY) - (event.touches[ 0 ].pageY)
                
                camera1.position.x += dx / 1000;
                camera1.position.y += -dy / 1000;
            }
            if (event.touches.length == 2)
            {
                //zwei Finger gleich Zooming
                var dx = event.touches[ 0 ].pageX - event.touches[ 1 ].pageX;
                var dy = event.touches[ 0 ].pageY - event.touches[ 1 ].pageY;
                camera1.position.z = Math.sqrt( dx * dx + dy * dy );
            }
            if (event.touches.length == 3)
            {
                //drei Finger Rotation
            }
            }, false );
        
        
    }, false );
    cont.addEventListener('touchend', function(endEvent)
    {
            cont.dispatchEvent( endEvent );
    });
}


/**
 * moves the camera to the specified X-value, used for the sliders of dat.GUI
 * @param {number} value
 * @returns {undefined}
 */
function MoveX(value)
{
    camera1.position.x = value;
}
/**
 * moves the camera to the specified Y-value, used for the sliders of dat.GUI
 * @param {number} value
 * @returns {undefined}
 */
function MoveY(value)
{
    camera1.position.y = value;
}
/**
 * moves the camera to the specified Z-value, used for the sliders of dat.GUI
 * @param {number} value
 * @returns {undefined}
 */
function ZoomCam(value)
{
    
    camera1.position.z = value;
}
/**
 * rotate the camera at the X-axis, used for the sliders of dat.GUI
 * @param {number} value
 * @returns {undefined}
 */
function rotateX(value)
{
    camera1.rotation.x = value;
}
/**
 * rotate the camera at the Y-axis, used for the sliders of dat.GUI
 * @param {number} value
 * @returns {undefined}
 */
function rotateY(value)
{
    camera1.rotation.y = value;
}
/**
 * rotate the camera at the Z-axis, used for the sliders of dat.GUI
 * @param {number} value
 * @returns {undefined}
 */
function rotateZ(value)
{
    camera1.rotation.z = value;
}
/**
 * changes the cameras X-position with an animation, not used
 * @param {number} anf the beginning-value of the animation
 * @param {number} end the end-value of the animation
 * @returns {undefined}
 */
function animateCamX(anf, end)
{
    
    anf = parseInt(anf); end = parseInt(end);
    var deltaEnd = anf - end;
    var interval = setInterval(function()
    {
        if (anf < end)
        {
            camera1.position.x += 3; 
        }
        if (anf > end)
        {
            camera1.position.x -= 3; 
        }
        deltaEnd = parseInt(end - camera1.position.x);
        
        if (deltaEnd < (4) && (deltaEnd > -4)) { clearInterval(interval);}
    }, 0)
    
    
}
/**
 * changes the cameras Y-position with an animation, not used
 * @param {number} anf the beginning-value of the animation
 * @param {number} end the end-value of the animation
 * @returns {undefined}
 */
function animateCamY(anf, end)
{
    
    anf = parseInt(anf); end = parseInt(end);
    var deltaEnd = anf - end;
    
    {
        var interv = setInterval(function()
        {
            if (anf < end)
            {
                camera1.position.y += 3; 
            }
            if (anf > end)
            {
                camera1.position.y -= 3; 
            }
            deltaEnd = end - camera1.position.y;
        if (deltaEnd < 4 && deltaEnd > -4) { clearInterval(interv);}
            //if (Math.round(camera1.position.y) == end) { clearInterval(interv);}
        }, 0)
    }
}
/**
 * changes the cameras Z-position with an animation, not used
 * @param {number} anf the beginning-value of the animation
 * @param {number} end the end-value of the animation
 * @returns {undefined}
 */
function animateCamZ(anf, end)
{
    
    anf = parseInt(anf); end = parseInt(end);
    var deltaEnd = anf - end;
    
    {
        var interv = setInterval(function()
        {
            if (anf < end)
            {
                camera1.position.z += 3; 
            }
            if (anf > end)
            {
                camera1.position.z -= 3; 
            }
            deltaEnd = end - camera1.position.z;
            if (deltaEnd < 4 && deltaEnd > -4) { clearInterval(interv);}
            //if (Math.round(camera1.position.z) == end) { clearInterval(interv);}
        }, 0)
    }
}

/**
 * changes the cameras X-rotation with an animation, not used and not finished yet
 * @param {number} anf the beginning-value of the animation
 * @param {number} end the end-value of the animation
 * @returns {undefined}
 */
function animateRotateX(anf, end)
{
    
    
    {
        var interv = setInterval(function()
        {
            if (anf < end)
            {
                camera1.rotation.x += 0.0001; 
            }
            if (anf > end)
            {
                camera1.rotation.x -= 0.0001; 
            }

            if ((camera1.rotation.x) === end) { clearInterval(interv);}
        }, 1000)
    }
}
/**
 * changes the cameras Y-rotation with an animation, not used, 
 * not finished yet
 * @param {number} anf the beginning-value of the animation
 * @param {number} end the end-value of the animation
 * @returns {undefined}
 */
function animateRotateY(anf, end)
{
    anf = parseInt(anf); end = parseInt(end);
    
    {
        var interv = setInterval(function()
        {
            if (anf < end)
            {
                camera1.rotation.y += 0.0001; 
            }
            if (anf > end)
            {
                camera1.rotation.y -= 0.0001; 
            }

            if ((camera1.rotation.y) === end) { clearInterval(interv);}
        }, 1)
    }
}
/**
 * changes the cameras Z-rotation with an animation, not used, 
 * not finished yet
 * @param {number} anf the beginning-value of the animation
 * @param {number} end the end-value of the animation
 * @returns {undefined}
 */
function animateRotateZ(anf, end)
{
    anf = parseInt(anf); end = parseInt(end);
    
    {
        var interv = setInterval(function()
        {
            if (anf < end)
            {
                camera1.rotation.z += 0.0001; 
            }
            if (anf > end)
            {
                camera1.rotation.z -= 0.0001; 
            }

            if ((camera1.rotation.z) === end) { clearInterval(interv);}
        }, 1)
    }
}