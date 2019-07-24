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
var distance_satisfied;
var already_placed_targets;
var targetslist;
var fixed_distance;
// console.log(tasklist,tasklist[0]);


function onStartButtonClicked() {
    // Reset the flag, and empty the word arrays
    distance_satisfied = true;
    fixed_distance = false;
    targetslist = [];
    already_placed_targets = [];

    // document.getElementById('Button_startStimuli').style.visibility = 'hidden';
    document.getElementById("Greeting").innerHTML = "";

    // Specifications about the targets, coming from the tasklist.
    var task = tasklist[0];
    var betw_targets_dist = task["betw_targets_dist"];
    var dist_to_center = task["radius"];

    var outer_radius = task["outer_radius"];
    var inner_radius = task["inner_radius"];
    var fixed_betw_dist = task["fixed_betw_dist"];


    // Specifications about the target words are loaded
    // from the csv to the tasklist
    // then from the tasklist to the getStim() method as params
    $.ajax({
        url: flask_util.url_for('getStim', {
            target_1_fontsize: task["target_1_fontsize"],
            target_1_length: task["target_1_length"],
            target_2_fontsize: task["target_2_fontsize"],
            target_2_length: task["target_2_length"]}),
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
                            html: {class: dictionary['html']},
                            handlers: {
                                mouseover: function() {this.style.cursor = "default";}
                            }
                        }
                    }
                });

                // push the target words into an array for later use
                words = formed_data;
                for (var i = 0; i < 2; i++){
                    targetslist.push(words.shift());
                }

                switch (betw_targets_dist){
                    case "random":
                        // words.sort(()=>Math.random() - 0.5);
                        break;
                    case "distant":
                        // words.sort(()=>Math.random() - 0.5);
                        distance_satisfied = false;
                        break;
                    case "fixed":
                        fixed_distance = true;
                        break;
                    default:
                        alert("Error reading tasklist");
                }

                // draw the targets first, then draw the distractors in the callback function
                drawTargetCloud(targetslist,outer_radius,inner_radius,fixed_betw_dist,drawDistractors);

            },
        dataType: "json"
    });
}

function drawTargetCloud(target_array,outer_radius,inner_radius,fixed_betw_dist,callback_drawDistractors) {
    $("#JQWC").addClass("jqcloud")
    drawTargets(target_array,outer_radius,inner_radius,fixed_betw_dist);

    callback_drawDistractors();
}

