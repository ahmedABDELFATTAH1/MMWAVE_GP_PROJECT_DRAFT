/**
 *
 * @fileOverview script for handling all the dataexchange with the server
 */

/**
 * function to connect to the websocket server and handling incoming and
 * outgoing data
 * @returns {undefined}
 */
function connect()
{
    try {
        
        
        var ipadress = $('#ipadress').val();
        connection = new WebSocket('ws://' + ipadress, []);
        
        /**
        * @event onopen
        * @description what to do when the connection is established
        */
        connection.onopen = function () {


            $('#connectbutt').hide();
            $('#discobutt').show();
            
            render1();
            //console.log(connection.binaryType)
            //Alle Parameter senden, sobald Verbindung besteht
            getparameters(connection);
            


            var elem = document.getElementById('resendConfig');
            var events = jQuery._data( elem, "events" );

            // if there r no events attached ==> attach events
            if (events == null)
            {   $('#SysInfoButt').click(function(){ connection.send('!I\r\n');});
				$('#FEScanButt').click(function(){ connection.send('!A\r\n');});
                $('#FrequScanButt').click(function(){ connection.send('!J\r\n');});
				$('#DetailedErrButt').click(function(){ connection.send('!E\r\n');});
                $('#SetMaxFrequ').click(function(){ connection.send('!K\r\n');});
                $('#frontendselect').change(function()
                { 
                    var frontend = parseInt($('#frontendselect').val());
                    if (frontend == 2) { $('#vcodividerIn').val(8); $('#bandwithIn').val(1000); $('#basefreqin').val(24000)}
                    if (frontend == 4) { $('#vcodividerIn').val(64); $('#bandwithIn').val(5000); $('#basefreqin').val(120000)}
                    if (frontend == 8) { $('#vcodividerIn').val(64); $('#bandwithIn').val(24000); $('#basefreqin').val(118000)}
					if (frontend == 16) { $('#vcodividerIn').val(32); $('#bandwithIn').val(3000); $('#basefreqin').val(60000)}
					if (frontend == 64) { $('#vcodividerIn').val(128); $('#bandwithIn').val(32000); $('#basefreqin').val(289000)}
                    
                    getparameters(connection);
                });
                $('#LEDselect').change(function(){ getSysconfig(connection);});
                $('#FIRMode').change(function(){ getSysconfig(connection);});
                $('#resendConfig').click(function () {  getparameters(connection);  });
                $('.sysconfigInput').on('change', function() {getSysconfig(connection)});
                $('#bandwithIn').change(function(){  getPLLfrequ(connection);  })
                $('#basefreqin').change(function(){  getRFEConfig(connection); })
                $('#vcodividerIn').change(function(){ getRFEConfig(connection); })
                $('.BBprocesstextfields').on('input', function () { getBBSetup(connection);  });
                $('.TargetRecogTextfield').on('input', function () { getBBSetup(connection);  });
				$('.OutputFrameInput').on('input', function () { getSysconfig(connection);  });
				$('.OutputFrameInput').on('change', function () { getSysconfig(connection);  });
				
            }
			setTimeout(function () {connection.send('!A\r\n');}, 100);
		    //setTimeout(function () {connection.send('!J\r\n');}, 100);
			
        };
        /**
         *
         * @event onclose
         * @description what to do when the connection is established
         */
        connection.onclose = function () {
            $('#discobutt').hide();
            $('#connectbutt').show();

            //remove eventhandlers
            $( "#resendConfig" ).off( "click", "**" );
            $( ".sysconfigInput" ).off( "change", "**" );
			$( ".OutputPanelInput" ).off( "change", "**" );
            $( "#bandwithIn" ).off( "change", "**" );
            $( "#basefreqin" ).off( "change", "**" );
            $( "#vcodividerIn" ).off( "change", "**" );
            $( ".BBprocesstextfields" ).off( "input", "**" );
            $( ".TargetRecogTextfield" ).off( "input", "**" );
			$( ".OutputFrameInput" ).off( "change", "**" );//OutputFrameLabel

            console.log('Websocket closed');
        };



        /**
         *
         * @event onerror
         * @description if there are errors log them and close the connection
         */
        connection.onerror = function (error) {

            console.log('WebSocket Error ' + error);
            connection.close();
        };

        /**
         *
         * @event onmessage
         * @description
         * The client expects to receive binary data and reads them
         * into a "blob", a Binary Large OBject.
         * When the Blob is loaded, an Uint8Array is going to the function
         * parsemultipleFrames() which starts to parse the data;
         */
        connection.onmessage = function (e) {

            if (typeof(e.data) == 'string' )
            {
                //console.log('received string: ' + e.data)
                var str = e.data;
                var bytes = [];
                for (var i = 0; i < str.length; ++i) {
                    bytes.push(str.charCodeAt(i));
                }
                //console.log(bytes);
                parsemultipleFrames(bytes);
            }
            else
            {     
                 //console.log('received binary data: ' + e.data)
                 if (window.sceneready == true)
                {
                    readBlob(e.data);
                }
            }
           


        };
    } catch (err) {
        console.log(err.toString());
    }
}


/**
 *
 * @description function, to disconnect and switching the 'connect'-button
 * @returns {undefined}
 */
function disconnect()
{
    try {
        $('#discobutt').hide();
        $('#connectbutt').show();
        cancelAnimationFrame(animationreq);
        connection.close();
    } catch (e) {
        console.log(e.toString());
    }
}
/**
 * reads the incoming Data from a Blob into an Uint8-Array and calls parsemultipleFrames()
 * @param {blob} blob Binary Large Object
 * @returns {undefined}
 */
function readBlob(blob)
{
            var reader = new FileReader();

            reader.addEventListener("loadend", function ()
            {
                // reader.result contains the contents of blob as a typed array
                var view = new Uint8Array(reader.result);
                //console.log(view);
                var begin = String.fromCharCode(view[0]);
                parsemultipleFrames(view);
                //if (begin === '!') { parseData(view); }
            });

            // reads the binary data from e.data
            reader.readAsArrayBuffer(blob);
}
/**
 * try to seperate the Frames with the delimiter '!' and then call parseData()
 * for each sliced part of the Array
 * @param {array} view the Uint8Array with the data to parse
 * @returns {undefined}
 */
