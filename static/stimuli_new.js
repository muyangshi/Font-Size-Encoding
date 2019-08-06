/*
 * WordCloud.js
 * Muyang Shi, 25 June 2019
 * Currently being used for the pilot study of comparing the fontsize
 * of TWO target words
 * 
 * as of 31 July, starting to implement for hypo2
 */

initialize();
function initialize() {
    var start = document.getElementById('Button_startStimuli')
    start.onclick = onStartButtonClicked;
}
console.log("device pixel ratio is: " + window.devicePixelRatio);

// var words; // distractors used for hypo1, should be able to put this inside onStartButtonClicked()
var already_placed_targets;

var distractors_hypo2; //used for hypo2
var targets_hypo2; // 2D array used for hypo2

function onStartButtonClicked() {
    document.getElementById("Greeting").innerHTML = ""; //Clear the page content

    // Reset the flag
    // empty the word arrays
    var targetslist = [];// targets used for hypo1
    already_placed_targets = [];
    // in_same_ring = false;
    

    // Specifications about the targets, coming from the tasklist.
    // Specifications about the target words are loaded
    // from the csv to the tasklist
    // then from the tasklist to the getStim() method as params
    var task = tasklist[0];

    // var outer_radius = task["outer_radius"];
    // var inner_radius = task["inner_radius"];
    var distance_between = task["distance_between"];
    var rule = task["rule"];
    var numberOfRings = 3;

    // Here I need a switch, according to the rule variable,
    // if the rule is "multiple", then it is used for hypo2, and
    // I need to have a different way to fetch the needed words data from the server
    switch (rule){
        case "multiple": // fetch the words in the hypo2 style
            // the 1st ajax call to gain the distractors data
            // after which another ajax call to gain the targets data
            $.ajax({
                url: flask_util.url_for('getDistractors'),
                success:
                    function(data){
                        distractors_hypo2 = data.map(function(dictionary){ // So in order for your code to work change data.map() to data.products.map() since products is an array which you can iterate upon.
                            return {
                                text: dictionary['text'],
                                weight: dictionary['fontsize'],
                                html: {class: dictionary['html']},
                                handlers: {
                                    mouseover: function() {this.style.cursor = "default";}
                                }
                            }
                        });
                        // alert(typeof(formed_distractors));
                        // distractors_hypo2 = formed_distractors;
                    
                        // the 2nd ajax call to gain the targets data
                        // Create 2D array for targets_hypo2
                        targets_hypo2 = [];
                        for (var i=0; i<numberOfRings; i++){
                            (function (i) {
                                    $.ajax({
                                        url: flask_util.url_for('getMultiTargets', {
                                            numberOfTargets: 3,
                                            correct_fontsize: task["target_2_fontsize"],
                                            wrong_fontsize: task["target_1_fontsize"],
                                            word_length: task["target_1_length"]}),
                                        success:
                                            function(data){
                                                formed_targets = data.map(function(dictionary){
                                                    return {
                                                        text: dictionary['text'],
                                                        weight: dictionary['fontsize'],
                                                        html: {class: dictionary['html']},
                                                        handlers: {
                                                            click: function() {postDataMulti($(this));},
                                                            mouseover: function() {this.style.cursor = "pointer";}
                                                        }
                                                    }
                                                });
                                                // alert(formed_targets);
                                                targets_hypo2[i] = formed_targets;
                                                if (i === numberOfRings-1){ // This is at the end of the for loop
                                                                            // Don't quite understand why success happens after all the url have been done
                                                                            // Tried complete:, but it assume the ajax is complete after the url request, 
                                                                            // but not after the three success callback
                                                    console.log(targets_hypo2);
                                                    $("#JQWC").addClass("jqcloud");

                                                    var ringsProcessed = 0;
                                                    targets_hypo2.forEach((target_array,index,array) => {
                                                        drawTargetsMulti(target_array,index,() => {
                                                            ringsProcessed++;
                                                            if(ringsProcessed === array.length){
                                                                drawDistractorsCallback(distractors_hypo2);
                                                            }
                                                        });
                                                    });
                                                }
                                            },
                                        dataType: "json"
                                    });
                                })(i);  // i.e. wrap the whole contents of your loop in an self-executing function.
                                        // Here, the value of outer i gets passed into the wrapping self-executing anonymous function; this 
                                        // unique value's location gets captured by the async callback. In this way, each async gets its own 
                                        // value, determined at the moment the self-executing function is invoked.
                        }   
                    },
                dataType: "json"
            });
            break;
        case "on_circle": // fetch the words for hypo1
            $.ajax({
                    url: flask_util.url_for('getStim', {
                        target_1_fontsize: task["target_1_fontsize"],
                        target_1_length: task["target_1_length"],
                        target_2_fontsize: task["target_2_fontsize"],
                        target_2_length: task["target_2_length"]}),
                    success:
                        function(data){
                            formed_words = data.map(function(dictionary) {
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
                            // words = formed_words;
                            for (var i = 0; i < 2; i++){
                                targetslist.push(formed_words.shift());
                            }
                            formed_distractors = formed_words;

                            // draw the targets first, then draw the distractors in the callback function
                            drawTargetCloud(targetslist,formed_distractors,distance_between,drawDistractorsCallback);

                        },
                    dataType: "json"
                });
            break;
        default:
            alert("rule not understand");
    }
}

function drawTargetCloud(target_array,distractor_array,distance_between,callback_drawDistractors) {
    $("#JQWC").addClass("jqcloud");
    drawTargets(target_array,distance_between); 
    callback_drawDistractors(distractor_array); 
    // Actually Here, 
    // Will the callback_drawDistractors(words) get called after the COMPLETION of the above drawTargets function?
    // When drawTargets invokes OTHER FUNCTION ?
}

function drawTargets(target_array,distance_between){
    var cloud_center_x = $("#JQWC").width() / 2.0;
    var cloud_center_y = $("#JQWC").height() / 2.0;
    // we have two target wrods, and we want to fix them onto a circle
    // that has the diameter of distance_between
    target0 = target_array[0];
    var font_size = target0["weight"];
        var word_span = $('<span>').attr(target0.html).addClass("target0");
        word_span.append(target0.text);
        $("#JQWC").append(word_span);
        word_span[0].style.visibility = "hidden";
        word_span[0].style.fontSize = font_size + "px";
        word_span[0].style.color = "black";
        var width = word_span.width();
        var height = word_span.height();
        var left;
        var top;
        var radius = distance_between / 2.0
        var x = Math.random()*(radius*2)-radius;
        var y = Math.sqrt(Math.pow(radius,2) - Math.pow(x,2)); // and here y will always be positive
        var coefficient = [-1,1];
            y = y*coefficient[Math.floor(Math.random()*coefficient.length)];
                        
        left = cloud_center_x - width / 2.0 - x;
        top = cloud_center_y - height / 2.0 - y;

        word_span[0].style.position = "absolute";
        word_span[0].style.left = left + "px";
        word_span[0].style.top = top + "px";
        

        $(word_span).bind("click", function(){postData($(this));});
        $(word_span).bind("mouseover", function() {this.style.cursor = 'pointer';});

    already_placed_targets.push(word_span[0]);

    target1 = target_array[1];
    var font_size = target1["weight"];
        var word_span = $('<span>').attr(target1.html).addClass("target1");
        word_span.append(target1.text);
        $("#JQWC").append(word_span);
        word_span[0].style.visibility = "hidden";
        word_span[0].style.fontSize = font_size + "px";
        word_span[0].style.color = "black";
        var width = word_span.width();
        var height = word_span.height();
        var left;
        var top;

        // target1 is place along the diameter of the cirle
        // the circle that target0 relies on
        left = cloud_center_x - width / 2.0 + x; // x is the x distance randomized for target0
        top = cloud_center_y - height / 2.0 + y; // y is the y distance randomized for target0

        word_span[0].style.position = "absolute";
        word_span[0].style.left = left + "px";
        word_span[0].style.top = top + "px";


        $(word_span).bind("click", function(){postData($(this));});
        $(word_span).bind("mouseover", function() {this.style.cursor = 'pointer';});

    already_placed_targets.push(word_span[0])

    var target_0 = $(".target0");
    var target_1 = $(".target1");
    var targets_x_distance = Math.abs((target_0.width() / 2.0 + parseFloat(target_0[0].style.left)) - (target_1.width() / 2.0 + parseFloat(target_1[0].style.left)));
    var targets_y_distance = Math.abs((target_0.height() / 2.0 + parseFloat(target_0[0].style.top)) - (target_1.height() / 2.0 + parseFloat(target_1[0].style.top)));
    var targets_distance = Math.sqrt(Math.pow(targets_x_distance,2) + Math.pow(targets_y_distance,2));
    console.log("distance between the two target is: " + targets_distance);
}

// The draw targets method, used by hypo2
function drawTargetsMulti(target_array,index,counter){
    var cloud_center_x = $("#JQWC").width() / 2.0;
    var cloud_center_y = $("#JQWC").height() / 2.0;
    var distance_between = index*300+75;
    var ring_num = index;
    target_array.forEach((target_word,index,array)=>{
        var font_size = target_word["weight"];
        var word_span = $('<span>').attr(target_word.html).addClass("ring"+ring_num);
        word_span.append(target_word.text);
        $("#JQWC").append(word_span);
        word_span[0].style.visibility = "hidden";
        word_span[0].style.fontSize = font_size + "px";
        word_span[0].style.color = "black";
        var width = word_span.width();
        var height = word_span.height();
        var radius = distance_between / 2.0
        var x = Math.random()*(radius*2)-radius;
        var y = Math.sqrt(Math.pow(radius,2) - Math.pow(x,2)); // and here y will always be positive
        var coefficient = [-1,1];
            y = y*coefficient[Math.floor(Math.random()*coefficient.length)];
        var left = cloud_center_x - width / 2.0 - x;
        var top = cloud_center_y - height / 2.0 - y;
        word_span[0].style.position = "absolute";
        word_span[0].style.left = left + "px";
        word_span[0].style.top = top + "px";
        $(word_span).bind("click", function(){postDataMulti($(this));});
        $(word_span).bind("mouseover", function() {this.style.cursor = 'pointer';});
        
        var hitTest = function(elem, other_elems) {
            // Pairwise overlap detection
            var overlapping = function(a, b) {
                if (Math.abs(2.0*a.offsetLeft + a.offsetWidth - 2.0*b.offsetLeft - b.offsetWidth) < a.offsetWidth + b.offsetWidth) {
                    if (Math.abs(2.0*a.offsetTop + a.offsetHeight - 2.0*b.offsetTop - b.offsetHeight) < a.offsetHeight + b.offsetHeight) {
                        return true;
                    }
                }
                return false;
            };
            var i = 0;
            // Check elements for overlap one by one, stop and return false as soon as an overlap is found
            for(i = 0; i < other_elems.length; i++) {
                if (overlapping(elem, other_elems[i])) {
                    return true;
                }
            }
            return false;
        };

        do{
            var overlap = hitTest(word_span[0],already_placed_targets);
            if (overlap === true) {
                var x = Math.random()*(radius*2)-radius;
                var y = Math.sqrt(Math.pow(radius,2) - Math.pow(x,2)); // and here y will always be positive
                var coefficient = [-1,1];
                    y = y*coefficient[Math.floor(Math.random()*coefficient.length)];
                var left = cloud_center_x - width / 2.0 - x;
                var top = cloud_center_y - height / 2.0 - y;
                word_span[0].style.left = left + "px";
                word_span[0].style.top = top + "px";
            }
        } while (overlap === true)

        already_placed_targets.push(word_span[0]);
    });
    counter();
}

function drawDistractorsCallback(word_array){
    $("#JQWC").jQCloud(word_array,already_placed_targets,"distractor",
        {   delayedMode: false,
            afterCloudRender: () => {
                startTime = new Date();
                $.each($(".target"),(index,value)=>{value.style.visibility = "visible";});
            }
        }
    );
}

function postData(clickedword){
    endTime = new Date();
    var timeDiff = endTime - startTime; // in ms
    timeDiff /= 1000; // strip the ms
    // alert(typeof(timeDiff));
    // alert('time taken: ' + timeDiff);
    
    var number_of_words = document.getElementById("JQWC").childElementCount - 1; // minus the dot span
    var span_content = document.getElementById("JQWC").innerHTML; //the span content
    
    var cloud_width = $("#JQWC").width(); // width of the container in int
    var cloud_height = $("#JQWC").height(); // height of the container in int
    
    var cloud_center_x = cloud_width / 2.0; // the center x in int
    var cloud_center_y = cloud_height / 2.0; // the center y in int

    var target_0 = $(".target0");
    var target_1 = $(".target1");
    var targets_x_distance = Math.abs((target_0.width() / 2.0 + parseFloat(target_0[0].style.left)) - (target_1.width() / 2.0 + parseFloat(target_1[0].style.left)));
    var targets_y_distance = Math.abs((target_0.height() / 2.0 + parseFloat(target_0[0].style.top)) - (target_1.height() / 2.0 + parseFloat(target_1[0].style.top)));
    var distance_between_targets = Math.sqrt(Math.pow(targets_x_distance,2) + Math.pow(targets_y_distance,2));

    var correct_word = target_0.css('font-size') > target_1.css('font-size') ? target_0:target_1;
    var wrong_word = target_0.css('font-size') < target_1.css('font-size') ? target_0:target_1;

    var correct_word_fontsize = parseInt(correct_word.css("font-size"));
    var wrong_word_fontsize = parseInt(wrong_word.css("font-size"));

    var correct_word_width = correct_word.width();
    var correct_word_height = correct_word.height();
    var wrong_word_width = wrong_word.width();
    var wrong_word_height = wrong_word.height();
    
    // the x and y coordinate of the two target words
    // take the center of the cloud to be the origin
    // e.g. if the container is of size (1000,1000), then the origin is (500,500)
    // all the subsequent x and y coordinates are with respect to that origin
    var correct_word_x = parseFloat(correct_word.css("left")) + correct_word_width/2.0 - cloud_center_x;
    var correct_word_y = cloud_center_y - parseFloat(correct_word.css("top")) - correct_word_height/2.0;
    var wrong_word_x = parseFloat(wrong_word.css("left")) + wrong_word_width/2.0 - cloud_center_x;
    var wrong_word_y = cloud_center_y - parseFloat(wrong_word.css("top")) - wrong_word_height/2.0;

    var correct_word_center_distance = Math.sqrt(Math.pow(correct_word_x,2) + Math.pow(correct_word_y,2));
    var wrong_word_center_distance = Math.sqrt(Math.pow(wrong_word_x,2) + Math.pow(wrong_word_y,2));

    var word_data = {
        "turker_id": turker_id,

        "cloud_width": cloud_width,
        "cloud_height": cloud_height,
        "cloud_center_x": cloud_center_x,
        "cloud_center_y": cloud_center_y,

        "clicked_word": clickedword[0].innerHTML,
        "correct_word": correct_word[0].innerHTML,
        "wrong_word": wrong_word[0].innerHTML,
        "distance_between_targets": distance_between_targets,
        "time": timeDiff,

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

function postDataMulti(clickedword){
    endTime = new Date();
    var timeDiff = endTime - startTime; // in ms
    timeDiff /= 1000; // strip the ms
    var number_of_words = document.getElementById("JQWC").childElementCount - 1; // minus the dot span
    var span_content = document.getElementById("JQWC").innerHTML; //the span content
    var cloud_width = $("#JQWC").width(); // width of the container in int
    var cloud_height = $("#JQWC").height(); // height of the container in int
    var cloud_center_x = cloud_width / 2.0; // the center x in int
    var cloud_center_y = cloud_height / 2.0; // the center y in int

    var number_of_targets = $(".target").length;
    var num_words_in_ring0 = $(".ring0").length;
    var num_words_in_ring1 = $(".ring1").length;
    var num_words_in_ring2 = $(".ring2").length;

    var fontsizes = [];
    $(".target").each((index,target)=>{fontsizes.push(parseInt(target.style.fontSize));});
    var correct_fontsize = Math.max(...fontsizes);
    var wrong_fontsize = Math.min(...fontsizes);

    var clicked_word_text = clickedword[0].innerHTML;
    var clicked_word_fontsize = parseInt(clickedword[0].style.fontSize);
    var clickedword_width = clickedword.width();
    var clickedword_height = clickedword.height();
    var clicked_word_x = parseFloat(clickedword.css("left")) + clickedword_width/2.0 - cloud_center_x;
    var clicked_word_y = cloud_center_y - parseFloat(clickedword.css("top")) - clickedword_height/2.0;
    var clicked_word_center_distance = Math.sqrt(Math.pow(clicked_word_x,2) + Math.pow(clicked_word_y,2));

    var word_data = {
        "turker_id": turker_id,
        "cloud_width": cloud_width,
        "cloud_height": cloud_height,
        "cloud_center_x": cloud_center_x,
        "cloud_center_y": cloud_center_y,

        "clicked_word": clicked_word_text,
        "time": timeDiff,
        "clicked_word_x": clicked_word_x,
        "clicked_word_y": clicked_word_y,
        "clicked_word_center_distance": clicked_word_center_distance,
        "clicked_word_fontsize": clicked_word_fontsize,
        "correct_fontsize": correct_fontsize,
        "wrong_fontsize": wrong_fontsize,

        "num_words_in_ring0": num_words_in_ring0,
        "num_words_in_ring1": num_words_in_ring1,
        "num_words_in_ring2": num_words_in_ring2,
        "number_of_targets": number_of_targets,
        "number_of_words": number_of_words,
        "span_content": span_content,

    };
    alert(clickedword[0].innerHTML + "I am clicked!");
    $.ajax({
        type: 'POST',
        url: post_data_multi_url,
        data: word_data,
        success: function(response) {
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