function drawTargets(target_array,outer_radius,inner_radius,fixed_betw_dist){
    if (fixed_distance === true) { 
    /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        // we have two target words, and we want to fix the distance between these two words
        var cloud_center_x = $("#JQWC").width() / 2.0;
        var cloud_center_y = $("#JQWC").height() / 2.0;

        target1 = target_array[0];
        var font_size = target1["weight"];
            var word_span = $('<span>').attr(target1.html).addClass("target");
            word_span.append(target1.text);
            $("#JQWC").append(word_span);
            var width = word_span.width();
            var height = word_span.height();
            var left;
            var top;
            do {
                left = cloud_center_x - width / 2.0 + Math.floor(Math.random() * (500)) + (-250);
                top = cloud_center_y - height / 2.0 + Math.floor(Math.random() * (500)) + (-250);
                distance_to_center = Math.sqrt(Math.pow((left-cloud_center_x),2) + Math.pow((top-cloud_center_y),2));
            } while (distance_to_center > outer_radius || distance_to_center < inner_radius)

            word_span[0].style.position = "absolute";
            word_span[0].style.left = left + "px";
            word_span[0].style.top = top + "px";
            word_span[0].style.fontSize = font_size + "px";
            word_span[0].style.color = "black";
            // console.log(target1_left);
            $(word_span).bind("click", function(){postData($(this));});
            $(word_span).bind("mouseover", function() {this.style.cursor = 'pointer';});

        already_placed_targets.push(word_span[0])
        
        target1_left = left;
        target1_top = top;            
        target2 = target_array[1];
        var font_size = target2["weight"];
            var word_span = $('<span>').attr(target2.html).addClass("target");
            word_span.append(target2.text);
            $("#JQWC").append(word_span);
            var width = word_span.width();
            var height = word_span.height();
            var left;
            var top;

            // console.log("target1_left: " + target1_left);
            // console.log("target_1_top: " + target1_top);
            do {
                var x = Math.random() * (fixed_betw_dist + fixed_betw_dist) - fixed_betw_dist;
                left = target1_left + x;
                top = target1_top + Math.sqrt(Math.pow(fixed_betw_dist,2)-Math.pow(x,2));
            } while (left > 1000 || top > 1000)
            // do {
            //     var x = Math.random() * (fixed_betw_dist + fixed_betw_dist) - fixed_betw_dist;
            //     // var x = Math.floor(Math.random() * Math.floor(fixed_betw_dist));
            //     left = target1_left + x;
            //     top = target1_top + Math.sqrt(Math.pow(fixed_betw_dist,2)-Math.pow(x,2));
            //     distance_to_center = Math.sqrt(Math.pow((left-cloud_center_x),2) + Math.pow((top-cloud_center_y),2));
            // } while (distance_to_center > outer_radius || distance_to_center < inner_radius)

            word_span[0].style.position = "absolute";
            word_span[0].style.left = left + "px";
            word_span[0].style.top = top + "px";
            word_span[0].style.fontSize = font_size + "px";
            word_span[0].style.color = "black";

            $(word_span).bind("click", function(){postData($(this));});
            $(word_span).bind("mouseover", function() {this.style.cursor = 'pointer';});

            already_placed_targets.push(word_span[0])
    }
    else {
        /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        // we dont care that much about the exact distance between the two target words,
        // as long as they are all within the same ring, also on the opposite side of the ring.
        target_array.forEach((target,index)=>{
            // console.log(target);
            // console.log(index);
            var font_size = target["weight"];
            var word_span = $('<span>').attr(target.html).addClass("target");
            word_span.append(target.text);
            $("#JQWC").append(word_span);
            var width = word_span.width();
            var height = word_span.height();
            var cloud_center_x = $("#JQWC").width() / 2.0;
            var cloud_center_y = $("#JQWC").height() / 2.0;
            var left;
            var top;
            do {
                left = cloud_center_x - width / 2.0 + Math.floor(Math.random() * (500)) + (-250);
                top = cloud_center_y - height / 2.0 + Math.floor(Math.random() * (500)) + (-250);
                distance_to_center = Math.sqrt(Math.pow((left-cloud_center_x),2) + Math.pow((top-cloud_center_y),2));
                // console.log("left: " + left);
                // console.log("top: " + top);
                // console.log("outer_radius: " + outer_radius);
                // console.log("inner_radius: " + inner_radius);
                // console.log("distance_to_center: " + distance_to_center);
                // console.log(distance_to_center > outer_radius);
                // console.log(distance_to_center < inner_radius);
            } while (distance_to_center > outer_radius || distance_to_center < inner_radius)

            console.log(word_span[0].innerHTML + Math.sqrt(Math.pow(left-cloud_center_x,2) + Math.pow(top - cloud_center_y,2)));

            word_span[0].style.position = "absolute";
            word_span[0].style.left = left + "px";
            word_span[0].style.top = top + "px";
            word_span[0].style.fontSize = font_size + "px";
            word_span[0].style.color = "black";

            $(word_span).bind("click", function(){postData($(this));});
            $(word_span).bind("mouseover", function() {this.style.cursor = 'pointer';});

            already_placed_targets.push(word_span[0])
        });

        var targets_left = []
        var targets_top = []
        $('.target').each(function(){targets_left.push(parseInt($(this).css('left'),10));});
        $('.target').each(function(){targets_top.push(parseInt($(this).css('top'),10));});
        var targets_x_distiance = Math.abs(targets_left[0] - targets_left[1]);
        var targets_y_distance = Math.abs(targets_top[0] - targets_top[1]);
        var targets_distance = Math.sqrt(Math.pow(targets_x_distiance,2)+Math.pow(targets_y_distance,2))
        console.log("distance between the two target is: " + targets_distance);

        // This is based on randomization,
        // making sure the distance between the two target words
        // is at least 2 times the inner radius
        while (distance_satisfied === false){
            if (targets_distance < inner_radius*2) {
                document.getElementById('JQWC').innerHTML = "";
                already_placed_targets = [];
                // console.log(targetslist);
                // console.log('dist_to_center: '+dist_to_center);
                drawTargets(targetslist,outer_radius,inner_radius,fixed_betw_dist);
            }
            else{
                distance_satisfied = true;
            }
        }
    }
}