function parsemultipleFrames(view)
{

    //save positions of delimiter '!'
    var delim = [];  view.forEach(function(item, index){ if (item === 33) {delim.push(index);}});

   

    //var datArr = []
    delim.forEach(function(item, index)
    {
        if (index < delim.length-1)
        {
            // bis zum nächsten delimiter '!' lesen
            parseData(view.slice(item, delim[index+1]));
			

        }
        else
        {
            //bis zum Ende lesen
            parseData(view.slice(item, view.length-1));
			 
        }

    });

}


/**
 * look for the CMD at position '1' and then parse the Frame depending on the Command
 * @param {array} view an Uint8Array
 * @returns {undefined}
 */
function parseData(view)
{
    //console.log(view)
    if ($('#LogCheckbox').is(':checked')){

        var infostr = "";
        view.forEach(function(item)
        {
            infostr += String.fromCharCode(item)
        })
        
        
      //console.log(infostr);
      writetoLocalStorage(infostr);
    }
    if( $('#ProtocolID').val() == 0){
    // console.log ($('#ProtocolID').val());
	//if( 1){
    var cmd = (String.fromCharCode(view[1]));
    if (cmd == 'R')
    {
        //console.log('range: ' + (view.length).toString())
        zeichneRangeFrame(view, '#0772a1', 'rangeframe')
    }
    if (cmd == 'C') {
        if (spectrogramm === false)
        {
             //console.log('cfar: ' + (view.length).toString())
             zeichneRangeFrame(view, '#ededed', 'cfar');
        }
    }
    if (cmd == 'T') {
        parseTargetFrame(view);
    }
    if (cmd == 'U') {
        logStatusErrorandSysInfo(view);
        parseStatusFrame(view);
    }
    if (cmd == 'P') {
        parsePhaseFrame(view);
    }
    if (cmd == 'E')
    {
        logStatusErrorandSysInfo(view);
		if (view.length <= 8) {
			parseErrorFrame(view);
		} else {
			parseDetailedErrorFrame(view);
		}
    }
    if (cmd == 'I')
    {
        logStatusErrorandSysInfo(view);
        parseSysInfoFrame(view);
    }
    if (cmd == 'D')
    {
        parseDopplerFrame(view);
    }
	}
    if (cmd == 'V')
    {
        parseVersionFrame(view);
    }
}


function logStatusErrorandSysInfo(view)
{
        
        var infostr = "";
        view.forEach(function(item)
        {
            infostr += String.fromCharCode(item)
        })
        
        if (LogTextArr.length < 1000)
        {
            LogTextArr.push(infostr);
        }
        else
        {   
            LogTextArr.shift()
            LogTextArr.push(infostr);
        }
        var logtext = ""
        LogTextArr.forEach(function(item)
        {
            logtext = logtext + item;
        })
        $('#logtext').html(logtext);
}


function parseSysInfoFrame(view)
{
    //console.log(view);
    var uid = "";
    for(var i = 2; i <= 25; i++)
    {
        uid += String.fromCharCode(view[i]);
    }
    $('#UIDLabel').html(uid.toString());
    //console.log('uid: ' + uid);
    var firmware = String.fromCharCode(view[27]);
	//var firmware = str.substring(29, 30);
    firmware = parseInt(firmware.charCodeAt());
    //console.log('firmware: ' + firmware);
	if ($('#VersionLabel').html().length > 0) {
		$('#FirmwareLabel').html("(" + firmware + ")");
	} else {
		$('#FirmwareLabel').html("");
	}
    
    var rfemin = "";
    for(var i = 28; i <= 32; i++)
    {
        rfemin += String.fromCharCode(view[i]);
    }
    //console.log('rfemin: ' + rfemin);
    rfemin = parseInt(rfemin, 16);
	//rfemin = Math.round(rfemin /4);
	//rfemin = rfemin * 250;
    $('#minFrequ').html(rfemin);
    
    if (window.frequScanned == false)
    {        
        $('#basefreqin').val(rfemin + 100);
        window.frequScanned = true;
    }
    
    
    var rfemax = "";
    for(var i = 33; i <= 37; i++)
    {
        rfemax += String.fromCharCode(view[i]);
    }
	rfemax = parseInt(rfemax, 16);
    //console.log('rfemax: ' + rfemax);
	//rfemax = Math.round(rfemax /4);
	//rfemin = rfemin * 250;
    $('#maxFrequ').html(rfemax);
}


function parseVersionFrame(view)
{
//	console.log(view);
	
	// get the length of the version frame
	var length = "";
	for(var i = 2; i <= 5; i++) {
        length += String.fromCharCode(view[i]);
    }
	length = parseInt(length, 16);
//	console.log(length);
	
	// now read the content
	var info = "";
	for(var i = 0; i <= length+5; i++) {
        info += String.fromCharCode(view[i]);
    }
//	console.log(info);
	
	// parse FW version info
	// leave first S alone (around char 36), start searching after it
	var softwareIdx = info.indexOf("S", 40);
//	console.log(softwareIdx);
	var versionCheckIn = info.substring(softwareIdx+3, softwareIdx+13);
//	console.log(versionCheckIn);
	var versionDate = info.substring(softwareIdx+14, softwareIdx+22);
//	console.log(versionDate);
	var version = info.substring(softwareIdx+23, softwareIdx+28);
//	console.log(version);
	$('#VersionLabel').html("v" + version);
	$('#VersionDateLabel').html(" (" + versionDate + ")");
	$('#VersionCheckInLabel').html(versionCheckIn);
	
	// parse protocol version info
	var protocolIdx = info.indexOf("C", 0);
//	console.log(protocolIdx);
   	var protocolSpec = info.substring(protocolIdx+3, protocolIdx+5);
//	console.log(protocolSpec);
	var protocolDate = info.substring(protocolIdx+6, protocolIdx+14);
//	console.log(protocolDate);
	var protocol = info.substring(protocolIdx+15, protocolIdx+20);
//	console.log(protocol);
	$('#ProtocolSpecLabel').html(protocolSpec);
	$('#ProtocolLabel').html("v" + protocol);
	$('#ProtocolDateLabel').html(" (" + protocolDate + ")");
}


