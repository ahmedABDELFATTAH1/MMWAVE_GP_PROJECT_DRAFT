
/**
 * @fileOverview file for all GUI-controls functionality
 */




function updateLastConfig(oldconfigstr, Frame)
{
    
    if (oldconfigstr.includes(Frame) ){
        //get old sysconfig
        var anf = (oldconfigstr.indexOf(Frame));
        var oldsysconfig = oldconfigstr.substring(anf, 11);
        var newconfigstr = oldconfigstr.replace(oldsysconfig, "");        
        return newconfigstr;
        
    }
    else
    {
        return oldconfigstr;
    }
        
}
function setStandardConfigs()
{
    var standardconfig = '{"desc":"high accuracy, short distance","trg":0,"slf":1,"slp":0,"dc":1,"FIR":0,"WINDOW":1,"raw":0,"cmp":0,"r":1,"c":1,"p":0,"tl":1,"st":1,"err":1,"ser1":0,"ser2":1,"AGC":1,"protocol":0,"LEDval":1,"frontend":3,"fmt":0,"log":0,"delay":"0","gain":"0","basefrequ":120000,"VCOdivider":64,"bandwith":5000,"adcClockDivideramount":"5","numofSample":"4","numofRamps":"4","downsamplamount":"0","FFTsize":"4","AverageN":"1","CFType":"0","CFGuard":"1","CFSize":"3","CFTreshold":"8"}';
	
    var landingmode = '{"desc":"high accuracy, short distance","trg":0,"slf":1,"slp":0,"dc":1,"FIR":0,"WINDOW":1,"raw":0,"cmp":0,"r":1,"c":1,"p":0,"tl":1,"st":1,"err":1,"ser1":0,"ser2":1,"AGC":1,"protocol":0,"LEDval":1,"frontend":3,"fmt":0,"log":0,"delay":"0","gain":"0","basefrequ":120000,"VCOdivider":64,"bandwith":5000,"adcClockDivideramount":"5","numofSample":"4","numofRamps":"0","downsamplamount":"0","FFTsize":"4","AverageN":"1","CFType":"0","CFGuard":"2","CFSize":"4","CFTreshold":"10"}';
	
    var maxupdateconfig = '{"desc":"high accuracy, short distance, high update rate, no spectrum output","FIR":0,"WINDOW":1,"raw":0,"cmp":0,"trg":0,"slf":1,"slp":0,"dc":1,"r":0,"c":0,"p":0,"tl":1,"st":0,"err":1,"ser1":0,"ser2":1,"AGC":0,"protocol":0,"LEDval":1,"frontend":3,"fmt":0,"log":0,"delay":"0","gain":"2","basefrequ":120000,"VCOdivider":64,"bandwith":5000,"adcClockDivideramount":"5","numofSample":"4","numofRamps":"1","downsamplamount":"0","FFTsize":"4","AverageN":"1","CFType":"0","CFGuard":"1","CFSize":"3","CFTreshold":"8"}';
	
    var maxdistanceconfig = '{"desc":"low accuracy, long distance","trg":0,"slf":1,"slp":0,"dc":1,"FIR":0,"WINDOW":1,"raw":0,"r":1,"cmp":0,"c":1,"p":0,"tl":1,"st":1,"err":1,"ser1":0,"ser2":1,"AGC":1,"protocol":0,"LEDval":1,"frontend":3,"fmt":0,"log":0,"delay":"0","gain":"0","basefrequ":120000,"VCOdivider":64,"bandwith":2000,"adcClockDivideramount":"5","numofSample":"5","numofRamps":"4","downsamplamount":"0","FFTsize":"5","AverageN":"1","CFType":"0" ,"CFGuard":"1","CFSize":"1","CFTreshold":"7"}';
	
    var maxaccuracy = '{"desc":"very high accuracy, short distance","trg":0,"slf":1,"slp":0,"dc":1,"r":1,"FIR":1,"WINDOW":1,"raw":0,"cmp":0,"c":1,"p":0,"tl":1,"st":1,"err":1,"ser1":0,"ser2":1,"AGC":1,"protocol":0,"LEDval":1,"frontend":3,"fmt":0,"log":0,"delay":"0","gain":"0","basefrequ":120000,"VCOdivider":64,"bandwith":6000,"adcClockDivideramount":"4","numofSample":"6","numofRamps":"1","downsamplamount":"3","FFTsize":"6","AverageN":"1","CFType":"0","CFGuard":"1","CFSize":"4","CFTreshold":"8"}';
    
    if (browser == "firefox")
    {
        document.cookie = "preset&standard=" + standardconfig;
        document.cookie = "preset&landing mode=" + landingmode;
        document.cookie = "preset&high update rate=" + maxupdateconfig;
        document.cookie = "preset&high distance="+ maxdistanceconfig;
        document.cookie = "preset&high accuracy="+ maxaccuracy;
    }    

    if (browser == "chrome")
        {
            localStorage.setItem("preset&standard", standardconfig);
            localStorage.setItem("preset&landing mode", landingmode);
            localStorage.setItem("preset&high update rate", maxupdateconfig);
            localStorage.setItem("preset&high distance", maxdistanceconfig);
            localStorage.setItem("preset&high accuracy", maxaccuracy);
        }
}

function updatepresets()
{
    $('#presetselect').empty();
    getconfigs();
}
function deleteConfig()
{
        var presetname = $('#presetselect').val();
        eraseCookie(presetname);
        localStorage.removeItem("preset&" + presetname);
        updatepresets();    
}


