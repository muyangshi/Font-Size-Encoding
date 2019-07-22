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
console.log("device pixel ratio is: " + window.devicePixelRatio);

do {
    if (window.devicePixelRatio != 1) {
    alert('Please adjust zoom to 100%', 'current: ',window.devicePixelRatio);
    }
    // window.devicePixelRatio = 1;
} while (window.devicePixelRatio != 1)


// if (window.devicePixelRatio != 1){
//     alert('Please adjust the zoom of your webpage to be 100%',window.devicePixelRatio)
//     console.log('Your zoom is', window.devicePixelRatio)
// }


var words;
var distance_satisfied = true;
console.log(tasklist,tasklist[0]);
// console.log(read_list);
// var task_list = read_list; // to be passed from the server, which read a csv
// console.log(task_list);


function onStartButtonClicked() {
    document.getElementById('Button_startStimuli').style.visibility = 'hidden';
    var task = tasklist[0]; //somthing to be read from an Array, that is from the CSV
    // var target_1_fontsize = this_task["target_1_fontsize"];

    var betw_targets_dist = task["betw_targets_dist"];
    // console.log(betw_targets_dist);

    var this_task = {
        "target_1_fontsize": task["target_1_fontsize"],
        "target_1_length": task["target_1_length"],
        "target_2_fontsize": task["target_2_fontsize"],
        "target_2_length": task["target_2_length"],
    };
    // console.log(this_task)

    
    $.ajax({
        url: flask_util.url_for('getStim', {
            target_1_fontsize: task["target_1_fontsize"],
            target_1_length: task["target_1_length"],
            target_2_fontsize: task["target_2_fontsize"],
            target_2_length: task["target_2_length"]}),
        // data: data,
        success:
            function(data){
                // console.log(data);
                formed_data = data.map(function(dictionary) {
                    if (dictionary["html"] === "target"){
                        return { 
                            text: dictionary['text'], 
                            weight: dictionary['fontsize'],
                            html: {class: dictionary['html']},
                            handlers: { 
                                click: function() {postData($(this));},
                                mouseover: function() {this.style.cursor = 'pointer';} 
                            }
                        }
                    }
                    else {
                        return { 
                            text: dictionary['text'], 
                            weight: dictionary['fontsize'],
                            html: {class: dictionary['html']}
                        }
                    }
                });
            words = formed_data;
            switch (betw_targets_dist){
                case "random":
                    words.sort(()=>Math.random() - 0.5);
                    break;
                case "random400":
                    words.sort(()=>Math.random() - 0.5);
                    distance_satisfied = false;
                    break;
                case "center": 
                    // seemingly the distance between the two target words
                    // is within 40px
                    // Both target words are fixated at the center of cloud
                    var targets = [words.shift(),words.shift()]
                    targets.sort(()=>Math.random() - 0.5)
                    words.sort(()=>Math.random() - 0.5)
                    words.unshift(targets[0])
                    words.unshift(targets[1])
                    break;
                case "far":
                    // seemingly the distance between the two target words
                    // is beyond 100px
                    // One target word is fixated at the center of cloud
                    // the other one is at the boarder of the wordcloud
                    var targets = [words.shift(),words.shift()]
                    targets.sort(()=>Math.random() - 0.5)
                    words.sort(()=>Math.random() - 0.5)
                    words.unshift(targets[0])
                    words.push(targets[1])
                    break;
                default:
                    alert("Error")
            }
            createCloud(words);
            },
        dataType: "json"
    });
}

function createCloud(word_array) {
    $("#JQWC").jQCloud(word_array,
        {   delayedMode: false,
            afterCloudRender: () => {
                for (let i = 0; i < $(".target").length; i++) {
                    $(".target")[i].style.color = 'black';
                }
                
                //measure the distance between the two target words
                var targets_left = []
                var targets_top = []
                $('.target').each(function(){targets_left.push(parseInt($(this).css('left'),10));});
                $('.target').each(function(){targets_top.push(parseInt($(this).css('top'),10));});
                var targets_x_distiance = Math.abs(targets_left[0] - targets_left[1]);
                var targets_y_distance = Math.abs(targets_top[0] - targets_top[1]);

                var targets_distance = Math.sqrt(Math.pow(targets_x_distiance,2)+Math.pow(targets_y_distance,2))
                console.log(targets_distance)
                if (distance_satisfied = false){
                    do{
                        if (targets_distance < 400){
                            document.getElementById('JQWC').innerHTML = "";
                            // console.log($('.target'));
                            words.sort(()=>Math.random()-0.5)
                            createCloud(words);
                            // onStartButtonClicked();
                        }
                        else {
                            distance_satisfied = true;
                        }
                    } while (distance_satisfied = false)   
                }
                
            }
        }
    );
}


function postData(clickedWord){
    var container = document.getElementById("JQWC");
    var containerSize = $(".jqcloud").css(['width','height']);
    var numberOfCloudWords = container.childElementCount;
    var theCloud = container.innerHTML; //the span content
    var clickedWordPosition = clickedWord.css(["left","top"]);

    var targets_left = []
    var targets_top = []
    $('.target').each(function(){targets_left.push(parseInt($(this).css('left'),10));});
    $('.target').each(function(){targets_top.push(parseInt($(this).css('top'),10));});

    var targets_x_distiance = Math.abs(targets_left[0] - targets_left[1]);
    var targets_y_distance = Math.abs(targets_top[0] - targets_top[1]);

    // var middle_x_pos = Math.abs(targets_left[0] + targets_left[1])/2;
    // var middle_y_pos = Math.abs(targets_top[0] + targets_top[1])/2;

    var targets_distance = Math.sqrt(Math.pow(targets_x_distiance,2)+Math.pow(targets_y_distance,2));
    // var mid_to_center = Math.sqrt()

    var targets_word = [];
    $('.target').each(function(){targets_word.push($(this));});
    var correct_word = (parseInt(targets_word[0].css('font-size')) > parseInt(targets_word[1].css('font-size'))) ? targets_word[0]:targets_word[1];
    var wrong_word = targets_word.filter(function(value,index,arr){return value != correct_word;})[0];
    // alert("correct word:" + correct_word[0].innerHTML + "wrong word:" + wrong_word[0].innerHTML);

    correct_word_position = correct_word.css(["left","top"]);
    wrong_word_position = wrong_word.css(["left","top"]);


    var word_data = {
        "turker_id": turker_id,
        "container size": containerSize,
        "clickedword": clickedWord[0].innerHTML,
        "clicked position": clickedWordPosition,
        "betw targets distance": targets_distance,
        "correct word": correct_word[0].innerHTML,
        "correct word position": correct_word_position,
        "wrong word": wrong_word[0].innerHTML,
        "wrong word position": wrong_word_position,
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
            // console.log(response);
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