function parseErrorFrame(view)
{
    var stelle1 = String.fromCharCode(view[2]);
    var stelle2 = String.fromCharCode(view[3]);
    var stelle3 = String.fromCharCode(view[4]);
    var stelle4 = String.fromCharCode(view[5]);
    var stelle5 = String.fromCharCode(view[6]);
    var hexzahl = stelle1 + stelle2 + stelle3 + stelle4 + stelle5;
    
    hexzahl = parseInt(hexzahl, 16);
    var ErrInBin = dec2bin(hexzahl);
    
    if (ErrInBin.length < 2) { ErrInBin = "0000" + ErrInBin }
    if (ErrInBin.length < 3) { ErrInBin = "000" + ErrInBin }
    if (ErrInBin.length < 4) { ErrInBin = "00" + ErrInBin }
    if (ErrInBin.length < 5) { ErrInBin = "0" + ErrInBin }
    
    //console.log(ErrInBin);
    
    var err5 = ErrInBin.substring(0,1);
    var err4 = ErrInBin.substring(1,2);
    var err3 = ErrInBin.substring(2,3);
    var err2 = ErrInBin.substring(3,4);
    var err1 = ErrInBin.substring(4,5);
    
    var warncolor = "yellow"; var errorcolor = "red";    
    
    
    if ( err5 === "1") {$('#err5').css('color', warncolor);} 
    else {$('#err5').css('color', 'white');} 
    if ( err4 === "1") {$('#err4').css('color', warncolor);} 
    else {$('#err4').css('color', 'white');} 
    if ( err3 === "1") {$('#err3').css('color', warncolor);} 
    else {$('#err3').css('color', 'white');} 
    if ( err2 === "1") {$('#err2').css('color', warncolor);} 
    else {$('#err2').css('color', 'white');} 
    if ( err1 === "1") {$('#err1').css('color', warncolor);} 
    else {$('#err1').css('color', 'white');}
    
}