function eraseCookie(name) {
    document.cookie = name + '=; Max-Age=0';
}
function getconfigs()
{
       
       if (browser == "firefox")
       {
           var cook = document.cookie;
        
        if (cook !== "" )
        {
            var text = cook.split(";")
            text.forEach(function(item, index){
            
            {
                var preset = item.split("=")
                //alert(preset)
                var name = (preset[0]);
                var presetobj = JSON.parse(preset[1]);
                var beschreibung = (presetobj.desc);              
                
                
                var option = document.createElement ('option');
                //option.id = name;
                option.value = name;
                option.innerHTML = name.replace('preset&', "");
                $('#presetselect').append(option);
            }
                      
        });
        }
        else { $('#oldpresets').hide();}
       }
        
            
        if (browser == "chrome")
        {
            var counter = 0;
            for (var i in localStorage)
            {
                var name = i;
                if (name.startsWith("preset&"))
                {
                    var option = document.createElement ('option');
                    
                    option.value = name.replace("preset&", "");
                    option.innerHTML = name.replace('preset&', "");
                    $('#presetselect').append(option);
                    counter++;
                    $('#oldpresets').show();
                }
                if (counter < 1)
                {
                    $('#oldpresets').hide();
                }
                
            }
        }
    
        
}
function opennewpresetdialog()
{
    
    if (!navigator.cookieEnabled)
    {
        alert('you have to enable cookies in your browser to use this function');
    }
    else
    {              
        $('#newpreset').slideDown();
        $('#oldpresets').slideUp();
        $('#newpresetbutt').hide();
    }
    
}
function saveConfig()
{
    var presetname = $('#presetname').val();
    var description = $('#presetdescr').val();

    var presetobj = {};
    presetobj.desc = description;

    // get values for sysconfig
    presetobj.trg = booltoInt(($('#trg').prop('checked')));
    presetobj.slf = booltoInt(($('#slf').prop('checked')));
    //presetobj.slp = booltoInt(($('#slp').prop('checked')));
    //presetobj.dc = booltoInt(($('#dc').prop('checked')));

    presetobj.raw = booltoInt(($('#raw').prop('checked')));
	presetobj.cmp = booltoInt(($('#cmp').prop('checked')));
    presetobj.r = booltoInt(($('#r').prop('checked')));
    presetobj.c = booltoInt(($('#c').prop('checked')));
    presetobj.p = booltoInt(($('#p').prop('checked')));

    presetobj.tl = booltoInt(($('#tl').prop('checked')));
    presetobj.st = booltoInt(($('#st').prop('checked')));
    presetobj.err = booltoInt(($('#err').prop('checked')));

    presetobj.ser1 = booltoInt(($('#ser1').prop('checked')));
    presetobj.ser2 = booltoInt(($('#ser2').prop('checked')));
    
    
    presetobj.AGC = booltoInt(($('#AGCMode').prop('checked')));
	  
    presetobj.protocol = parseInt($('#ProtocolID').val(), 10);
    presetobj.log = parseInt($('#ScaleID').val(), 10);
    presetobj.fmt = parseInt($('#UnitAmount').val(), 10);	
    presetobj.frontend = parseInt($('#frontendselect').val(), 10);
    //frontend = dec2bin(frontend);    console.log(frontend)    
    presetobj.delay = $('#TriggerDelayAmount').val();
    presetobj.gain = $('#GainAmount').val();
    
    //get RFEconfig-values
    presetobj.basefrequ = parseInt($('#basefreqin').val());
    presetobj.VCOdivider = parseInt($('#vcodividerIn').val());
    
    //get PLLfrequ-values
    presetobj.bandwith = parseInt($('#bandwithIn').val());
    
    
    //get BBSetup-values
    presetobj.adcClockDivideramount = $('#adcClockDivideramount').val();
    presetobj.numofSample = $('#NumofSampleamount').val();
    presetobj.numofRamps = $('#NumofRampsamount').val();
    presetobj.downsamplamount = $('#Downsamplingamount').val();
    presetobj.FFTsize = $('#FFTsizeamount').val();
    presetobj.AverageN = $('#AverageNamount').val();	
    presetobj.CFGuard = $('#CFGuardamount').val();
    presetobj.CFSize = $('#CFSizeamount').val();
    presetobj.CFTreshold = $('#CFTresholdamount').val();
    presetobj.CFType = $('#CFARamount').val();
	presetobj.DC = $('#DCCancelamount').val(); 
    presetobj.WINDOW= $('#Windowamount').val();
    presetobj.FIR = $('#FIRamount').val();
    
    var JSONstr = JSON.stringify(presetobj);
    
    if (browser == "firefox")
    {
          $( function() {    $(document ).tooltip();  } );
        document.cookie = 'preset&' + presetname + "=" + JSONstr + ";";
        
    } 
    if (browser == "chrome")
    {
        localStorage.setItem("preset&" + presetname, JSONstr)
    }
    
    updatepresets();
    $('#newpreset').slideUp(); $('#oldpresets').slideDown(); $('#newpresetbutt').show();
    
    //save the config
}

