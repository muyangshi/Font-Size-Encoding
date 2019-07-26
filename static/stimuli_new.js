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

// while (window.devicePixelRatio != 1) {
//     alert('Please adjust zoom to 100%. ' + 'Current: ' + window.devicePixelRatio);
// }

var words;
var already_placed_targets;
var targetslist;
var in_same_ring;

function onStartButtonClicked() {
    document.getElementById("Greeting").innerHTML = "";

    // Reset the flag
    // empty the word arrays
    targetslist = [];
    already_placed_targets = [];
    in_same_ring = false;
    

    // Specifications about the targets, coming from the tasklist.
    var task = tasklist[0];

    var outer_radius = task["outer_radius"];
    var inner_radius = task["inner_radius"];
    var distance_between = task["distance_between"];
    var rule = task["rule"];
    // var fixed_betw_dist = task["fixed_betw_dist"];


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

                // draw the targets first, then draw the distractors in the callback function
                drawTargetCloud(rule,targetslist,outer_radius,inner_radius,distance_between,drawDistractorsCallback);

            },
        dataType: "json"
    });
}

function drawTargetCloud(rule,target_array,outer_radius,inner_radius,distance_between,callback_drawDistractors) {
    $("#JQWC").addClass("jqcloud");
    drawTargets(rule,target_array,outer_radius,inner_radius,distance_between);

    callback_drawDistractors();
}