function parseDetailedErrorFrame(view)
{
	var stelle1 = String.fromCharCode(view[2]);
	var stelle2 = String.fromCharCode(view[3]);
	var stelle3 = String.fromCharCode(view[4]);
	var stelle4 = String.fromCharCode(view[5]);
	var stelle5 = String.fromCharCode(view[6]);
	var stelle6 = String.fromCharCode(view[7]);
	var stelle7 = String.fromCharCode(view[8]);
	var stelle8 = String.fromCharCode(view[9]);
	
	
	var hexzahl = stelle1 + stelle2 + stelle3 + stelle4 + stelle5 + 
				  stelle6 +	stelle7 + stelle8;
	
//	console.log(hexzahl);
	
	hexzahl = parseInt(hexzahl, 16);
    var ErrInBin = dec2bin(hexzahl);

//  console.log(ErrInBin);
	
	if (ErrInBin.length <  2) { ErrInBin = "000000000000000000000000000000" + ErrInBin }
	if (ErrInBin.length <  3) { ErrInBin = "00000000000000000000000000000" + ErrInBin }
	if (ErrInBin.length <  4) { ErrInBin = "0000000000000000000000000000" + ErrInBin }
	if (ErrInBin.length <  5) { ErrInBin = "000000000000000000000000000" + ErrInBin }
	if (ErrInBin.length <  6) { ErrInBin = "00000000000000000000000000" + ErrInBin }
	if (ErrInBin.length <  7) { ErrInBin = "0000000000000000000000000" + ErrInBin }
	if (ErrInBin.length <  8) { ErrInBin = "000000000000000000000000" + ErrInBin }
	if (ErrInBin.length <  9) { ErrInBin = "00000000000000000000000" + ErrInBin }
	if (ErrInBin.length < 10) { ErrInBin = "0000000000000000000000" + ErrInBin }
	if (ErrInBin.length < 11) { ErrInBin = "000000000000000000000" + ErrInBin }
	if (ErrInBin.length < 12) { ErrInBin = "00000000000000000000" + ErrInBin }
	if (ErrInBin.length < 13) { ErrInBin = "0000000000000000000" + ErrInBin }
	if (ErrInBin.length < 14) { ErrInBin = "000000000000000000" + ErrInBin }
	if (ErrInBin.length < 15) { ErrInBin = "00000000000000000" + ErrInBin }
	if (ErrInBin.length < 16) { ErrInBin = "0000000000000000" + ErrInBin }
	if (ErrInBin.length < 17) { ErrInBin = "000000000000000" + ErrInBin }
	if (ErrInBin.length < 18) { ErrInBin = "00000000000000" + ErrInBin }
	if (ErrInBin.length < 19) { ErrInBin = "0000000000000" + ErrInBin }
	if (ErrInBin.length < 20) { ErrInBin = "000000000000" + ErrInBin }
	if (ErrInBin.length < 22) { ErrInBin = "00000000000" + ErrInBin }
	if (ErrInBin.length < 23) { ErrInBin = "0000000000" + ErrInBin }
	if (ErrInBin.length < 24) { ErrInBin = "000000000" + ErrInBin }
	if (ErrInBin.length < 25) { ErrInBin = "00000000" + ErrInBin }
	if (ErrInBin.length < 26) { ErrInBin = "0000000" + ErrInBin }
	if (ErrInBin.length < 27) { ErrInBin = "000000" + ErrInBin }
	if (ErrInBin.length < 28) { ErrInBin = "00000" + ErrInBin }
	if (ErrInBin.length < 29) { ErrInBin = "0000" + ErrInBin }
	if (ErrInBin.length < 30) { ErrInBin = "000" + ErrInBin }
	if (ErrInBin.length < 31) { ErrInBin = "00" + ErrInBin }
	if (ErrInBin.length < 32) { ErrInBin = "0" + ErrInBin }
        
//    console.log(ErrInBin);
	
	var err32 = ErrInBin.substring(0,1);
    var err31 = ErrInBin.substring(1,2);
    var err30 = ErrInBin.substring(2,3);
    var err29 = ErrInBin.substring(3,4);
    var err28 = ErrInBin.substring(4,5);
	var err27 = ErrInBin.substring(5,6);
	var err26 = ErrInBin.substring(6,7);
	var err25 = ErrInBin.substring(7,8);
	var err24 = ErrInBin.substring(8,9);
	var err23 = ErrInBin.substring(9,10);
	var err22 = ErrInBin.substring(10,11);
	var err21 = ErrInBin.substring(11,12);
	var err20 = ErrInBin.substring(12,13);
	var err19 = ErrInBin.substring(13,14);
	var err18 = ErrInBin.substring(14,15);
	var err17 = ErrInBin.substring(15,16);
	var err16 = ErrInBin.substring(16,17);
	var err15 = ErrInBin.substring(17,18);
	var err14 = ErrInBin.substring(18,19);
	var err13 = ErrInBin.substring(19,20);
	var err12 = ErrInBin.substring(20,21);
	var err11 = ErrInBin.substring(21,22);
	var err10 = ErrInBin.substring(22,23);
	var err9  = ErrInBin.substring(23,24);
	var err8  = ErrInBin.substring(24,25);
	var err7  = ErrInBin.substring(25,26);
	var err6  = ErrInBin.substring(26,27);
	var err5  = ErrInBin.substring(27,28);
	var err4  = ErrInBin.substring(28,29);
	var err3  = ErrInBin.substring(29,30);
	var err2  = ErrInBin.substring(30,31);
	var err1  = ErrInBin.substring(31,32);

	if ( err1 === "1") {
		$("#error1").css("background-color", "red");
	} else {
		$("#error1").css("background-color", "transparent");
	}
	if ( err2 === "1") {
		$("#error2").css("background-color", "red");
	} else {
		$("#error2").css("background-color", "transparent");
	}
	if ( err3 === "1") {
		$("#error3").css("background-color", "red");
	} else {
		$("#error3").css("background-color", "transparent");
	}
	if ( err4 === "1") {
		$("#error4").css("background-color", "red");
	} else {
		$("#error4").css("background-color", "transparent");
	}
	if ( err5 === "1") {
		$("#error5").css("background-color", "red");
	} else {
		$("#error5").css("background-color", "transparent");
	}
	if ( err6 === "1") {
		$("#error6").css("background-color", "red");
	} else {
		$("#error6").css("background-color", "transparent");
	}
	if ( err7 === "1") {
		$("#error7").css("background-color", "red");
	} else {
		$("#error7").css("background-color", "transparent");
	}
	if ( err8 === "1") {
		$("#error8").css("background-color", "red");
	} else {
		$("#error8").css("background-color", "transparent");
	}
	if ( err9 === "1") {
		$("#error9").css("background-color", "red");
	} else {
		$("#error9").css("background-color", "transparent");
	}
	if ( err10 === "1") {
		$("#error10").css("background-color", "red");
	} else {
		$("#error10").css("background-color", "transparent");
	}
	if ( err11 === "1") {
		$("#error11").css("background-color", "red");
	} else {
		$("#error11").css("background-color", "transparent");
	}
	if ( err12 === "1") {
		$("#error12").css("background-color", "red");
	} else {
		$("#error12").css("background-color", "transparent");
	}
	if ( err13 === "1") {
		$("#error13").css("background-color", "red");
	} else {
		$("#error13").css("background-color", "transparent");
	}
	if ( err14 === "1") {
		$("#error14").css("background-color", "red");
	} else {
		$("#error14").css("background-color", "transparent");
	}
	if ( err15 === "1") {
		$("#error15").css("background-color", "red");
	} else {
		$("#error15").css("background-color", "transparent");
	}
	if ( err16 === "1") {
		$("#error16").css("background-color", "red");
	} else {
		$("#error16").css("background-color", "transparent");
	}
	if ( err17 === "1") {
		$("#error17").css("background-color", "red");
	} else {
		$("#error17").css("background-color", "transparent");
	}
	if ( err18 === "1") {
		$("#error18").css("background-color", "red");
	} else {
		$("#error18").css("background-color", "transparent");
	}
	if ( err19 === "1") {
		$("#error19").css("background-color", "red");
	} else {
		$("#error19").css("background-color", "transparent");
	}
	if ( err20 === "1") {
		$("#error20").css("background-color", "red");
	} else {
		$("#error20").css("background-color", "transparent");
	}
	if ( err21 === "1") {
		$("#error21").css("background-color", "red");
	} else {
		$("#error21").css("background-color", "transparent");
	}
	if ( err22 === "1") {
		$("#error22").css("background-color", "red");
	} else {
		$("#error22").css("background-color", "transparent");
	}
	if ( err23 === "1") {
		$("#error23").css("background-color", "red");
	} else {
		$("#error23").css("background-color", "transparent");
	}
	if ( err24 === "1") {
		$("#error24").css("background-color", "red");
	} else {
		$("#error24").css("background-color", "transparent");
	}
	if ( err25 === "1") {
		$("#error25").css("background-color", "red");
	} else {
		$("#error25").css("background-color", "transparent");
	}
	if ( err26 === "1") {
		$("#error26").css("background-color", "red");
	} else {
		$("#error26").css("background-color", "transparent");
	}
	if ( err27 === "1") {
		$("#error27").css("background-color", "red");
	} else {
		$("#error27").css("background-color", "transparent");
	}
	if ( err28 === "1") {
		$("#error28").css("background-color", "red");
	} else {
		$("#error28").css("background-color", "transparent");
	}
	if ( err29 === "1") {
		$("#error29").css("background-color", "red");
	} else {
		$("#error29").css("background-color", "transparent");
	}
	if ( err30 === "1") {
		$("#error30").css("background-color", "red");
	} else {
		$("#error30").css("background-color", "transparent");
	}
	if ( err31 === "1") {
		$("#error31").css("background-color", "red");
	} else {
		$("#error31").css("background-color", "transparent");
	}
	if ( err32 === "1") {
		$("#error32").css("background-color", "red");
	} else {
		$("#error32").css("background-color", "transparent");
	}
}


/**
 * parse the TargetFrame
 * @param {array} view
 * @returns {undefined}
 */
