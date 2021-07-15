/**
 * This variable keeps the known NodeRed database state.
 * @see Each time a new version of each piece is returned from server, this variable is updated.
 */
var DB = {
    players: null,
    playersPos: null,
    missions: null,
    opinion: null,
    missionTeam: null
};

/**
 * This variable stores the data entered using the url (url.com?data=1 => queryString = {data: 1})
 */
var queryString = new Array();


// WHEN FILE LOADED, EXECUTE THIS CODE
getQuerry(); // Get information from URL
resizeTextSize(); // Update the text size with the current screen
$(window).resize(resizeTextSize); // When screen size change, adjust text size


// ************ CSS ************

/**
 * Updates the CSS properties with the standar Text-Size.
 * This allows to have a consistent text display, scalling text-size with the height of the window.
 * @see this values are designed for mobile devices.
 */
function resizeTextSize() {
    let size = $("body").css("height"); // Height of the window in pixels
    size = Number.parseInt(size.substr(0, size.length - 2) / 50); // Is is the smallest text-size

    let textSize = [
        ["huge", 3.5],
        ["bigger", 3],
        ["big", 2.5],
        ["normal", 2],
        ["small", 1.5],
        ["detail", 1]
    ];
    for (let e of textSize) { // for each desired textSize-type
        $(":root").css(`--${e[0]}Text`, `${e[1] * size}px`); // Add it to the CSS :root
    }

    console.log("Screen resized");
}

/**
 * Updates the background acording to the current score of missions
 * @param {number} resistencia - Missions won by the resistance
 * @param {number} chunguitos - Missions won by the chunguitos
 */
 function changeBackground(resistencia, chunguitos) {
    if (typeof resistencia != "number" || typeof chunguitos != "number")  {
        throw new Error("The arguments must be numbers");
    }
    if (resistencia < 0 || chunguitos < 0)  {
        throw new Error("The arguments must be positive");
    }
    if (resistencia >= 3) {
        $("body").css("background", "var(--blue)");
    }
    else if (chunguitos >= 3) {
        $("body").css("background", "var(--red)");
    }
    else { // Normal
        const intensidad = {
            resistencia: [
                5,
                15,
                30
            ],
            chunguitos: [
                90,
                70,
                55
            ]
        };
        $("body").css("background", `linear-gradient(180deg, var(--blue) ${intensidad.resistencia[resistencia]}%, var(--red) ${intensidad.chunguitos[chunguitos]}%)`);
    }
}



// ************ Connectivity ************

/**
 * Get all the information addressed in the URL and store it on the queryString object.
 */
function getQuerry(){
    if (queryString.length == 0) {
        if (window.location.search.split('?').length > 1) { // If there're arguments to store
            // Get them
            var params = window.location.search.split('?')[1].split('&');
            for (let i = 0; i < params.length; i++) { // For each argument
                let d = params[i].split('='); // Split key-value

                queryString[d[0]] = decodeURIComponent(d[1]);
            }

            if (queryString.username && !queryString.pId) { // If username stored but pId missing
                console.warn("pId not selected");

                $.ajax({ // Get pId and store it
                    url: "getpId",
                    method: "get",
                    data:{
                        username: queryString.username
                    },
                    success: function(data) {
                        console.log("pId recovered: " + data);
                        queryString["pId"] = parseInt(data);
                    }
                });
            }
        }
    }
}

/**
 * Changes the current URL of the device, storing the desired data on it.
 * This prevents the user of asking for the information all the time or the need of cache.
 * @param {String} url - URL defined at NodeRed to go to.
 * @param {Obj} extraData - Object with the desired extra data we want to add.
 */
function go2page(url, extraData={}) {
    let extra = [];
    for (const v of Object.entries(queryString)) {
        extra.push(v.join("="))
    }
    for (const v of Object.entries(extraData)) {
        extra.push(v.join("="))
    }
    window.location.href = url + "?" + extra.join("&");
};

var lastTime = 0;
function getDB(successF, failF) {
    $.ajax({
        url: "getDB",
        method: "get",
        data: {
            lastTime: lastTime
        },
        success: (data) => {
            if (data.lastTime > lastTime) { // If the content is new
                lastTime = data.lastTime; // Do not update until DB change in the future

                // Store is DB
                DB.players = data.players; 
                DB.missions = data.missions;
                DB.missionTeam = data.missionTeam;
                DB.opinion = data.opinion;

                successF(data);
            }
        },
        error: (e) => {
            // store debug content
            DB.players = debugPlayers;
            DB.missions = debugMissions;
            DB.missionTeam = [];
            DB.opinion = [];

            failF(e);
        }
    });
};


