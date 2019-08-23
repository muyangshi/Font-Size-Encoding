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
    $(document).keypress(function(e){
        if (e.which == 13){
            $("#next").click();
        }
    });

}

function onNextClicked() {
    var turker_id = document.getElementById('turker_id').value; // How to proceed after validating the ID?
    $.ajax({
        type: 'POST',
        url: turker_id_url,
        data: {'turker_id': turker_id,},
        success: function(response) {
            console.log(response);
            // var experiment;
            
            var input = $("<input>").attr("type","hidden").attr("name","turker_id").val(turker_id);
            // $('#get_description_page').append(experiment);
            $('#get_description_page').append(input).submit();
        },
        error: function(error) {
            alert('error saving turker id');
            console.log(error);
        }
    });
}