function drawTargets(rule,target_array,outer_radius,inner_radius,distance_between){
    var cloud_center_x = $("#JQWC").width() / 2.0;
    var cloud_center_y = $("#JQWC").height() / 2.0;

    switch (rule){
        case "in_ring":///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        // Currectly, this is accountable for two target words
        // The two target words will be placed inside a ring of inner_radius to outer_radius
        // The distance between the two target words will be at least 2*inner_radius
            
            // forEach target in the targetslist
            // randomize its position within the ring
            // and set the css styles and click function
            target_array.forEach((target,index)=>{
                var font_size = target["weight"];
                var word_span = $('<span>').attr(target.html).addClass("target"+index);
                word_span.append(target.text);
                $("#JQWC").append(word_span);
                var width = word_span.width();
                var height = word_span.height();
                var left;
                var top;

                // Making the position of this target
                // to be in the ring
                // ineer_radius < dist_to_center < outer_radius
                do {
                    left = cloud_center_x - width / 2.0 + Math.floor(Math.random() * (500)) + (-250);
                    top = cloud_center_y - height / 2.0 + Math.floor(Math.random() * (500)) + (-250);
                    distance_to_center = Math.sqrt(Math.pow((left + width/2.0 - cloud_center_x),2) + Math.pow((top + height/2.0 - cloud_center_y),2));
                } while (distance_to_center > outer_radius || distance_to_center < inner_radius)
    
                console.log(word_span[0].innerHTML + distance_to_center);
    
                word_span[0].style.position = "absolute";
                word_span[0].style.left = left + "px";
                word_span[0].style.top = top + "px";
                word_span[0].style.fontSize = font_size + "px";
                word_span[0].style.color = "black";    
                $(word_span).bind("click", function(){postData($(this));});
                $(word_span).bind("mouseover", function() {this.style.cursor = 'pointer';});
    
                already_placed_targets.push(word_span[0])
            });

            // Calculate the distance between the two target words' center
            var target_0 = $(".target0");
            var target_1 = $(".target1");
            var targets_x_distance = Math.abs((target_0.width() / 2.0 + parseInt(target_0[0].style.left)) - (target_1.width() / 2.0 + parseInt(target_1[0].style.left)));
            var targets_y_distance = Math.abs((target_0.height() / 2.0 + parseInt(target_0[0].style.top)) - (target_1.height() / 2.0 + parseInt(target_1[0].style.top)));
            var targets_distance = Math.sqrt(Math.pow(targets_x_distance,2) + Math.pow(targets_y_distance,2));
            console.log("distance between the two target is: " + targets_distance);

            // This is based on randomization,
            // making sure the distance between the two target words
            // is at least 2 times the inner radius
            while (in_same_ring === false){
                if (targets_distance < inner_radius*2) {
                    document.getElementById('JQWC').innerHTML = '<span class="dot" style="position: absolute;top: 500px;left: 500px;height: 5px;width: 5px;background-color: red;border-radius: 35%;display: inline-block;"></span>';
                    already_placed_targets = [];
                    // console.log(targetslist);
                    // console.log('dist_to_center: '+dist_to_center);
                    drawTargets(rule,targetslist,outer_radius,inner_radius,distance_between);
                }
                else{
                    in_same_ring = true;
                }
            }
            break;
        case "on_circle":///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            // we have two target wrods, and we want to fix them onto a circle
            // that has the diameter of distance_between
            target0 = target_array[0];
            var font_size = target0["weight"];
                var word_span = $('<span>').attr(target0.html).addClass("target0");
                word_span.append(target0.text);
                $("#JQWC").append(word_span);
                var width = word_span.width();
                var height = word_span.height();
                var left;
                var top;
                var radius = distance_between / 2.0
                var x = Math.random()*(radius*2)-radius;
                var y = Math.sqrt(Math.pow(radius,2) - Math.pow(x,2)); // and here y will always be positive
                var coefficient = [-1,1];
                    y = y*coefficient[Math.floor(Math.random()*coefficient.length)];
                
                // console.log("x: "+x+" y: " + y);
                
                left = cloud_center_x - width / 2.0 - x;
                top = cloud_center_y - height / 2.0 - y;
                distance_to_center = Math.sqrt(Math.pow((left + width/2.0 - cloud_center_x),2) + Math.pow((top + height/2.0 - cloud_center_y),2));
                console.log("target0: " + distance_to_center);

                word_span[0].style.position = "absolute";
                word_span[0].style.left = left + "px";
                word_span[0].style.top = top + "px";
                word_span[0].style.fontSize = font_size + "px";
                word_span[0].style.color = "black";

                $(word_span).bind("click", function(){postData($(this));});
                $(word_span).bind("mouseover", function() {this.style.cursor = 'pointer';});

            already_placed_targets.push(word_span[0]);

            target1 = target_array[1];
            var font_size = target1["weight"];
                var word_span = $('<span>').attr(target1.html).addClass("target1");
                word_span.append(target1.text);
                $("#JQWC").append(word_span);
                var width = word_span.width();
                var height = word_span.height();
                var left;
                var top;

                // console.log("x: "+x+" y: " + y);

                // target1 is place along the diameter of the cirle
                // the circle that target0 relies on
                left = cloud_center_x - width / 2.0 + x; // x is the x distance randomized for target0
                top = cloud_center_y - height / 2.0 + y; // y is the y distance randomized for target0
                distance_to_center = Math.sqrt(Math.pow((left + width/2.0 - cloud_center_x),2) + Math.pow((top + height/2.0 - cloud_center_y),2));
                console.log("target1: " + distance_to_center);

                word_span[0].style.position = "absolute";
                word_span[0].style.left = left + "px";
                word_span[0].style.top = top + "px";
                word_span[0].style.fontSize = font_size + "px";
                word_span[0].style.color = "black";

                $(word_span).bind("click", function(){postData($(this));});
                $(word_span).bind("mouseover", function() {this.style.cursor = 'pointer';});

            already_placed_targets.push(word_span[0])

            var target_0 = $(".target0");
            var target_1 = $(".target1");
            var targets_x_distance = Math.abs((target_0.width() / 2.0 + parseInt(target_0[0].style.left)) - (target_1.width() / 2.0 + parseInt(target_1[0].style.left)));
            var targets_y_distance = Math.abs((target_0.height() / 2.0 + parseInt(target_0[0].style.top)) - (target_1.height() / 2.0 + parseInt(target_1[0].style.top)));
            var targets_distance = Math.sqrt(Math.pow(targets_x_distance,2) + Math.pow(targets_y_distance,2));
            console.log("distance between the two target is: " + targets_distance);
            break;
        default:
            alert("Cannot read rule");
    }
}

