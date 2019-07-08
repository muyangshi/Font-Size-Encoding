/*
 * Javascript for the landing page, 
 * on Next button click,
 * send the Tucker's ID number to the server
 * Muyang Shi, 25 June 2019
 *
 * 
 */

initialize();

function initialize() {
    var next = document.getElementById('next');
    if (next) {
        next.onclick = onNextClicked;
    }

}

function onNextClicked() {
    var turker_id = document.getElementById('turker_id').value; // How to proceed after validating the ID?
    alert(typeof turker_id);
    $.ajax({
        type: 'POST',
        url: '/word_cognition_study/turker_id',
        data: {'turker_id': turker_id,},
        success: function(response) {
            console.log(response);
            var input = $("<input>").attr("type","hidden").attr("name","turker_id").val(turker_id);
            $('#get_description_page').append(input).submit();
        },
        error: function(error) {
            alert('error saving data');
            console.log(error);
        }
    });
}