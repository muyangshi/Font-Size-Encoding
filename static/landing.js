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
    var next = document.getElementById('tucker_next');
    if (next) {
        next.onclick = onNextClicked;
    }

}

function onNextClicked() {
    var tucker_id = document.getElementById('tucker_id').value; // How to proceed after validating the ID?
    var ID = {
        'tucker_id': tucker_id,
    };
    // $.post("/word_cognition_study/tucker_id", ID);
    $.ajax({
        type: 'POST',
        url: '/word_cognition_study/tucker_id',
        data: ID,
        success: function(response) {
            console.log(response);
            var url = '/word_cognition_study/description/' + tucker_id 
            window.open(url,'_self',false)
        },
        error: function(error) {
            alert('error saving data');
            console.log(error);
        }
    });

    
}