function loaddescription()
{
    var presetname = $('#presetselect').val();
    
    if (browser == "firefox")
    {
        var cookie = document.cookie;
    
    var Jsontext = cookie.split(";");    
    Jsontext.forEach(function(item){
        if (item.startsWith(presetname))
            {
                var preset = item.split("=")[1];
                //console.log(preset);
                var presetobj = JSON.parse(preset);
                $('#description').html(presetobj.desc);
            }
        });
    }
    
    if (browser == "chrome")
    {
        var preset = localStorage.getItem("preset&" + presetname);
        var presetobj = JSON.parse(preset)
        $('#description').html(presetobj.desc);        
        
    }
    
}
function loadconfig()
{
    
    var presetname, cookie = "";
    var Jsontext = [];
    var presetobj = {}
    if (browser == "firefox")
    {
        var presetname = $('#presetselect').val();     
        var cookie = document.cookie;
        Jsontext = cookie.split(";");
        
        Jsontext.forEach(function(item){
        if (item.startsWith(presetname))
            {
                var preset = item.split("=")[1];
                //console.log(preset);
                presetobj = JSON.parse(preset);
            }
        });
    }
    
    if (browser == "chrome")
    {
        var presetname = $('#presetselect').val();
        var preset = localStorage.getItem("preset&" + presetname);        
        presetobj = JSON.parse(preset);
    }
    //get SystemConfig-values	
    (($('#ISMMode').prop('checked', presetobj.ISM )));
	   
    $('#trg').prop('checked', presetobj.trg);
    $('#slf').prop('checked', presetobj.slf);
    (($('#slp').prop('checked', presetobj.slp)));
    $('#TriggerDelayAmount').val(presetobj.delay);
    $('#TriggerDelaySlider').slider('value', presetobj.delay);
	
	(($('#ser1').prop('checked', presetobj.ser1)));
    (($('#ser2').prop('checked', presetobj.ser2)));
	
	(($('#AGCMode').prop('checked', presetobj.AGC )));
    $('#GainAmount').val(presetobj.gain);
    $('#GainSlider').slider('value', presetobj.gain);
	$('#CouplingSlider').slider('value', presetobj.gain);
	$('#Coupling').val(presetobj.coupling);
	$('#UnitAmount').val(presetobj.fmt);
	$('#UnitSlider').slider('value', presetobj.fmt);
	

    (($('#raw').prop('checked', presetobj.raw )));
    (($('#cmp').prop('checked', presetobj.cmp )));
    (($('#r').prop('checked', presetobj.r)));
    (($('#c').prop('checked', presetobj.c )));
    (($('#p').prop('checked', presetobj.p)));
    (($('#tl').prop('checked', presetobj.tl)));
    (($('#st').prop('checked', presetobj.st)));
    (($('#err').prop('checked', presetobj.err)));
	
	$('#ProtocolID').val(presetobj.protocol);
    $('#ProtocolSlider').slider('value', presetobj.protocol);

	$('#ScaleID').val( presetobj.log);
	$('#ScaleSlider').slider('value', presetobj.log);
    
    $('#frontendselect').val(presetobj.frontend);
    //frontend = dec2bin(frontend);    console.log(frontend)   
    
    //get RFEconfig-values
	//console.log(presetobj.basefrequ);
    ($('#basefreqin').val(presetobj.basefrequ));
    ($('#vcodividerIn').val(presetobj.VCOdivider));
    
    //get PLLfrequ-values
    $('#bandwithIn').val(presetobj.bandwith);
        
    //get BBSetup-values
    $('#adcClockDivideramount').val(presetobj.adcClockDivideramount);    
    $('#adcClockDividerSlider').slider('value', presetobj.adcClockDivideramount);
    
    $('#NumofSampleamount').val(presetobj.numofSample ); 
    $('#NumofSamplSlider').slider('value', presetobj.numofSample);
    $('#NumofSamplLabel').html(32 << presetobj.numofSample );
    
    $('#NumofRampsamount').val(presetobj.numofRamps); 
    $('#NumofRampsSlider').slider('value', presetobj.numofRamps);
    $('#numofRampsLabel').html(1 << presetobj.numofRamps);
	
	$('#DCCancelamount').val(presetobj.dc);    
    $('#DCCancelSlider').slider('value', presetobj.dc);
	
	$('#FIRamount').val(presetobj.FIR);    
    $('#FIRSlider').slider('value', presetobj.FIR);
    
    var valuearr = [0, 1, 2, 4, 8, 16, 32, 64];
    $('#Downsamplingamount').val(presetobj.downsamplamount); 
    $('#DownsamplingSlider').slider('value', presetobj.downsamplamount);
    $('#downsamplLabel').html(valuearr[presetobj.downsamplamount]);
    
	$('#Windowamount').val(presetobj.WINDOW);    
    $('#WindowSlider').slider('value', presetobj.WINDOW);
	
    $('#FFTsizeamount').val(presetobj.FFTsize); 
    $('#FFTsizeSlider').slider('value', presetobj.FFTsize);
    $('#FFTsizeLabel').html(32 << presetobj.FFTsize);
    
    $('#AverageNamount').val(presetobj.AverageN);
    $('#AverageNSlider').slider('value', presetobj.AverageN);
    $('#AverageNLabel').html(presetobj.AverageN);
	
    //Target Recognition Config
	$('#CFARLabel').val(presetobj.CFType); 
    $('#CFARSlider').slider('value', presetobj.CFType);
   	
    $('#CFGuardamount').val(presetobj.CFGuard); 
    $('#CFGuardSlider').slider('value', presetobj.CFGuard);
    $('#CFGuardLabel').html(presetobj.CFGuard);
    
    $('#CFSizeamount').val(presetobj.CFSize);
    $('#CFSizeSlider').slider('value', presetobj.CFSize);
    $('#CFSizeLabel').html(presetobj.CFSize);
    
    $('#CFTresholdamount').val(presetobj.CFTreshold); 
    $('#CFTresholdSlider').slider('value', presetobj.CFTreshold);
    $('#CFTresholdLabel').html(2*presetobj.CFTreshold);   
   
    setTimeout(function(){$('#resendConfig').trigger('click');}, 500)
    
        
    
    
   
}

/**
 * adding dat.GUI to the page (slider to control the camera and see the cameras position)
 * @returns {undefined}
 */
function addDatGUI()
{
    var gui = new DAT.GUI(
            {
                height: 200,
                width: 200,
                autoPlace: false,
            });
    gui.domElement.id = 'datgui';
    $("#accordion").append(gui.domElement);

    //cameraposition
    gui.add(window.cameraposition, 'CamPosX').min(0).max(2048).step(1).listen().onChange(function (x) {
        MoveX(x);
    });
    gui.add(window.cameraposition, 'CamPosY').min(0).max(80).step(1).listen().onChange(function (y) {
        MoveY(y);
    });
    gui.add(window.cameraposition, 'CamPosZ').min(0).max(1500).step(1).listen().onChange(function (z) {
        ZoomCam(z);
    });
    //camerarotation
    gui.add(window.camerarotation, 'CamRotX').min(-6.3).max(6.3).step(0.0001).listen().onChange(function (x) {
        rotateX(x);
    });
    gui.add(window.camerarotation, 'CamRotY').min(-6.3).max(6.3).step(0.0001).listen().onChange(function (y) {
        rotateY(y);
    });

    //positioning dat.gui
    //  $('#datgui').css('position', 'absolute');
    $('#datgui').css('width', '100%');
    $('#datgui').css('top', '6px');
    $('#datgui').css('margin', '6px');
    $('#datgui').css('float', 'right');
    $('#datgui').css('border-radius', '3px');
    $('#datgui').css('z-index', '2');

    //positioning targetlist
    $("#targetlistContainer").css('left', '80%');
    $('#targetlistContainer').css('height', 'auto');
    $("#targetlistContainer").draggable();

    //removetogglebutton
    $('a.guidat-toggle').remove();

    //add own togglebutton
    var btn = document.createElement("Button");
    var t = document.createTextNode("show camera controls");
    btn.appendChild(t);
    btn.style.background = '#999999';
    btn.style.color = 'white';
    btn.style.height = '15px';
    btn.style.border = '0px';
    btn.id = 'toggleCamControls';
    btn.onclick = function () {
        toggleCamControls(btn.innerHTML);
    };
    $('#datgui').append(btn);
    $('div.guidat-controllers').hide();

}


