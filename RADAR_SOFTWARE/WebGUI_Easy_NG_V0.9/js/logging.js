
/**
 * writes one Frame to the LocalStorage
 * @param {string} Frame the Frame received from the Server
 * @returns {undefined}
 */
function writetoLocalStorage(Frame)
{
    if (browser !== 'firefox')
    {
            if (localStorage.getItem('radarlog') !== 'undefined' && localStorage.getItem('radarlog') !== null )
        {
            if (localStorage.getItem('radarlog').length < 1000000)
            {   
                localStorage.radarlog = localStorage.radarlog + Frame;
                //localStorage.radarlog = localStorage.radarlog + $('#Seperator').val() + Frame;
            }
        }
        else
        {
            localStorage.setItem('radarlog', Frame);
        }
    }
    
    
    
    // Timestap -- Key
//    var timestamp = Date.now()
//    console.log(localStorage.length)
//    
//    if (localStorage.length < 1000)
//    {
//        localStorage.setItem('Radarlog' + timestamp.toString(), Frame);
//    }
//    else
//    {
//        localStorage.clear()
//    }
    
}

/**
 * shows the Log: opens a new Window and shows 
 * everything what is safed in the localStorage in the key "radarlog" 
 * @returns {undefined}
 */
function showLog()
{
    if (browser !== 'firefox')
    {
        var radarlog = localStorage.radarlog;
        var myWindow = window.open("", "Logdata", "toolbar=yes, scrollbars=yes, resizable=yes, top=500, left=500, width=600, height=600");
        myWindow.document.write("<p>" + radarlog + "</p>");
    }
    
    
    
//    var radarlog = "";
//    for(var i in localStorage)
//    {
//        var k = localStorage.key(i);
//        if (k.startsWith('Radarlog'))
//        {
//            radarlog += localStorage[i];
//        }
//
//    }
//    var myWindow = window.open("", "Logdata")
    
}

/**
 * clears the LocalStorage and deletes the key "radarlog"
 * @returns {undefined}
 */
function clearLog()
{
    if (browser !== 'firefox')
    {
        for(var i in localStorage)
        {
            var k = localStorage.key(i);
            if (k.startsWith('radarlog'))
            {
                localStorage.removeItem(k);
            }
        }
    }
    
}
