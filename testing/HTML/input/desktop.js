/**
 * The index of the current Mission (1º mission => 0).
 */
var currentMissionIndex;

/**
 * Key: number of players in the game.
 * 
 * Index: number of the mission.
 * 
 * Value: number of players needed for that mission.
 */
var playersPerM = {
    5: [ 2, 3, 2, 3, 3 ],
    6: [ 2, 3, 4, 3, 4 ],
    7: [ 2, 3, 3, 4, 4 ],
    8: [ 3, 4, 4, 5, 5 ],
    9: [ 3, 4, 4, 5, 5 ],
    10:[ 3, 4, 4, 5, 5 ]
}

// GetDB functions

/**
 * Function to execute when data from getDB is received from server.
 * @param {Obj} data - Object from server.
 */
var successGetDBf = (data) => {
    updatePlayers();
    updateMissions();
    updateSelectedPlayers();
    updatePoll();
};

/**
 * Function to execute when error getting data from getDB.
 * @param {Obj} data - Object from server.
 */
var errorGetDBf = (e) => {
    updatePlayers(debugPlayers);
    updateMissions(debugMissions);
    updateSelectedPlayers([])
    updatePoll(debugOpinion);
};

window.onload = function() {
    // Create poll btns events    
    $("#LeftBtn").click(()=>{vote(1);});
    $("#RightBtn").click(()=>{vote(-1);});

    $(".torch").attr("src", "../../Res/img/torch.png");
    $(".gun").attr("src", "../../Res/img/guns/007-gun.png");
    $(".playerIcon").attr("src", "../../Res/img/users/user13.png");
    // update();

    //Update periodically the following functions

    // setInterval(update, 500);

    // asyncInterval(goToNextState, "t", 500);
}

/**
 * Executes the function to get the content of the DB using the functions:
 * @see successGetDBf
 * @see errorGetDBf
 */
function update() {
    getDB(successGetDBf, errorGetDBf);
}