/**
 * change the text of the togglebutton to hide or show the button
 * @param {string} txt
 * @returns {undefined}
 */
function toggleCamControls(txt)
{

    $('div.guidat-controllers').toggle('slow', function (finished)
    {
        if (txt == 'hide camera controls') {
            $('#toggleCamControls').html('show camera controls');
        }
        if (txt == 'show camera controls') {
            $('#toggleCamControls').html('hide camera controls');
        }
    });
}

/**
 * adding the stats for fps etc. to the document
 * @returns {undefined}
 */
function addStats()
{
    stats = new Stats();
    stats.setMode(0); // 0: fps, 1: ms, 2: mb

    // align top-left

    stats.domElement.style.right = '12px';
    stats.domElement.style.top = '6px';
    stats.domElement.id = 'stats';
    stats.domElement.style.position = 'absolute';
    $('#stats').css('z-index', '1');

    $('#canvascontainer').append(stats.domElement);
    update();


}

/**
 * function for updating the stats like FPS ..
 * @returns {undefined}
 */
var update = function () {

    stats.begin();

    // monitored code goes here

    stats.end();

    requestAnimationFrame(update);

};

/**
 * show the semitransparent dropdown in the horizontal menu for the FFT-View at the top of the screen
 * @returns {undefined}
 */
function showFFTDropdown() {
    $('#FFTDropdown').show().css('display', 'block');
}

function showRawDropdown() {
    $('#RawDropdown').show().css('display', 'block');
}
/**
 * hide the semitransparent dropdown in the horizontal menu at the top of the screen
 * @returns {undefined}
 */
function hidedropdown()
{
    $('.untermenu').hide();
}
/**
 * show the semitransparent dropdown in the horizontal menu for the FFT-View at the top of the screen
 * @returns {undefined}
 */
function showOptionsDropdown() {
    $('#OptionsDropdown').show().css('display', 'block');
}


/**
 * let the accordioncontainer on the left of document appear or disappear with an animation
 * @returns {undefined}
 */
function togglemenu()
{

    $(".accordcontainer").toggle('slow', function callback()
    {
        if ($('#accordion').css('display') == 'none')
        {
            $('#canvascontainer').css('width', '99%');
            changeRand('>');
            resetview();

        } else
        {
            $('#canvascontainer').css('width', '79%');
            changeRand('<');
            resetview();
        }
    });



}
/**
 * changes the signs of the accordionborder from '<' to '>' and back
 * @param {string} zeichn which char to show
 * @returns {undefined}
 */
function changeRand(zeichn)
{
    $('.randleft').empty();
    for (i = 0; i < 8; i++)
    {
        var p = document.createElement('p');
        p.textContent = zeichn
        $('.randleft').append(p);
    }
}

/**
 * changes the grid, axes, labels and the Camera depending on the FFT-Size
 * @param {number} maxR the FFT-Size
 * @returns {undefined}
 */
function gridanpassen(maxR)
{
    //disconnect();
    //console.log('passe grid an..fftsize: ' + maxR)
    //console.log('clientfftsize: ' + window.FFTSize)
    window.FFTSize = maxR;
    window.sceneready = false;


    if (scene1.children.length > 0)
    {
        for (i = scene1.children.length - 1; i >= 0; i--)
        {

            scene1.remove(scene1.children[i]);                        
                     
            
            
            if (i == 0)
            {
                // change the target of the Orbitcontrols
                maxR = parseInt(maxR);
                targetsetzen(maxR);
                cameraanpassen(window.FFTSize);
                window.setTimeout(function ()
                {
                    //scene1.children = [];

                    if (achsengeloescht() == true)
                    {
                        
                        zeichneachsen(maxR, maxR / window.LineCount.LineCountX, maxR / 100, maxR / 100000);
                        resetBuffers();
                        window.sceneready = true;
                    }
                    else
                    {
                        gridanpassen(window.FFTSize)

                    }

                }, 100);
            }

        }

    } else
    {

        maxR = parseInt(maxR);

        // change the target of the Orbitcontrols
        targetsetzen(maxR);

        window.setTimeout(function ()
        {
           if (achsengeloescht() === true)
                    {
                        zeichneachsen(maxR, maxR / window.LineCount.LineCountX, maxR / 100, maxR / 100000);
                        resetBuffers();
                        window.sceneready = true;
                    }
                    else
                    {
                        gridanpassen(window.FFTSize)
                    }
            //connect();
        }, 100);
    }

}
/**
 * detect if all the axes are deleted
 * @returns {Boolean}
 */
function achsengeloescht()
{

    var anzahl = 0;
    scene1.children.forEach(function(item, index)   {
        if (item.className == 'Achse')
        {
            anzahl += 1;
        }

    });
    if (anzahl > 0) return false;
    else return true;

}


/**
 * used to set the target of the Camera when the Orbitcontrols.js Script is used
 * @param {number} maxR the FFT-Size
 * @returns {undefined}
 */
function targetsetzen(maxR)
{
        var Scale = scaleX(maxR);
        controls.target.set(maxR / 2, 140 * Scale, -maxR / 2);
        //console.log(camera1.position)

}

/**
 * change the view of the camera, depending on the FFT-Size
 * @param {number} maxR the FFT-Size
 * @returns {Number}
 */