function parseTargetFrame(view)
{


    if ($('#2Dradio').is(":checked")) { deleteOldArrows();}
    if ($('#3Dradio').is(":checked") && $('#targetview').is(":checked")) { fadeaway(Backsteps, Sichtweite, 'targetarrows'); }

    
    // delete the old arrows if the checkbox is unchecked
    if ($('#targetview').is(":checked") !== true) {deleteOldArrows();}
    var format = String.fromCharCode(view[2]);
	//console.log(format);
    formatsetzen(format);


    //addText('distance in: ' + format, 200, -184, 0.1, 6, 'distanzlabel');

    var gainDB = String.fromCharCode(view[3]);
    var targets = (view.slice(4));
    //console.log(targets.toString());
    var s = "";
    for (i = 0; i < targets.length - 1; i++)
    {
        s += (String.fromCharCode(targets[i]));
    }
    parseTargetData(s, format);


}
/**
 * setting format, for example 'mm' or 'cm' 
 * @param {type} format
 * @returns {undefined}
 */
function formatsetzen(format)
{
//    console.log(format);
//    console.log(window.format);
    if (window.format != format) {

        gridanpassen(window.FFTSize)
    }
    window.format = parseInt(format);
    var formatstr = ""
	 if (format == 0) {  formatstr = "mm"   }
    if (format == 1) {  formatstr = "cm"   }


    $('#EinheitsLabel').html(formatstr);
}
/**
 * parses the targetdata for each target,
 * function is called from parseTargetFrame() and parseTargetString()
 * @param {string} s a string containing the Data for all targets
 * @param {number} format the format as Integer, 5 = 'mm'
 * @returns {undefined}
 */
function parseTargetData(s, format)
{

    var targetdata = [];
    var target;
    for (i = 0; i < s.length-1; i = i + 14)
    {
        target = s.substring(i, i + 14);     
        targetdata.push(target);
        
    }
    $('#targetlistbody').empty();
    phasendiagrammleeren();
    if (window.TargetTimeLine == true)
        {
            Backsteps = parseInt(window.FFTSize / window.LineCount.LineCountZ);
            drawtargetpoints(targetdata);            
        }
	

     targetdata.forEach(function (targetstr)
    {
        var targetnum = parseInt(targetstr.substring(0, 1), 16);
        var distanz = parseInt(targetstr.substring(1, 5), 16);
        var DBWert = (targetstr.substring(5, 7).charCodeAt(0)) - 174;
        var Phi = parseInt((targetstr.substring(7, 11)), 16);
        if (Phi > 32767) {  Phi = (Phi-65535);  }
        Phi = ((((Phi)/1000.0))).toFixed(4); //convert to 0 .. 2Pi
        //console.log(targetnum + " " + Phi);
        var Velocity = parseInt((targetstr.substring(11, 15)), 16);
        if (Velocity > 32767) {  Velocity = Velocity-65535;  }

        addtargetrow(targetnum, distanz, DBWert, Phi, Velocity);
        if (phasediagramm === true)
        {
            var x = calckartesianX(distanz, Phi);
            var y = calckartesianY(distanz, Phi);
            drawsvgPhiLine(targetnum, x, y, distanz, format);
        } 
        else
        {
            if (DBWert > -140)
            {
                var acc = accuracy;
                var xval = distanz / acc;
                
                if ($('#targetview').is(":checked"))
                {
                    drawArrow( xval, Phi, DBWert, TargetColors[targetnum]);
                }                
                
            }

        }
//        if (window.TargetTimeLine == true)
//        {
//            drawTargetPoint(targetnum, distanz, accuracy);
//            if (targetnum === 15) {window.TTCounter++;}
//        }
    });

}
/**
 * parsing the Status-Frame 'U'
 * @param {type} view
 * @returns {undefined}
 */
function parseStatusFrame(view)
{
    //console.log(view)
    var str = "";
    for (i = 0; i < view.length; i++)
    {
        str += (String.fromCharCode(view[i]));
    }
    var format = str.substring(2, 3);

    formatsetzen(format);
    window.format = parseInt(format);
    //console.log(str)
    var gain = str.substring(3, 4);
    gain = parseInt(gain.charCodeAt() - 174);
    $('#StatusGain').html(gain)

    accuracy = parseInt(str.substring(4, 8), 16);
    accuracy /= 10;
    $('#accuracyLabel').html(accuracy);
	if(parseInt(format) == 1){
		accuracy /= 10;
		
	}
    //console.log(str.substring(4, 8) + ' ' + accuracy)

    var laenge = parseInt(str.substring(8, 12), 16);
	if(parseInt(format) == 1){
		   
		laenge=Math.round(laenge/10);
		
    }
    if (laenge != $('#StatusMaxRange').html()){ gridanpassen(window.FFTSize); }
    $('#StatusMaxRange').html(laenge);
    //console.log(str.substring(8, 12) + ' ' + laenge)

    var Ramptime = parseInt(str.substring(12, 16), 16);
    $('#ramptime').val(Ramptime);
    //console.log(str.substring(12, 16) + ' ' + Ramptime)
    var Bandwith = parseInt(str.substring(16, 20), 16);
	if(Bandwith>32767)
	{
	
		Bandwith ^= 0xffff;
		//console.log(Bandwith)
		Bandwith++;
		//console.log(Bandwith)		
		Bandwith=-Bandwith;
		
	}
    $('#bandwith').html(Bandwith);
   // console.log(str.substring(16, 20) + ' ' + Bandwith)
    var TSLM = parseInt(str.substring(20, 24), 16);
    TSLM = (1/ (parseInt(TSLM) / 100000)).toFixed(2);
    //console.log(str.substring(20, 24) + ' ' + TSLM)
    $('#tslm').html(TSLM);

}


/**
 * parse the data of the phase-frame, used to visualize the
 * phaseangles with color in the spectrogramm
 * @param {type} view an Array containing the phaseframe-information
 * @returns {undefined}
 */
function parsePhaseFrame(view)
{
    var Phi = 0;
    var farbwert = 0;

    for (var i = 14; i < view.length - 2; i++)
    {
  Phi = ((1.0+((view[i]-143)/110.0))/2.0).toFixed(4); //convert to -110 .. 110 --> -1 .. 1 --> 0 .. 1
        farbwert = (Phi);

        if (usedPhaseArray == 0)
        {


            PhaseArray0.push(farbwert);
            if (i == view.length - 3)
            {
                usedPhaseArray = 1;
            }

        }
        else if (usedPhaseArray == 1)
        {

            PhaseArray1.push(farbwert);
            if (i == view.length - 3)
            {
                usedPhaseArray = 0;
    PhaseArray0 = [];
            }

        }
    }

    if (usedPhaseArray == 0)
    {
  PhaseArray0 = [];
    }
    if (usedPhaseArray == 1)
    {
  PhaseArray1 = [];
    }
}
/**
 * calculate the Difference between the phaseangles from the Frame before,
 * not used actually
 * @param {type} oldPhases an array with the old phaseangles
 * @param {type} newPhases an array with the new phaseangles
 * @returns {undefined}
 */