function drawDistractorsCallback(){
    $("#JQWC").jQCloud(words,already_placed_targets,"distractor",
        {   delayedMode: false,
        }
    );
}

function nextTask(){
    document.getElementById('JQWC').innerHTML = '<span class="dot" style="position: absolute;top: 500px;left: 500px;height: 5px;width: 5px;background-color: red;border-radius: 35%;display: inline-block;"></span>';
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
    var number_of_words = document.getElementById("JQWC").childElementCount - 1; // minus the dot span
    var span_content = document.getElementById("JQWC").innerHTML; //the span content
    
    var cloud_width = $("#JQWC").width(); // width of the container in int
    var cloud_height = $("#JQWC").height(); // height of the container in int
    
    var cloud_center_x = cloud_width / 2.0; // the center x in int
    var cloud_center_y = cloud_height / 2.0; // the center y in int

    var target_0 = $(".target0");
    var target_1 = $(".target1");
    var targets_x_distance = Math.abs((target_0.width() / 2.0 + parseInt(target_0[0].style.left)) - (target_1.width() / 2.0 + parseInt(target_1[0].style.left)));
    var targets_y_distance = Math.abs((target_0.height() / 2.0 + parseInt(target_0[0].style.top)) - (target_1.height() / 2.0 + parseInt(target_1[0].style.top)));
    var distance_between_targets = Math.sqrt(Math.pow(targets_x_distance,2) + Math.pow(targets_y_distance,2));

    var correct_word = target_0.css('font-size') > target_1.css('font-size') ? target_0:target_1;
    var wrong_word = target_0.css('font-size') < target_1.css('font-size') ? target_0:target_1;

    var correct_word_fontsize = parseInt(correct_word.css("font-size"));
    var wrong_word_fontsize = parseInt(wrong_wordcss("font-size"));

    var correct_word_width = correct_word.width();
    var correct_word_height = correct_word.height();
    var wrong_word_width = wrong_word.width();
    var wrong_word_height = wrong_word.height();
    
    // the x and y coordinate of the two target words
    // take the center of the cloud to be the origin
    // e.g. if the container is of size (1000,1000), then the origin is (500,500)
    // all the subsequent x and y coordinates are with respect to that origin
    var correct_word_x = parseInt(correct_word.css("left")) + correct_word_width/2.0 - cloud_center_x;
    var correct_word_y = cloud_center_y - parseInt(correct_word.css("top")) + correct_word_height/2.0;
    var wrong_word_x = parseInt(wrong_word.css("left")) + wrong_word_width/2.0 - cloud_center_x;
    var wrong_word_y = cloud_center_y - parseInt(wrong_word.css("top")) + wrong_word_height/2.0;

    var correct_word_center_distance = Math.sqrt(Math.pow(correct_word_x,2) + Math.pow(correct_word_y,2));
    var wrong_word_center_distance = Math.sqrt(Math.pow(wrong_word_x,2) + Math.pow(wrong_word_y,2));

    var word_data = {
        "turker_id": turker_id,

        "cloud_width": cloud_width,
        "cloud_height": cloud_height,
        "cloud_center_x": cloud_center_x,
        "cloud_center_y": cloud_center_y,

        "clicked_word": clickedWord[0].innerHTML,
        "correct_word": correct_word[0].innerHTML,
        "wrong_word": wrong_word[0].innerHTML,
        "distance_between_targets": distance_between_targets,

        "correct_word_x": correct_word_x,
        "correct_word_y": correct_word_y,
        "correct_word_fontsize": correct_word_fontsize,
        "correct_word_width": correct_word_width,
        "correct_word_height": correct_word_height,
        "correct_word_center_distance": correct_word_center_distance,

        "wrong_word_x": wrong_word_x,
        "wrong_word_y": wrong_word_y,
        "wrong_word_fontsize": wrong_word_fontsize,
        "wrong_word_width": wrong_word_width,
        "wrong_word_height": wrong_word_height,
        "wrong_word_center_distance": wrong_word_center_distance,
        
        "number_of_words": number_of_words,
        "span_content": span_content,
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