function cameraanpassen(maxR)
{
    // vertikaler Blickwinkel
    var alpha = 70;
    var haelfte = maxR / 2;
    //var aspect = x / y;
    var hFoV = haelfte;
    var dist = (hFoV / Math.tan(alpha));
    var height = (dist * Math.tan(alpha)) / 2;

    if (spectrogramm == false)
    {
        //animateCamX(camera1.position.x, haelfte);
        camera1.position.x = haelfte;
        //animateCamY(camera1.position.y, (- height / 4));
        camera1.position.y = height * 0.9;
        //camera1.position.y = (- height / 4);
        //animateCamZ(camera1.position.z, dist * 0.9);
        camera1.position.z = dist * 0.9;
        if (($('#2Dradio').is(":checked")) == false)
        {
    //        camera1.position.set(haelfte, 0, dist)
    //        camera1.rotation.x = -(dist / 1000);
    //        camera1.position.set(0, height, dist/4)
    //        camera1.lookAt(new THREE.Vector3(dist, 0, -dist));
            camera1.rotation.x = 0;
        }
        if (($('#2Dradio').is(":checked")) == true)
        {
            camera1.rotation.x = 0;
        }

    }
    if (spectrogramm == true)
    {
        camera1.position.set(haelfte * 1.5, dist * 1.3, -height * 1.5)
        camera1.rotation.set(-(Math.PI/2),0,0)


    }

    //globales statisches Cameraobjekt fuer Aktualiserung der Slider updaten
    window.cameraposition.CamPosX = camera1.position.x;
    window.cameraposition.CamPosY = camera1.position.y;
    window.cameraposition.CamPosZ = camera1.position.z;
    window.camerarotation.CamRotX = camera1.rotation.x;
    window.camerarotation.CamRotY = camera1.rotation.y;

    return haelfte;

}


/**
 * resets the view to depending of the size of the actual size of the canvascontainer
 * @returns {undefined}
 */
function resetview()
{
    scene1.rotation.set(0,0,0); camera1.rotation.set(0,0,0);
    $('.randleft').css('height', window.innerHeight);

    //get size of the drawpanel
    var x = parseInt($('#canvascontainer').css('width'));
    $('#canvascontainer').css('height', window.innerHeight * 0.9);
    var y = parseInt($('#canvascontainer').css('height'));
    // set size of the renderer to size of the drawpanel
    renderer1.setSize(x, y);
    cameraanpassen(window.FFTSize);
    // draw new axes
    gridanpassen(window.FFTSize);
    window.TTCounter = 0;

}

/**
 * sets all booleans variables to false before the actual view is going to be 'activated'
 * @returns {undefined}
 */
function setViewsfalse()
{

    FFT = false;
    spectrogramm = false;
    phasediagramm = false;
    window.TargetTimeLine = false;
    $('.active').attr('class', 'inactive');
    $('.drawpanel').hide();
}


function showRAWData()
{

    setViewsfalse();
    $('#canvascontainer').show();
    FFT = false;
	//RAW = true;
    resetview();
	window.RawData = true;
    var sel = document.getElementById('RAWDatashow');
    sel.className = "active";
   //console.log('RAW');
}

/**
 * show the FFT: 2D-View, setting the other views to false and call resetview()
 * @returns {undefined}
 */
function showFFT()
{

    setViewsfalse();
    $('#canvascontainer').show();
    FFT = true;
    resetview();
    var sel = document.getElementById('fftshow');
    sel.className = "active";

}
/**
 * activating the 3D-view, with old data going to the background
 * every time new data comes in and call resetview()
 * @returns {undefined}
 */
function showWave()
{

    setViewsfalse();
    $('#canvascontainer').show();
    Wave = true; FFT = true;
    var sel = document.getElementById('fftshow');
    sel.className = "active";
    resetview();

}
/**
 * show the spectrogramm
 * @returns {undefined}
 */
function showspectrogramm()
{

    setViewsfalse();
    spectrogramm = true;
    $('#3Dradio').prop('checked', true);
    $('#canvascontainer').show();
    var sel = document.getElementById('spectroshow');
    sel.className = "active";
    resetview();

    // vertikaler Blickwinkel
    var alpha = 70;
    var haelfte = window.FFTSize / 2;

    //var aspect = x / y;
    var hFoV = haelfte;
    var dist = (hFoV / Math.tan(alpha));
    var height = (dist * Math.tan(alpha)) / 2;

    camera1.position.set(haelfte * 1.5, dist * 1.3, -height * 1.5)
    camera1.rotation.set(-(Math.PI/2),0,0)
    targetsetzen(window.FFTSize)

    //scene1.remove($('#GridYZ'));

}

function showTargetTimeLine()
{
    setViewsfalse();
    $('#canvascontainer').show();
    window.TargetTimeLine = true;
    var sel = document.getElementById('TargetTimeLineShow');
    sel.className = "active";
    resetview();
    
    /*
    var alpha = 70;
    var haelfte = window.FFTSize / 2;
    var hFoV = haelfte;
    var dist = (hFoV / Math.tan(alpha));
    var height = (dist * Math.tan(alpha)) / 2;

    camera1.position.set(haelfte * 1, -(dist * 1.5), -dist * 2)
    camera1.rotation.set((Math.PI/2), 0.03 , -Math.PI/2)
    */
}
/**
 * show/hide the arrows in the scene representing the targets and their phaseangle
 * @param {type} checkbox
 * @returns {undefined}
 */
function showtargetlistArrows(checkbox)
{
    if (checkbox.checked === true)
    {
        var sel = document.getElementById('fftshow');
        sel.className = "active";
        //resetview();

    } else
    {

        arrows = false;
        $('#canvascontainer').show();
    }

}
/**
 * function to change a row of the targetlisttable
 * @param {number} targetnum
 * @param {number} distanz
 * @param {number} DBWert
 * @param {number} Phi
 * @returns {undefined}
 */
function changetargetrow(targetnum, distanz, DBWert, Phi)
{
    var rowid = '#targetrow' + targetnum.toString();
    var row = $(rowid);

    row.find('td').each(function (colIndex, c) {
        if (colIndex = 0)
            c.innerHTML = targetnum;

    });
}
/**
 * adding a new row to the targetlist, called for every target in targetlist-Frame
 * (the table will be cleared every time a new targetframe comes in)
 * @param {type} targetnum
 * @param {type} distanz
 * @param {type} DBWert
 * @param {type} Phi
 * @param {type} Velocity
 * @returns {undefined}
 */