function getPhaseDelta(oldPhases, newPhases)
{
    //console.log('oldphase: ' + oldPhases)
    //console.log('newphase: ' + newPhases)
    DeltaPhase = [];
    for (var j = 0; j < oldPhases.length; j++)
    {
        var delta = 100-Math.abs(((oldPhases[j] - newPhases[j])))
        DeltaPhase.push(delta);

    }
    //console.log(Delta)
    if (usedPhaseArray == 0) {PhaseArray0 = []}
    if (usedPhaseArray == 1) {PhaseArray1 = []}

}
/**
 * function for parsing the Dopplerframe,
 * not implemented yet
 * @param {type} view
 * @returns {undefined}
 */
function parseDopplerFrame(view)
{
    var s = "";
    view.forEach(function(item){
        s += String.fromCharCode(item);
    })

    //console.log(s)
    var Werte = s.split('/');
}

/**
 * Drawing the Range-Frame
 * @param {array} view
 * @param {string} hexcolor
 * @returns {undefined}
 */
function zeichneRangeFrame(view, hexcolor, datatype)
{
    // vergleichen ob sich an der Range was geaendert hat
    // und entsprechend Achsen anpassen
    //console.log(view)

    var datenlaenge = 0;
    for (i = 2; i <= 5; i++)
    {
       datenlaenge += (String.fromCharCode(view[i]));
    }
    datenlaenge = parseInt(datenlaenge, 16);
//	 console.log(datenlaenge);
    var laenge = (parseInt(window.FFTSize));
//	 console.log(laenge);
    //console.log('Rframe fftsize client:' + laenge)
    //console.log('Rframe fftsize server: ' + datenlaenge)
    if (datenlaenge !== laenge)
    {
		window.FFTSize = parseInt(datenlaenge);
        gridanpassen(window.FFTSize);
        //resetview();
    }

    if ($('#2Dradio').is(":checked")) {deleteolddata(datatype);    }
    // delete the old arrows if the checkbox is unchecked
    if ($('#targetview').is(":checked") !== true) {deleteOldArrows();}
    if (spectrogramm === false && FFT == true)
    {
        // alte Daten nach hinten ruecken
        if ($('#3Dradio').is(":checked"))
        {
            Backsteps = parseInt(window.FFTSize / window.LineCount.LineCountZ);
            Sichtweite = window.FFTSize;
            //console.log('zeichne: ' + datatype)
            fadeaway(Backsteps, Sichtweite, datatype);
        }
        //console.log(view.slice(6, view.length-2))
        printchart(view.slice(14, view.length-2), hexcolor, datatype);
        //drawSpline(view.slice(6, view.length-2), hexcolor, datatype);

    }
/* 	    if (spectrogramm === false && RAW == true)
    {

        //console.log(view.slice(6, view.length-2))
        printchartRAW(view.slice(14, view.length-2), hexcolor, datatype);
        //drawSpline(view.slice(6, view.length-2), hexcolor, datatype);

    } */
    if (spectrogramm === true)
    {
        if ($('#3Dradio').is(":checked"))
        {
            //var Scale = scaleX(window.FFTSize)
//            Sichtweite = 512;
//            if (window.FFTSize >= 512)  {  Sichtweite = 256 }
//            if (window.FFTSize <= 512)  {  Sichtweite = 256 }
//            if (window.FFTSize <= 256)  {  Sichtweite = 128 }
//            if (window.FFTSize <= 128)  {  Sichtweite = 128 }
//            Backsteps = 1;
            
            
            Backsteps = parseInt(window.FFTSize / window.LineCount.LineCountZ);
            Backsteps /= 10;
            Sichtweite = window.FFTSize;
            
            fadeaway(Backsteps, Sichtweite, 'rangeframe');
            printchart(view.slice(14, view.length-2), hexcolor, datatype);
            //drawSpline(view.slice(6, view.length-5), hexcolor, datatype);
        }

    }


}


/**
 * get all parameters and then send them with a timeout of 200ms to the server when connecting
 * @param {object} connection the connection object initialized by connect()
 * @returns {undefined}
 */
function getparameters(connection)
{
    setTimeout(function() {  getSysconfig(connection) } , 200);
    setTimeout(function() {  getRFEConfig(connection)} , 400);
    setTimeout(function () { getPLLfrequ(connection)} , 600);
    setTimeout(function () { getBBSetup(connection) }, 800);
	setTimeout(function () { getVersionFrame(connection) }, 1000);
				
}


/**
 * function to get the parameters of the Systemconfig and then send them to the server
 * @param {object} connection the connection object initialized by connect()
 * @returns {undefined}
 */
