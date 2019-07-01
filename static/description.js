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
    alert(turker_id)
}


function onNextClicked() {
    // var tucker_id = document.getElementById('tucker_id').value;
    // var ID = {
        // 'tucker_id': tucker_id,
    // };
    // $.post("/word_cognition_study/tucker_id", ID);
    // $.ajax({
    //     type: 'POST',
    //     url: '/word_cognition_study/tucker_id',
    //     data: ID,
    //     success: function(response) {
    //         console.log(response);
    //     },
    //     error: function(error) {
    //         alert('error saving data');
    //         console.log(error);
    //     }
    // });

    var url = '/word_cognition_study/' + turker_id + '/stimuli' 
    window.open(url,'_self',false)
}