function addtargetrow(targetnum, distanz, DBWert, Phi, Velocity) {

    var row = document.createElement('tr');
    var col1 = document.createElement('td');
    var col2 = document.createElement('td');
    var col3 = document.createElement('td');
    var col4 = document.createElement('td');
    var col5 = document.createElement('td');
    col1.innerHTML = targetnum;
    col2.innerHTML = distanz;
    col3.innerHTML = DBWert;
    col4.innerHTML = (parseFloat(Phi)).toFixed(4);
    col5.innerHTML = Velocity;

    $('#targetlisttable').append(row);
    col1.innerHTML = targetnum;
    col2.innerHTML = distanz;
    col3.innerHTML = DBWert;
    col4.innerHTML = Phi;
    col5.innerHTML = Velocity;

    row.appendChild(col1);
    row.appendChild(col2);
    row.appendChild(col3);
    row.appendChild(col4);
    row.appendChild(col5);
    row.style.color = TargetColors[targetnum]
    $('#targetlisttable').append(row);
    var targettable = document.getElementById('targetlisttable');
    //console.log(targettable);
    for (i = 0; i < targettable.length; i++)
    {
        item.id = 'targetrow' + i;
        item.className = 'targetrow';

    }

}


/**
 * deactivate all other views and show the phasediagramm
 * @returns {undefined}
 */
function showphasediagramm()
{
    
    Anzeige = 'T';
    setViewsfalse();
    phasediagramm = true;
    var sel = document.getElementById('phaseshow');
    sel.className = "active";
    zeichnePhaseDiagramm(window.format);

}
/**
 * draw the empty phase diagramm, actually with a fixed size of 500x500px
 * @param {type} format
 * @returns {undefined}
 */
function zeichnePhaseDiagramm(format)
{
    $("#svgcontainer").css('height', '500px')
    $("#svgcontainer").css('width', '500px')
    $("#svgcontainer").css('margin-top', '10px')
    $("#svgcontainer").css('margin-left', '10%')
    $('#svgcontainer').show();
    $("#svgflaeche").empty().show();

    //$("#svgflaeche").css('height', window.innerHeight * 0.85);
    //$('#svgflaeche').css('width', $('#svgflaeche').parent().css('width'));
    $("#svgflaeche").css('height', '500px')
    $("#svgflaeche").css('width', '500px')
    //$("#svgflaeche").css('border', 'solid 1px orange')

    var breite = parseInt($("#svgflaeche").css('width'));
    var hoehe = parseInt($("#svgflaeche").css('height'));
    center = [breite / 2, hoehe / 2];
    //var Xabstand = breite / 10;
    var Yabstand = (hoehe) / 15;

    var svg = d3.select("#svgflaeche");



    for (i = 1; i <= 7; i++)
    {
        svg.append("circle")
                .attr("cx", breite / 2)
                .attr("cy", hoehe / 2)
                .attr("r", i * Yabstand)
                .attr('id', 'circle' + i)
                .style('fill', 'none')
                .style('stroke', "#ededed")
                .style('stroke-width', "1");


        if (format === 4)
        //beschriftung fuer 'bin#'
        {
            svg.append("text")
                .attr("x", center[0] + ((i - 1) * Yabstand))
                .attr("y", center[1])
                //.attr("dy", "0.1em")
                .attr('id', 'text' + i)
                .text((i - 1) + 'k');
        }

        if (format === 0)
        //beschriftung fuer 'mm'
        {
            svg.append("text")
                .attr("x", center[0] + ((i - 1) * Yabstand))
                .attr("y", center[1])
                //.attr("dy", "0.1em")
                .attr('id', 'text' + i)
                .text((i - 1) * 10 + 'k');
        }


    }

    drawsvgaxes();
}

/**
 * draw the axes of the phasediagramm in the SVG-Tag
 * @returns {undefined}
 */
function drawsvgaxes()
{
    //x-axis
    d3.select('#svgflaeche').append('line')
            .attr('x1', center[0] * 0.0)
            .attr('y1', center[1])
            .attr('x2', center[0] * 2)
            .attr('y2', center[1])
            .attr('id', 'xAchseleft')
            .style('stroke', '#FFFFFF');


    //y-axis
    d3.select('#svgflaeche').append('line')
            .attr('x1', center[0])
            .attr('y1', 0)
            .attr('x2', center[0])
            .attr('y2', center[1] * 2)
            .attr('id', 'xAchseleft')
            .style('stroke', '#FFFFFF');

}


// jquery ui functions

/**
 * adds the functionality for the accordion and making it sortable
 * @returns {undefined}
 */
function addaccordionfunctions()
{
    $(function () {
    $("#accordion")
            .accordion({
                header: "> div > h3", collapsible: true, heightStyle: "content"
            })
            .sortable({
                axis: "y",
                handle: "h3",
                stop: function (event, ui) {
                    // IE doesn't register the blur when sorting
                    // so trigger focusout handlers to remove .ui-state-focus
                    ui.item.children("h3").triggerHandler("focusout");

                    // Refresh accordion to handle new order
                    $(this).accordion("refresh");
                }
            });
    });
}


/**
 * adds the jquery-functionality to all the sliders in the accordion and events
 * when they change to pass the data to the server
 * @returns {undefined}
 */