var getSysconfig = function(connection)
{
    var endstr = "\r\n";
    // get sys config bools
	var raw = booltoInt(($('#raw').prop('checked')));	
	var coupling = parseInt($('#Coupling').val());	
	
	var slf = booltoInt(($('#slf').prop('checked')));
    var slp = booltoInt(($('#slp').prop('checked')));	
    var trg = booltoInt(($('#trg').prop('checked')));
    var ser1 = booltoInt(($('#ser1').prop('checked')));
    var ser2 = booltoInt(($('#ser2').prop('checked')));
	var AGC = booltoInt(($('#AGCMode').prop('checked')));
    var gain = $('#GainAmount').val();
    gain = shiftIt(gain, 14);
    var fmt = parseInt($('#UnitAmount').val());	
    fmt = shiftIt(fmt, 26);
	//console.log(fmt);
	var LEDval = $('#LEDselect').val();
    LEDval = shiftIt(LEDval, 24);
	
    
	var cmp = booltoInt(($('#cmp').prop('checked')));
    var r = booltoInt(($('#r').prop('checked')));
    var c = booltoInt(($('#c').prop('checked')));
    var p = booltoInt(($('#p').prop('checked')));
    var tl = booltoInt(($('#tl').prop('checked')));
    var st = booltoInt(($('#st').prop('checked')));
    var err = booltoInt(($('#err').prop('checked')));       
	
	var protocol = $('#ProtocolID').val();
    protocol = shiftIt(protocol, 18);
	    
    var frontend = parseInt($('#frontendselect').val(), 10);
    frontend = shiftIt(frontend, 20);
	
	var log = parseInt($('#ScaleID').val());  
	log = shiftIt(log, 27);
	
    //frontend = dec2bin(frontend);    console.log(frontend)

    var delay = $('#TriggerDelayAmount').val();
    delay = shiftIt(delay, 29);
	
	if ((slf === 1) && (trg === 1)) {
		document.getElementById("trg").checked = false;
		trg = 0;
	}
	
	if ((raw === 1) | (cmp === 1)) {
		document.getElementById("p").checked = false;
		document.getElementById("r").checked = false;
		document.getElementById("c").checked = false;
		document.getElementById("tl").checked = false;	
		document.getElementById("p").disabled = true;
		document.getElementById("r").disabled = true;
		document.getElementById("c").disabled = true;
		document.getElementById("tl").disabled = true;	
	} else {
		document.getElementById("raw").disabled = false;
		document.getElementById("cmp").disabled = false;
		document.getElementById("p").disabled = false;
		document.getElementById("r").disabled = false;
		document.getElementById("c").disabled = false;
		document.getElementById("tl").disabled = false;	
	}
	if ((raw === 1) ) {
        raw = Math.pow(2, 4);
		document.getElementById("cmp").checked = false;				
		document.getElementById("cmp").disabled = true;		
		cmp = 0;
		p=0;
		r=0;
		c=0;
		tl=0;
		
    } else {
        raw = 0;
    }
	if ((cmp === 1) ) {
        cmp = Math.pow(2, 5);
		document.getElementById("raw").checked = false;			
		document.getElementById("raw").disabled = true;	
		p=0;
		r=0;
		c=0;
    } else {
        cmp = 0;
    }	

	if (coupling === 1) {
	   coupling = Math.pow(2, 28);
    } 
	else {
        coupling = 0;
    }
	
    if (trg === 1) {
        trg = Math.pow(2, 0);
    } else {
        trg = 0;
    }
    if (slf === 1) {
        slf = Math.pow(2, 1);
    } else {
        slf = 0;
    }
    if (slp === 1) {
        slp = Math.pow(2, 2);
    } else {
        slp = 0;
    }

	if (p === 1) {
        p = Math.pow(2, 6);
    } else {
        p = 0;
    }	
    if (r === 1) {
        r = Math.pow(2, 7);
    } else {
        r = 0;
    }
    if (c === 1) {
        c = Math.pow(2, 8);
    } else {
        c = 0;
    }
	if (tl === 1) {
        tl = Math.pow(2, 9);
    } else {
        tl = 0;
    }
    if (st === 1) {
        st = Math.pow(2, 10);
    } else {
        st = 0;
    }
    if (err === 1) {
        err = Math.pow(2, 11);
    } else {
        err = 0;
    }
    if (ser1 === 1) {
        ser1 = Math.pow(2, 12);
    } else {
        ser1 = 0;
    }
    if (ser2 === 1) {
        ser2 = Math.pow(2, 13);
    } else {
        ser2 = 0;
    }
    if (AGC === 1) {
        AGC = Math.pow(2, 17);
    } else {
        AGC = 0;
    }


	var summe = trg + slf + slp + raw + cmp + p + r + c + tl + st + err + ser1 + ser2 + gain + AGC + protocol + frontend + LEDval + fmt + log + delay + coupling;
    summe = summe.toString(16);
    
    var sysconfig = (hexauffuellen(summe, 8));
    sysconfig = "!S" + sysconfig.toUpperCase() + endstr;
    
    var oldconfigstr = $('#actConfig').html();    
    var configstr = updateLastConfig(oldconfigstr, "!S");
	
/*      if(raw != 0){
		 FFT = false;
		 RAW = true;
	 }
	 else {
		 RAW = false;
		 FFT = true;
	 } */
	// console.log(raw)
	
    
    //console.log(sysconfig);
    setTimeout(function () {
        $('#actConfig').html(configstr + sysconfig);
        connection.send(sysconfig);
    }, 100);
}

/**
 * get the RFEConfig and send it to the server
 * @param {object} connection the connection object initialized by connect()
 * @returns {undefined}
 */
function getRFEConfig(connection)
{
    var endstr = "\r\n";
    var basefrequ = parseInt($('#basefreqin').val()*4);
	//console.log('basefrequ: ' + basefrequ)
	basefrequ = basefrequ ;
	//basefrequ = Math.floor(basefrequ / 250);
    //console.log('basefrequ: ' + basefrequ)
    basefrequ = shiftIt(basefrequ, 0);
    //console.log('basefrequ formated : ' + basefrequ)

    var VCOdivider = parseInt($('#vcodividerIn').val());
    //console.log('vcodivider: ' + VCOdivider);
    VCOdivider = shiftIt(VCOdivider, 21);
    //console.log('VCO formated: ' + VCOdivider);

    var RFEConfig = basefrequ + VCOdivider;
    RFEConfig = RFEConfig.toString(16);
    RFEConfig = '!F' + hexauffuellen(RFEConfig.toUpperCase(), 8) + endstr;
    
    var oldconfigstr = $('#actConfig').html();    
    var configstr = updateLastConfig(oldconfigstr, "!F");
        
    //console.log(RFEConfig);
    setTimeout(function () {
        $('#actConfig').html(configstr + RFEConfig);
        connection.send(RFEConfig);
    }, 100);
}

  /*   function  flip( c) {
        return (c == '0') ? '1' : '0';
    } */

/**
 * get the PLLfrequ and send it to the server
 * @param {object} connection the connection object initialized by connect()
 * @returns {undefined}
 */