// Asinc functions using promises
const sleep = async (ms) => {
    return new Promise(resolve => setTimeout(resolve, ms));
};

/**
 * Allows to execute $.ajax method periodically until the spected result is returned by the server or until the triesLeft are 0.
 * @param {Object} petition - JavaScript object with the argument of the $.ajax(XXXXXX) method.
 * @param {any} spected - Spected result of the petition.
 * @param {number} ms - Time to wait between petitions in milliseconds.
 * @param {number} triesLeft - Number of tries until the device stops making petitions.
 * @returns 
 */
const asyncInterval = async (petition, spected, ms, triesLeft = 10000) => {
    return new Promise((resolve, reject) => {
        const interval = setInterval(async () => {
            if (await $.ajax(petition) == spected) {
                resolve();
                clearInterval(interval);
            } 
            else if (triesLeft <= 1) {
                reject();
                clearInterval(interval);
            }
            triesLeft--;
        }, ms);
    });
};


// ************ Analyzers ************
/**
 * Checks whenever an element e is (phisically) inside of a element p
 * @param {object} e - Element to check if it is inside ({x: number, y: number, w: number, h: number})
 * @param {object} p - Parent ({x: number, y: number, w: number, h: number})
 * @param {boolean} conversion - (optional) if the input is a HTML element (true) or it is a object with the div2disposition function format
 * @returns {boolean} The result of the analysis
 */
function stillIn(e, p, conversion = true) {
    if (conversion){
        e = div2disposition(e);
        p = div2disposition(p);
    }
    // return !(e.x < 0 || e.y < 0 ||
    return !(e.x < p.x || e.y < p.y ||
        e.x + e.w > p.x + p.w || 
        e.y + e.h > p.y + p.h);
}

/**
 * Whenever the inputed string is a valid integer.
 * @param {String} str - String to compare.
 * @returns (boolean) Result.
 */
function isInt(str) {
    if (typeof str != "string") {
        return false; // we only process strings!  
    }
    return !isNaN(str) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
           !isNaN(parseInt(str)); // ...and ensure strings of whitespace fail
}

// ************ Conversors ************

function getBase64Image(img) {
    var canvas = document.createElement("canvas");
    canvas.width = img.width;
    canvas.height = img.height;
    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);
    var dataURL = canvas.toDataURL("image/png");
    return dataURL;
    // return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
}

/**
 * Transforms a px unit to a float.
 * @param {string} p string with the pixels in the regex-format "d+ px"
 */
function pixel2float(p){
    return parseFloat(p.substring(0, p.length - 2));
}


// ********* DEBUG ************

// debug
const debugPlayers = [
    {"pId":1,"name":"jorge","groupPos":1,"pType":0},
    {"pId":2,"name":"paula","groupPos":2,"pType":0},
    {"pId":3,"name":"ana","groupPos":3,"pType":1},
    {"pId":4,"name":"adri","groupPos":4,"pType":0},
    {"pId":5,"name":"laura","groupPos":5,"pType":1},
    {"pId":6,"name":"Juan","groupPos":6,"pType":0},
    {"pId":7,"name":"Pepa","groupPos":7,"pType":0},
    {"pId":8,"name":"Esmeralda","groupPos":8,"pType":0},
    {"pId":9,"name":"Luis","groupPos":9,"pType":0},
    {"pId":10,"name":"Paco","groupPos":10,"pType":0}
];

var debugMissions = [
    {
        mId: 1,
        active: false,
        leaderId: 3,
        vYes: 4,
        vNo: 1,
        mRes: 1
    },
    {
        mId: 2,
        active: false,
        leaderId: 4,
        vYes: 5,
        vNo: 2,
        mRes: 0
    },
    {
        mId: 3,
        active: true,
        leaderId: 5,
        vYes: null,
        vYes: null,
        mRes: 0
    },
    {
        mId: 4,
        active: false,
        leaderId: 6,
        vYes: null,
        vNo: null,
        mRes: 0
    },
    {
        mId: 5,
        active: false,
        leaderId: null,
        vYes: null,
        vNo: null,
        mRes: 0
    }
];

var debugOpinion = [
    {
        "pId":1,
        "val":1
    },
    {
        "pId":2,
        "val":1
    },
    {
        "pId":3,
        "val":1
    },
    {
        "pId":4,
        "val":1
    },
    {
        "pId":5,
        "val":1
    },
    {
        "pId":6,
        "val":1
    },
    {
        "pId":7,
        "val":1
    },
    {
        "pId":8,
        "val":1
    },
    {
        "pId":9,
        "val":1
    },
    {
        "pId":10,
        "val":1
    }
];