function addSliderfunctions()
{

    $(function ()
    {
        $("#GainSlider").slider(
                {
                    range: "min",
                    value: 0,
                    min: 0,
                    max: 5,

                    stop: function(event, ui)
                    {

			 if ($("#GainAmount").html() != (ui.value).toString())
                        {
                           // console.log(ui.value)
                            $("#GainAmount").val(ui.value);
                            $("#GainAmount").trigger('change');
                        }
                    }
                })
    });
	
    $(function ()
    {
        $("#CouplingSlider").slider(
                {
                    range: "min",
                    value: 1,
                    min: 0,
                    max: 1,

                    stop: function (event, ui)
                    {

                        var valuearr = ["DC", "AC"];

                        if ($("#Coupling") != (ui.value).toString())
                        {
                            $('#CouplingLabel').html(valuearr[ui.value]);
                            $("#Coupling").val(ui.value);
                            $("#Coupling").trigger('change');
                        }

                    }
				})
    });
	
    $(function ()
    {
        $("#TriggerDelaySlider").slider(
                {
                    range: "min",
                    value: 0,
                    min: 0,
                    max: 7,

                    stop: function(event, ui)
                    {

			 if ($("#TriggerDelayAmount").html() != (ui.value).toString())
                        {
                          //  console.log(ui.value)
                            $("#TriggerDelayAmount").val(ui.value);
                            $("#TriggerDelayAmount").trigger('change');
                        }
                    }
                })
    });

    
    $(function ()
    {
        $("#adcClockDividerSlider").slider(
                {
                    range: "min",
                    value: 5,
                    min: 0,
                    max: 7,

                    stop: function(event, ui)
                    {

			 if ($("#adcClockDivideramount").html() != (ui.value).toString())
                        {
                           // console.log(ui.value)
                            $("#adcClockDivideramount").val(ui.value);
                            $("#adcClockDivideramount").trigger('input');
                        }
                    }
                })
    });
	
	$(function ()
    {
        $("#ProtocolSlider").slider(
                {
                    range: "min",
                    value: 0,
                    min: 0,
                    max: 2,
					stop: function(event, ui)
                    {

			 if ($("#ProtocolID").html() != (ui.value).toString())
                        {
                           
                            $("#ProtocolID").val(ui.value);
                            $("#ProtocolID").trigger('input');
                        }
                    }
                })


    });


    $(function () {
        $("#NumofSamplSlider").slider(
                {
                    range: "min",
                    value: 4,
                    min: 0,
                    max: 6,
                    stop: function (event, ui)
                    {

                        if ($("#NumofSampleamount").html() != (ui.value).toString())
                        {
                            $("#NumofSampleamount").val(ui.value);
                            $('#NumofSamplLabel').html(32 << ui.value);
                            $("#NumofSampleamount").trigger('input');
                        }

                    }
                })
    });
    $(function () {
        $("#NumofRampsSlider").slider(
                {
                    range: "min",
                    value: 4,
                    min: 0,
                    max: 7,
                    stop: function (event, ui)
                    {

                        if ($("#NumofRampsamount").html() != (ui.value).toString())
                        {
                            $("#NumofRampsamount").val(ui.value);
                            $('#numofRampsLabel').html(1 << ui.value);
                            $("#NumofRampsamount").trigger('input');
                        }

                    }
                })
    });
	
	$(function () {
        $("#DCCancelSlider").slider(
              {
                    range: "min",
                    value: 1,
                    min: 0,
                    max: 1,
                    stop: function (event, ui)
                    {
                        var valuearr = ["OFF","ON"];
						
						if ($("#DCCancelamount") != (ui.value).toString())
                        {
                            $('#DCCancelLabel').html(valuearr[ui.value]);
                            $("#DCCancelamount").val(ui.value);
                            $("#DCCancelamount").trigger('input');
                        }

                    }
                })
    });
	
	$(function () {
        $("#FIRSlider").slider(
              {
                    range: "min",
                    value: 0,
                    min: 0,
                    max: 1,
                    stop: function (event, ui)
                    {
                        var valuearr = ["OFF","ON"];
						
						if ($("#FIRamount") != (ui.value).toString())
                        {
                            $('#FIRLabel').html(valuearr[ui.value]);
                            $("#FIRamount").val(ui.value);
                            $("#FIRamount").trigger('input');
                        }

                    }
                })
    });
		
	
    $(function () {
        $("#DownsamplingSlider").slider(
                {
                    range: "min",
                    value: 0,
                    min: 0,
                    max: 7,
                    stop: function (event, ui)
                    {

                        var valuearr = [0, 1, 2, 4, 8, 16, 32, 64];

                        if ($("#Downsamplingamount") != (ui.value).toString())
                        {
                            $('#downsamplLabel').html(valuearr[ui.value]);
                            $("#Downsamplingamount").val(ui.value);
                            $("#Downsamplingamount").trigger('input');
                        }

                    }
                })
    });
	
	    $(function () {
        $("#WindowSlider").slider(
                {
                    range: "min",
                    value: 1,
                    min: 0,
                    max: 1,
                    stop: function (event, ui)
                    {

                        var valuearr = ["OFF","ON"];

                        if ($("#Windowamount") != (ui.value).toString())
                        {
                            $('#WindowLabel').html(valuearr[ui.value]);
                            $("#Windowamount").val(ui.value);
                            $("#Windowamount").trigger('input');
                        }

                    }
                })
    });
	    $(function () {
        $("#UnitSlider").slider(
                {
                    range: "min",
                    value: 0,
                    min: 0,
                    max: 1,
                    stop: function (event, ui)
                    {

                        var valuearr = ["mm","cm"];

                        if ($("#UnitAmount") != (ui.value).toString())
                        {
                            $('#UnitLabel').html(valuearr[ui.value]);
                            $("#UnitAmount").val(ui.value);
                            $("#UnitAmount").trigger('change');
                        }

                    }
                })
    });
    $(function () {
        $("#ScaleSlider").slider(
                {
                    range: "min",
                    value: 0,
                    min: 0,
                    max: 1,
                    stop: function (event, ui)
                    {

                        var valuearr = ["Log","Linear"];

                        if ($("#ScaleID") != (ui.value).toString())
                        {
                            $('#ScaleLabel').html(valuearr[ui.value]);
                            $("#ScaleID").val(ui.value);
                            $("#ScaleID").trigger('input');
                        }

                    }
                })
    });
    $(function ()
    {
        $("#FFTsizeSlider").slider(
                {
                    range: "min",
                    value: 4,
                    min: 0,
                    max: 6,
                    stop: function (event, ui)
                    {


                        if ($("#FFTsizeamount").html() != (ui.value).toString())
                        {

                            //console.log('changed slider: ' + ui.value + ' auf: ' + (32 << ui.value).toString())
                            $("#FFTsizeamount").val(ui.value);
                            $('#FFTsizeLabel').html(32 << ui.value);
                            $("#FFTsizeamount").trigger('input');
                            window.FFTSize = (32 << ui.value)
                            //resetview();
                        }

                    }
                });
    });



    $(function () {
        $("#AverageNSlider").slider(
                {
                    range: "min",
                    value: 1,
                    min: 0,
                    max: 3,
                    stop: function (event, ui)
                    {

                        if ($("#AverageNamount").html() != (ui.value).toString())
                        {
                            $("#AverageNamount").val(ui.value);
                            $('#AverageNLabel').html(ui.value);
                            $("#AverageNamount").trigger('input');
                        }
                    }
                })
    });

    $(function () {
        $("#CFGuardSlider").slider(
                {
                    range: "min",
                    value: 1,
                    min: 0,
                    max: 3,
                    stop: function (event, ui)
                    {

                        if ($("#CFGuardamount").html() != (ui.value).toString())
                        {
                            $("#CFGuardamount").val(ui.value);
                            $('#CFGuardLabel').html(ui.value);
                            $("#CFGuardamount").trigger('input');
                        }

                    }
                })
    });

    $(function () {
        $("#CFSizeSlider").slider(
                {
                    range: "min",
                    value: 10,//3,
                    min: 0,
                    max: 15,
                    stop: function (event, ui)
                    {

                        if ($("#CFSizeamount").html() != (ui.value).toString())
                        {
                            $("#CFSizeamount").val(ui.value);
                            $('#CFSizeLabel').html(ui.value);
                            $("#CFSizeamount").trigger('input');
                        }

                    }
                })
    });

    $(function () {
        $("#CFTresholdSlider").slider(
                {
                    range: "min",
                    value: 8,
                    min: 0,
                    max: 15,
                    stop: function (event, ui)
                    {

                        if ($("#CFTresholdamount").html() != (ui.value).toString())
                        {
                            $("#CFTresholdamount").val(ui.value);
                            $('#CFTresholdLabel').html(ui.value << 1);
                            $("#CFTresholdamount").trigger('input');

                        }

                    }
                })
    });

    $(function () {
        $("#FormatSlider").slider(
                {
                    range: "min",
                    value: 5,
                    min: 0,
                    max: 6,
                    stop: function (event, ui)
                    {


                        if ($("#FormatAmount").html() != (ui.value).toString())
                        {
                            $("#FormatAmount").val(ui.value);
                            if(ui.value == 0){$('#FormatLabel').html('raw A/D');}
                            if(ui.value == 1){$('#FormatLabel').html('FFT comp');}
                            if(ui.value == 2){$('#FormatLabel').html('FFT mag/ph');}
                            if(ui.value == 3){$('#FormatLabel').html('CFAR');}
                            if(ui.value == 4){$('#FormatLabel').html('bin');}
                            if(ui.value == 5){$('#FormatLabel').html('mm');}
                            if(ui.value == 6){$('#FormatLabel').html('cm');}
                             $("#FormatAmount").trigger('input');
                        }

                    }
                })
    });

    $(function () {
        $("#ProtocolSlider").slider(
                {
                    range: "min",
                    value: 0,
                    min: 0,
                    max: 2,
                    stop: function (event, ui)
                    {
                        var valuearr = ["WebGUI","TSV","Binary"];

                        if ($("#ProtocolID") != (ui.value).toString())
                        {
                            $('#OutputFormatLabel').html(valuearr[ui.value]);
                            $("#ProtocolID").val(ui.value);
                            $("#ProtocolID").trigger('input');
                        }

                    }
                })
    });
	
	    $(function () {
        $("#CFARSlider").slider(
                {
                    range: "min",
                    value: 0,
                    min: 0,
                    max: 2,
                    stop: function (event, ui)
                    {
                        var valuearr = ["CA-CFAR","CFAR-GO","CFAR-SO"];

                        if ($("#CFARamount") != (ui.value).toString())
                        {
                            $('#CFARLabel').html(valuearr[ui.value]);
                            $("#CFARamount").val(ui.value);
                            $("#CFARamount").trigger('input');
                        }

                    }
                })
    });
	
    $(function () {
        $("#LineCountSlider").slider(
                {
                    range: "min",
                    value: 10,
                    min: 10,
                    max: 50,
                    stop: function (event, ui)
                    {
                        $('#LineCountLabel').html(ui.value);
                        window.LineCount.LineCountZ = ui.value;
                        gridanpassen(window.FFTSize);
                    }
                });
    });

    $(function () {
        $("#XDividerSlider").slider(
                {
                    range: "min",
                    value: 10,
                    min: 5,
                    max: 20,
                    stop: function (event, ui)
                    {
                        $('#XDividerLabel').html(ui.value);
                        window.LineCount.LineCountX = ui.value;
                        gridanpassen(window.FFTSize);
                    }
                })
    });


}
/**
 * function to detect, which Browser is used,
 * chrome or firefox
 * @returns {undefined}
 */
