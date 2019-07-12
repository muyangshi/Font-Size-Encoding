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
alert(window.devicePixelRatio);

do {
    alert('Please adjust zoom to 100%', 'current: ',window.devicePixelRatio)
} while (window.devicePixelRatio != 1)


// if (window.devicePixelRatio != 1){
//     alert('Please adjust the zoom of your webpage to be 100%',window.devicePixelRatio)
//     console.log('Your zoom is', window.devicePixelRatio)
// }


var words;
console.log(tasklist,tasklist[0]);
// console.log(read_list);
// var task_list = read_list; // to be passed from the server, which read a csv
// console.log(task_list);


function onStartButtonClicked() {
    var task = tasklist[0]; //somthing to be read from an Array, that is from the CSV
    // var target_1_fontsize = this_task["target_1_fontsize"];

    var this_task = {
        "target_1_fontsize": task["target_1_fontsize"],
        "target_1_length": task["target_1_length"],
        "target_2_fontsize": task["target_2_fontsize"],
        "target_2_length": task["target_2_length"],
    };
    console.log(this_task)

    
    $.ajax({
        url: flask_util.url_for('getStim', {
            target_1_fontsize: task["target_1_fontsize"],
            target_1_length: task["target_1_length"],
            target_2_fontsize: task["target_2_fontsize"],
            target_2_length: task["target_2_length"]}),
        // data: data,
        success:
            function(data){
                console.log(data);
                formed_data = data.map(function(dictionary) {
                    return { 
                        text: dictionary['text'], 
                        weight: dictionary['fontsize'],
                        html: {class: dictionary['html']},
                        handlers: { 
                            click: function() {postData($(this));},
                            mouseover: function() {this.style.cursor = 'pointer';} 
                        }
                    }
                });
            // console.log(formed_data);
            words = formed_data;
            createCloud();
            },
        dataType: "json"
    });
}

function createCloud() {
    $("#JQWC").jQCloud(words,
        {delayedMode: false,
            afterCloudRender: () => {
                for (let i = 0; i < $(".target").length; i++) {
                    $(".target")[i].style.color = 'black';
                }
            }
        }
    );
}


function postData(clickedWord){
    var container = document.getElementById("JQWC");
    var containerSize = $(".jqcloud").css(['width','height']);
    var numberOfCloudWords = container.childElementCount;
    var theCloud = container.innerHTML;
    
    var clickedWordPosition = clickedWord.css(["left","top"]);

    var targets_left = []
    var targets_top = []
    $('.target').each(function(){targets_left.push(parseInt($(this).css('left'),10));});
    $('.target').each(function(){targets_top.push(parseInt($(this).css('left'),10));});
    var targets_x_distiance = Math.abs(targets_left[0] - targets_left[1]);
    var targets_y_distance = Math.abs(targets_top[0] - targets_top[1]);

    var targets_distance = Math.sqrt(Math.pow(targets_x_distiance,2)+Math.pow(targets_y_distance,2))

    var targets_word = []
    $('.target').each(function(){targets_word.push($(this));})
    var correct_word = (parseInt(targets_word[0].css('font-size')) > parseInt(targets_word[1].css('font-size'))) ? targets_word[0]:targets_word[1]

    var word_data = {
        "turker_id": turker_id,
        "container size": containerSize,
        "word": clickedWord[0].innerHTML,
        "word position": clickedWordPosition,
        "targets distance": targets_distance,
        "correct word": correct_word[0].innerHTML,
        "number of Stim": numberOfCloudWords,
        "cloud": theCloud,
    };

    // $.post("/randomStim/post_data", word_data);

    $.ajax({
        type: 'POST',
        url: post_data_url,
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
    tasklist.shift();
    if (tasklist.length == 0){
        console.log('All tasks completed')
        var input = $("<input>").attr("type","hidden").attr("name","turker_id").val(turker_id);
        $('#get_completion_page').append(input).submit();
    } else {
    onStartButtonClicked();
    }
}
