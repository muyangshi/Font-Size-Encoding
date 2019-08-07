/*
 * Javascript for the description page, 
 * on Next button click,
 * read a csv for recursive stimulus
 * Muyang Shi, 25 June 2019
 *
 * 
 */

initialize();

function initialize() {
    var next = document.getElementById('start_stim');
    if (next) {
        next.onclick = onNextClicked;
    }
    console.log(turker_id);
    if (participant === "tested"){
        $("body").html("Hello "+turker_id+", you have already participated in this research. \n If this is your first time participating in this research, please contant us at xxx@carleton.edu. \n Thank you for your understanding.")
    }
}


function onNextClicked() {
    var input = $("<input>").attr("type","hidden").attr("name","turker_id").val(turker_id);
    $('#get_stimuli_page').append(input).submit();
}