function getBrowser()
{
    var browserstr = (window.navigator.userAgent).toLowerCase()

    if (browserstr.includes("chrome") ) { browser = 'chrome'}
    if (browserstr.includes("firefox") ) { browser = 'firefox'}
}

$(document).ready(function () {  documentready();  });

 /**
 * @description what to do, when the document is loaded:
 *  setting the height of the accordioncontainer to the windowheight,
 *  adding accordionfuntionality by calling addaccordionfunctions(),
 *  adding jquery-sliderfunctionalitys to the accordions sliders (div-tags),
 *  resize the renderer, when the window is going to be resized *
 */
function documentready()
{       
        
    // style MTI-Mode-Button
   // $("#MTIMode").button();
	$("#LOG").button();
	$("#ISMMode").button();
    
    // add exist-function to jquery
    $.fn.exists = function () {
        return this.length !== 0;
    };
       
     
    //get to know which browser, because mouse behaves different
    getBrowser();
    
    //because of firefox bug for localstorage
    if (browser !== 'firefox') { clearLog(); }
    if (browser == 'firefox') { $('LogCheckbox').change(function(){alert('logging for firefox actually not supported')})}

    // set accordionbackround to windowheight
    $('#accordion').css('height', window.innerHeight);
    addaccordionfunctions();
    // add sliderfunctionalitys
    addSliderfunctions();
    
    // set the standard presets and get already saved presets
    setStandardConfigs();
    getconfigs();
    
    
    //$('#targetlistcaption').click(function () { $('#targetlistbody').toggle() });
    // change view on windowresize
    window.addEventListener('resize', function ()
    {
        window.addEventListener('mouseup', function () {

            var x = parseInt($('#canvascontainer').css('width'));
            $('#canvascontainer').css('height', window.innerHeight * 0.9);
            var y = parseInt($('#canvascontainer').css('height'));
            try
            {
                window.setTimeout(function ()
                {
                    renderer1.setSize(x, y);
                    //resetview();
                }, 1000)
            } catch (ex)
            {
                console.log(ex.toString());
            }

            //location.reload(); // seite neue Laden, wenn Fenstergroeße geändert wird

        });


    });
}