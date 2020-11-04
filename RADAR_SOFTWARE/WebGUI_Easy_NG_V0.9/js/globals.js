
/**
 * @fileOverview file for all global variables
 
 */
/**
 * Which Browser is used (Chrome or Firefox recommended)
 * @type String
 */
var browser = ''
/**
 * @description the sceneobject where all other 3D-objects will be added to
 */
var scene1;
/**
 * 
 * @description defines if the scene is ready for drawing new things
 */
window.sceneready = true;
/**
 * @description the camera which will show the elements of the scene
 */
var camera1;
/**
 * @description the rendererobject which will draw all the object in the scene
 */
var renderer1;
/**
 * @description the controls-object which will be used by Orbitcontrols (actually deactivated)
 */
/**
 * 
 * @description the Frames per second, used in stats.js and to optimize the Rendering
 * if fps falls to low no new received data will be parsed
 */
var fps;
/**
 * 
 * @description the reference to the OrbitControls.js - Script from Three.js , 
 * actually not used
 */
var controls;
/**
 * @description counts the number of vertices in one RangeFrame-Chart
 */
var count = 0;
/**
 * @description counts the number of charts/lines added to the scene in 3D-RangeFrame-mode
 */
var linecount = 0;

/**
 * @description boolean, show the FFT or not
 */
var FFT = true;
/**
 * @description boolean, show the FFT or not
 */
var RAW = false;
/**
 * @description boolean, show the phasediagramm or not
 */
var phasediagramm = false;
/**
 * @description boolean, show spectrogramm or not
 */
var spectrogramm = false;
/**
 * @description the center coordinates of the SVG-Drawingarea
 */
var center = [];

/**
 * describes the how many mm is one BinNumber
 * @type Number
 */
var accuracy = 50;

/**
 * @description array with the coefficents to scale the incoming data with depending on the FFT-Size
 */
var Skalierungen = [2, 4, 8, 16, 32];
/**
 * @description global variable of the cameraposition, used to keep dat.GUI actual
 */
window.cameraposition = {CamPosX: 0, CamPosY: 0, CamPosZ: 250};
/**
 * @description global variable of the camerarotation, used to keep dat.GUI actual
 */
window.camerarotation = {CamRotX: 0, CamRotY: 0, CamRotZ: 0};

/**
 * 
 * @description the Size of the FFT (how many datapoints)
 */
window.FFTSize = 512;

/**
 * 
 * @description in which format the data will be returned to the client,
 * for example: 'mm' or 'cm'
 */
window.format = 5;


/**
 * @description global array of colors the different targets will be displayed in the scene
 */
var TargetColors =
        [
            '#ff000e', '#ffa100', '#fff100', '#cdff00',
            '#7dff00', '#2dff00', '#00ff53', '#00ff93',
            '#00ffe3', '#00cbff', '#007bff', '#001bff',
            '#7400ff', '#a400ff', '#e400ff', '#ff00de'
        ];
/**
 * 
 * @description Array when the spectrogramm and the phaseframe is activated
 * this Array is going to save the actual phaseangles
 */

/**
 * 
 * @description an Array which will keep the values of the phaseangles,
 * part 1 of the doublebuffer
 */
var PhaseArray0 = [];
/**
 * 
 * @description an Array which will keep the values of the phaseangles,
 * part 2 of the doublebuffer
 */
var PhaseArray1 = [];

/**
 * 
 * @description an Integer holding the value, which PhaseArray is actually used
 */
var usedPhaseArray = 0;

/**
 * 
 * @description an Array containing the Differences between one phaseframe and the next one
 */
var DeltaPhase = [];

/**
 * 
 * @description an Integer defining how far the objects will be displayed in the background
 * before they get deleted from the function fadeaway()
 */
var Sichtweite = 512;

/**
 * 
 * @description a Number defining the space between two datasets on the z-axis
 */
var Backsteps = 10;

/**
 * 
 * @description global object, in how much lines/parts are the X- and the Z-axis diveded
 */
window.LineCount = {LineCountX: 10, LineCountZ: 10};

/**
 * 
 * @description saves the Frames for the Logging 
*/
var LogTextArr = []

/**
 * 
 * @description boolean, if the TT-Diagramm is shown or not 
 */
window.TargetTimeLine = false;


/**
 * 
 * @description counter which gets incrementet for each targetlistframe in Target
 * -Time-Diagramm
 */
window.TTCounter = 0;

/**
 * 
 * @description Boolean describing if the frequency has already been scanned
 */
window.frequScanned = false;