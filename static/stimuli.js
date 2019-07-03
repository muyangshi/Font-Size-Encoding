/*
 * WordCloud.js
 * Muyang Shi, 25 June 2019
 *
 * 
 */

initialize();
function initialize() {
    var start = document.getElementById('Button_startStimuli')
    start.onclick = onStartButtonClicked;
}


var words;
var task_list = read_list; // to be passed from the server, which read a csv
alert(task_list);


function onStartButtonClicked() {
    var num = task_list[0]; //somthing to be read from an Array, that is from the CSV

    $.ajax({
        url: '/randomStim/'+ num,
        // data: data,
        success: 
            function(data){
                formed_data = data.map(function(word) {
                    return { 
                        text: word, 
                        weight: 10 + Math.random() * 90,
                        html: {"class": "CloudWord"},
                        handlers: { 
                            click: function() {postData($(this));} 
                        }
                    }
                });
            console.log(formed_data);
            words = formed_data;
            createCloud();
            },
        dataType: "json"
    });
}

function createCloud() {
    $("#JQWC").jQCloud(words);
}

function postData(theWord){
    var container = document.getElementById("JQWC");
    var containerSize = $(".jqcloud").css(['width','height']);
    var numberOfCloudWords = container.childElementCount;
    var theCloud = container.innerHTML;
    
    var wordPosition = theWord.css(["left","top"]);
        
    var word_data = {
        "turker_id": turker_id,
        "container size": containerSize,
        "word": theWord[0].innerHTML, //the word itself, but why $(this)[0]
        "word position": wordPosition,
        "number of Stim": numberOfCloudWords,
        "cloud": theCloud,
    };

    // $.post("/randomStim/post_data", word_data);

    $.ajax({
        type: 'POST',
        url: '/randomStim/post_data',
        data: word_data,
        success: function(response) {
            // alert('Response collected, please be ready for the next one');
            nextTask();
            console.log(response);
        },
        error: function(error) {
            alert('error saving data');
            console.log(error);
        }
    });
}

function nextTask(){
    document.getElementById('JQWC').innerHTML = "";
    task_list.shift();
    if (task_list.length == 0){
        alert('Im Done')
        var input = $("<input>").attr("name","turker_id").val(turker_id);
        $('#get_completion_page').append(input).submit();
    } else {
    onStartButtonClicked();
    }
}
