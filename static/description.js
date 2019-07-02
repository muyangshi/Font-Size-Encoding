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
    // alert(turker_id)
}


function onNextClicked() {
    var input = $("<input>").attr("name","turker_id").val(turker_id);
    $('#get_stimuli_page').append(input).submit();
}