function getPLLfrequ(connection)
{
    var endstr = "\r\n";
    //get bandwith from GUI 16 Bits linksshift 16
    var bandwith = parseInt($('#bandwithIn').val());
    //console.log('bandwith: ' + bandwith);
    
    
    if (bandwith >= 0) 
    {
        bandwith = shiftIt(bandwith/2, 0);
    }
    else // zweierkomplement fuer negative bandweiten
    {      
		bandwith= (Math.abs(bandwith/2));
		bandwith ^= 0xffff;
		//console.log(bandwith)
		bandwith++;
		//console.log(bandwith)	
        bandwith = shiftIt(bandwith, 0);
		
    }
    
    //console.log('bandwidth formated: ' + bandwith);
	bandwith = Math.floor(bandwith );
	//console.log(bandwith);
    bandwith = hexauffuellen(bandwith.toString(16), 8);	
	
    var PLLfrequ = '!P' + bandwith.toUpperCase() + endstr;
    
    var oldconfigstr = $('#actConfig').html();    
    var configstr = updateLastConfig(oldconfigstr, "!P");    
    
    setTimeout(function () {
        $('#actConfig').html(configstr + PLLfrequ);
        connection.send(PLLfrequ);
    }, 100);
}

/**
 * get the BBSetup and send it to the server
 * @param {object} connection the connection object initialized by connect()
 * @returns {undefined}
 */
function getBBSetup(connection)
{

    var endstr = "\r\n";

    //BBSetup
    var BBSetup = "";
    var adcClockDivider = $('#adcClockDivideramount').val();
    var numofSample = $('#NumofSampleamount').val();
    var numofRamps = $('#NumofRampsamount').val();
    var downsamplamount = $('#Downsamplingamount').val();
    var FFTsize = $('#FFTsizeamount').val();
    var AverageN = $('#AverageNamount').val();
    var CFGuard = $('#CFGuardamount').val();
    var CFSize = $('#CFSizeamount').val();
    var CFTreshold = $('#CFTresholdamount').val();
	var CFType = $('#CFARamount').val();
	var DC = $('#DCCancelamount').val();
	var FIR = $('#FIRamount').val();
	var WINDOW = $('#Windowamount').val();
    //var Format = $('#FormatAmount').val();

    //console.log('adcClockDivider: ' + adcClockDivider);
    //console.log('numofSample: ' + numofSample);
    //console.log('numofRamps: ' + numofRamps);
    //console.log('downsamplamount: ' + downsamplamount);
    //console.log('FFTsize:' + FFTsize);

    //console.log('AverageN: ' + AverageN);
    //console.log('CFGuard: ' + CFGuard);
    //console.log('CFSize: ' + CFSize);
    //console.log('CFTreshold: ' + CFTreshold);

    adcClockDivider = shiftIt(adcClockDivider, 0);
    numofSample = shiftIt(numofSample, 3);
    numofRamps = shiftIt(numofRamps, 6);
    downsamplamount = shiftIt(downsamplamount, 9);
    FFTsize = shiftIt(FFTsize, 12);

    AverageN = shiftIt(AverageN, 15);
    CFGuard = shiftIt(CFGuard, 17);
    CFSize = shiftIt(CFSize, 19);
    CFTreshold = shiftIt(CFTreshold, 23);
	CFType = shiftIt(CFType, 27);
	DC = shiftIt(DC, 29);
	FIR = shiftIt(FIR, 30);
	WINDOW = shiftIt(WINDOW, 31);

    BBSetup = adcClockDivider + numofSample + numofRamps + downsamplamount + FFTsize + AverageN + CFGuard + CFSize + CFTreshold + CFType + DC + FIR + WINDOW;
    //console.log(BBSetup);
    BBSetup = BBSetup.toString(16);
    //console.log(BBSetup);
    BBSetup = '!B' + hexauffuellen(BBSetup.toUpperCase(), 8) + endstr;
    
        
    var oldconfigstr = $('#actConfig').html();    
    var configstr = updateLastConfig(oldconfigstr, "!B");   
    
    //console.log('BBSetup: ' + BBSetup);
    setTimeout(function () 
    {
        $('#actConfig').html(configstr + BBSetup);
        connection.send(BBSetup);    
    }, 100);

}


/**
 * Sends a version frame request !V\r\n.
 * @param {object} connection the connection object initialized by connect()
 * @returns {undefined}
 */
function getVersionFrame(connection)
{

    var endstr = "\r\n";
    versionCmd = '!V' + endstr;   
    //console.log('versionCmd: ' + versionCmd);
	
    setTimeout(function () 
    {
        connection.send(versionCmd);    
    }, 100);
}


/**
 * converting a boolean to an Integer
 * @param {bool} val true or false
 * @returns {Number}
 */
function booltoInt(val)
{
    if (val === true)
        val = 1;
    if (val === false)
        val = 0;
    return val;
}

/**
 * converts an integer into a binary string
 * @param {Number} dec
 * @returns {Number}
 */
function dec2bin(dec){
    return (dec >>> 0).toString(2);
}

/**
 * make sure shift operations succeed in javascript because numbers in JS
 * are 32Bit-signed Integers so one Bit is missing when calculating with big numbers
 * @param {number} param the number which should be left-shifted
 * @param {number} shiftparam how often should be shifted
 * @returns {shiftIt.result}
 */
function shiftIt(param, shiftparam)
{
    //console.log(param + ' ' + shiftparam);

    var parambitstr = (param >>> 0).toString(2);
    //console.log(parambitstr);
    var result = param;
    if ((parambitstr.length + shiftparam) >= 31)
    {
        //per schleife multiplizieren
        for (i = 0; i <= shiftparam - 1; i++) {
            result *= 2;
        }
        return result;
    } else
    {
        //linkshiften
        result = param << shiftparam;
        return result;
    }

}

/**
 * fills the hexnumber at the beginning with zeros to the specified amount of digits
 * @param {string} hexzahl an hexadezimal number as string
 * @param {int} stellen how much digits the hexnumber should have
 * @returns {String}
 */
function hexauffuellen(hexzahl, stellen)
{
    var zerostr = "";
    var laenge = hexzahl.length;
    var diff = stellen - laenge;
    for (i = 0; i < diff; i++)
    {
        zerostr += '0';
    }

    var neuehex = zerostr + hexzahl;
    return neuehex;
}
