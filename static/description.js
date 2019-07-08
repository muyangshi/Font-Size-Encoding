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
}


function onNextClicked() {
    var input = $("<input>").attr("type","hidden").attr("name","turker_id").val(turker_id);
    $('#get_stimuli_page').append(input).submit();
}