function drawDistractors(){
    $("#JQWC").jQCloud(words,already_placed_targets,"distractor",
        {   delayedMode: false,
            afterCloudRender: () => {

                // Creating a red dot at the center of the WordCloud
                var dot_span = $('<span>').addClass("dot");
                $("#JQWC").append(dot_span);
                $(".dot")[0].style.position = "relative";
                $(".dot")[0].style.top = "50%";
                // $(".dot")[0].style.left = "50%";
                $(".dot")[0].style.height = "5px";
                $(".dot")[0].style.width = "5px";
                $(".dot")[0].style.backgroundColor = "red";
                $(".dot")[0].style.borderRadius = "35%";
                $(".dot")[0].style.display = "inline-block";
            }
        }
    );
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
// function drawTargetCloud(word_array,already_placed_targets,dist_to_center) {
//     // console.log("drawTargetCloud() is called")
//     $("#JQWC").jQCloud(word_array,already_placed_targets,"target",dist_to_center,
//         {   delayMode: false,
//             afterCloudRender: () => {
//                 // console.log("afterCloudRender is called")
//                 for (let i = 0; i < 2; i++) {
//                     $(".target")[i].style.color = 'black';
//                 }
//                 //measure the distance between the two target words
//                 var targets_left = []
//                 var targets_top = []
//                 $('.target').each(function(){targets_left.push(parseInt($(this).css('left'),10));});
//                 $('.target').each(function(){targets_top.push(parseInt($(this).css('top'),10));});
//                 var targets_x_distiance = Math.abs(targets_left[0] - targets_left[1]);
//                 var targets_y_distance = Math.abs(targets_top[0] - targets_top[1]);

//                 var targets_distance = Math.sqrt(Math.pow(targets_x_distiance,2)+Math.pow(targets_y_distance,2))
//                 console.log("distance between the two target is: " + targets_distance);

//                 // if (distance_satisfied === false){
//                 //     do{
//                 //         if (targets_distance < 300){
//                 //             console.log("distance is smaller than wanted")
//                 //             // targetslist still contain the two targets
//                 //             // we need to clean the "canvas"
//                 //             // we need to clean the already_placed_targets;

//                 //             document.getElementById('JQWC').innerHTML = "";
//                 //             already_placed_targets = [];

//                 //             targetslist.sort(()=>Math.random()-0.5);
//                 //             // console.log(targetslist);
//                 //             // console.log('dist_to_center: '+dist_to_center);

//                 //             drawTargetCloud(targetslist,already_placed_targets,dist_to_center);
//                 //         }
//                 //         else {
//                 //             // console.log("else")
//                 //             distance_satisfied = true;
//                 //         }
//                 //     } while (distance_satisfied === false)   
//                 // }

//                 // while (distance_satisfied === false){
//                 //     if (targets_distance < 300){
//                 //         document.getElementById('JQWC').innerHTML = "";
//                 //         already_placed_targets = [];
//                 //         console.log(targetslist);
//                 //         console.log('dist_to_center: '+dist_to_center);
//                 //         drawTargetCloud(targetslist,already_placed_targets,dist_to_center);

//                 //     }
//                 //     else {
//                 //         distance_satisfied = true;
//                 //     }

//                 // }

//                 // for (let i = 0; i < $("#JQWC")[0].childElementCount; i++){
//                 //     already_placed_targets.push($("#JQWC")[0].children[i]);
//                 // }
//                 console.log(already_placed_targets);
//                 drawNextCloud();
//             }
//         }
//     );
// }


// function drawNextCloud(){
//     targetslist.shift();
//     targetslist.shift();
//     if (targetslist.length == 0){
//         console.log('Targets have been placed')
//         drawDistractorCloud(words,already_placed_targets);
//     }
//     else{
//         drawTargetCloud(targetslist,already_placed_targets);
//     }
// }

// function drawDistractorCloud(word_array,already_placed_targets) {
//     $("#JQWC").jQCloud(word_array,already_placed_targets,"distractor");
// }








// function createCloud(word_array) {
//     $("#JQWC").jQCloud(word_array,
//         {   delayedMode: false,
//             afterCloudRender: () => {
//                 for (let i = 0; i < $(".target").length; i++) {
//                     $(".target")[i].style.color = 'black';
//                 }
                
//                 //measure the distance between the two target words
//                 var targets_left = []
//                 var targets_top = []
//                 $('.target').each(function(){targets_left.push(parseInt($(this).css('left'),10));});
//                 $('.target').each(function(){targets_top.push(parseInt($(this).css('top'),10));});
//                 var targets_x_distiance = Math.abs(targets_left[0] - targets_left[1]);
//                 var targets_y_distance = Math.abs(targets_top[0] - targets_top[1]);

//                 var targets_distance = Math.sqrt(Math.pow(targets_x_distiance,2)+Math.pow(targets_y_distance,2))
//                 console.log(targets_distance)
//                 if (distance_satisfied = false){
//                     do{
//                         if (targets_distance < 400){
//                             document.getElementById('JQWC').innerHTML = "";
//                             // console.log($('.target'));
//                             words.sort(()=>Math.random()-0.5)
//                             createCloud(words);
//                             // onStartButtonClicked();
//                         }
//                         else {
//                             distance_satisfied = true;
//                         }
//                     } while (distance_satisfied = false)   
//                 }
                
//             }
//         }
//     );
// }