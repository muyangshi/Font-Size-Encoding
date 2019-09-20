/*
 * WordCloud.js
 * Muyang Shi, 25 June 2019
 * Currently being used for the pilot study of comparing the fontsize
 * of TWO target words -- Not anymore! :D
 * 
 * as of 31 July, starting to implement for hypo2
 * 
 * as of Aug 8, we want N target words for hypo1
 * 
 * as of Aug 9, some changes in the design.
 * Specify "single_circle" or "multiple_circles" in the test_length.csv
 * there can be multiple targets on a single_circle, except that 
 * they will no be exactly on the opposite side of each other
 * since there  could be more than two target words
 * 
 * as of Aug 22, try to let click_on_cross = visible, to reduce visual lag.
 */


 /*
 * Global variables stored here are for the ease of access for functions
 * timeout_func is pointing to the setTimeout function that create the blocks, which should be canceled if the user react before the blocks are created.
 * already_placed_target is for ease of access within the helper funcitons
 */
tasklist = shuffle(tasklist);

var task;

var total_num = tasklist.length;
var target_num;

var startTime;
var endTime;

var timeout_func;
var already_placed_targets;

var clicked_word_stack = null; // "stack" that holds the clicked_word
var experiment = null; //Specify which postData function to be used


(function initialize() {
    // var start = document.getElementById('Button_startStimuli');
    // start.onclick = onStartButtonClicked;
    console.log("device pixel ratio is: " + window.devicePixelRatio);
    // $("#center_cross").bind("click",function(){onStartButtonClicked();});
    // $("#center_cross").trigger("click");
    onStartButtonClicked();
})();



function onStartButtonClicked() {
    $("#center_cross").css("cursor", "pointer").off();
    // $("#Status_Bar").append('<div id="notification" style="font-size: larger; text-align: center;">Loading...</div>');
    task = tasklist[0];
        
    // Clear the page content to contain only the fixation cross, and empty the word arrays
    already_placed_targets = [];
    clicked_word_stack = null;

    // Add Process bar to the Status_Bar div
    document.getElementById("Status_Bar").innerHTML = '<div id="progress_bar" style="text-align: center;"><h3>You have ' + tasklist.length + ' tasks left</h3></div>';
    $("#Status_Bar").append('<div id="notification" style="font-size: larger; text-align: center;">Loading...</div>');
    load_cloud();
}
 
function load_cloud(){
    // task = tasklist[0];
    var rule = task["rule"];
    /*
     * switch control for differen rule
     * single_circle: multiple targets on a single circle
     * multiple_circles: multiple targets on multiple circles
     * opposite_on_circle: 2 targets on a single circle. the 2 target words are on the same diameter of that circle
     */
    switch (rule) {
        case "opposite_on_circle":
            experiment = "opposite_on_circle";
            target_num = 2;
            // The two target words being positioned on the opposite side of a circle
            var targets;
            var distractors;
            $.ajax({
                url: $SCRIPT_ROOT +"/_" + "getStim" + "/" + task["small_fontsize"] + "/" + task["smallword_length"] + "/" + task["big_fontsize"] + "/" + task["bigword_length"],
                success:
                    function (data) {
                        distractors = data.map(function (dictionary) {
                            if (dictionary["html"] === "target") {
                                return {
                                    text: dictionary['text'],
                                    weight: dictionary['fontsize'],
                                    html: { class: dictionary['html'],
                                            style: 'visibility: hidden' },
                                    handlers: {
                                        click: function () { postData($(this)); },
                                        mouseover: function () { this.style.cursor = 'pointer'; }
                                    }
                                }
                            }
                            else {
                                return {
                                    text: dictionary['text'],
                                    weight: dictionary['fontsize'],
                                    html: { class: dictionary['html'],
                                            style: 'visibility: hidden' },
                                    handlers: {
                                        mouseover: function () { this.style.cursor = "default"; }
                                    }
                                }
                            }
                        });

                        targets = [];
                        for (var i = 0; i < 2; i++) {
                            targets.push(distractors.shift());
                        }
                        drawTargetsOpposite(targets, distractors, task["distance_between"], task["flash_time"], drawDistractorsCallback);
                    },
                dataType: "json"
            });
            break;
        case "single_circle":
            experiment = "single_circle";
            target_num = task["number_of_targets"];
            var distractors;
            var targets;
            $.ajax({
                url: $SCRIPT_ROOT+ "/_getDistractors",
                // url: flask_util.url_for('getDistractors'),
                success:
                    function (data) {
                        distractors = data.map(function (dictionary) {
                            return {
                                text: dictionary['text'],
                                weight: dictionary['fontsize'],
                                html: { class: dictionary['html'],
                                        style: 'visibility: hidden' },
                                handlers: { mouseover: function () { this.style.cursor = "default"; } }
                            }
                        });
                        var number_of_targets = task["number_of_targets"];
                        var correct_fontsize = task["big_fontsize"];
                        var wrong_fontsize = task["small_fontsize"];
                        var word_length = task["smallword_length"];
                        $.ajax({
                            url: $SCRIPT_ROOT + `/_getMultiTargets/${number_of_targets}/${correct_fontsize}/${wrong_fontsize}/${word_length}`,
                            success:
                                function (data) {
                                    targets = data.map(function (dictionary) {
                                        return {
                                            text: dictionary['text'],
                                            weight: dictionary['fontsize'],
                                            html: { class: dictionary['html'],
                                                    style: 'visibility: hidden' },
                                            handlers: {
                                                click: function () { postDataMulti($(this)); },
                                                mouseover: function () { this.style.cursor = "pointer"; }
                                            }
                                        }
                                    });
                                    var radius = task["distance_between"] / 2;
                                    drawTargetsOnRing(targets, distractors, radius, task["flash_time"], drawDistractorsCallback);
                                },
                            dataType: "json"
                        });
                    },
                dataType: "json"
            });
            break;
        case "multiple_circles":
            experiment = "multiple_circles";
            target_num = task["number_of_targets"]
            // 3 targets on each level of circle
            var number_of_rings = 3;
            var distractors;
            var targets;
            $.ajax({
                url: $SCRIPT_ROOT+'/_getDistractors',
                success:
                    function (data) {
                        distractors = data.map(function (dictionary) {
                            // So in order for your code to work 
                            // change data.map() to data.products.map() 
                            // since products is an array which you can iterate upon.
                            // Here, specify the ajax dataType as "json" also works
                            return {
                                text: dictionary['text'],
                                weight: dictionary['fontsize'],
                                html: { class: dictionary['html'],
                                        style: 'visibility: hidden' },
                                handlers: { mouseover: function () { this.style.cursor = "default"; } }
                            }
                        });

                        // the 2nd ajax call to gain the targets data
                        // Create 2D array that contains the targets on each circle.
                        targets = [];
                        for (var i = 0; i < number_of_rings; i++) {
                            (function (i) {
                                var number_of_targets = task["number_of_targets"];
                                var correct_fontsize = task["big_fontsize"];
                                var wrong_fontsize = task["small_fontsize"];
                                var word_length = task["smallword_length"];
                                $.ajax({
                                    url: $SCRIPT_ROOT + `/_getMultiTargets/${number_of_targets}/${correct_fontsize}/${wrong_fontsize}/${word_length}`,
                                    success:
                                        function (data) {
                                            formed_targets = data.map(function (dictionary) {
                                                return {
                                                    text: dictionary['text'],
                                                    weight: dictionary['fontsize'],
                                                    html: { class: dictionary['html'],
                                                            style: 'visibility: hidden' },
                                                    handlers: {
                                                        click: function () { postDataMulti($(this)); },
                                                        mouseover: function () { this.style.cursor = "pointer"; }
                                                    }
                                                }
                                            });
                                            // alert(formed_targets);
                                            targets[i] = formed_targets;
                                            if (i === number_of_rings - 1) { // This is at the end of the for loop
                                                // Don't quite understand why success happens after all the url have been done
                                                // Tried complete:, but it assume the ajax is complete after the url request, 
                                                // but not after the three success callback
                                                drawTargetsMultiRings(targets, distractors, task["flash_time"]);
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
        default:
            alert("rule not understand");
    }
}

function show_word(word_type){
    switch(word_type){
        case "both":
            $(".target, .distractor").css("visibility","visible");
            break;
        case "target":
            $(".target").css("visibility","visible");
            break;
        case "distractor":
            $(".distractor").css("visibility","visible");
            break;
    }
}
function hide_word(word_type){
    switch(word_type){
        case "both":
            $(".target, .distractor").css("visibility","hidden");
            break;
        case "target":
            $(".target").css("visibility","hidden");
            break;
        case "distractor":
            $(".distractor").css("visibility","hidden");
            break;
    }
}

// show the cloud
// start the timer
function show_stim(block,flash_time){
    $("#notification").html("");
    $("#center_cross").off();
    show_word("both");
    startTime = new Date();

    if (block === true){
        var create_block = ()=>{
            $.each($(".target"), (index, target) => {
                var target_left = parseFloat(target.style.left);
                var target_top = parseFloat(target.style.top);
                var block = makeBlock("block" + index, target_left, target_top);
                hide_word("target");
                $("#JQWC").append(block);

                $("#block" + index).bind("click", function () {
                    // highlight the clicked block
                    if (clicked_word_stack === null) {
                        $(this).css("border", "3px solid");
                    }
                    // hide the irrelevant words and blocks to prevent changing mind
                    hide_word("both");
                    $(".block").css("visibility","hidden");

                    // trigger the target underneath's click, which add this word
                    // to the clicked_word_stack
                    $("#target" + index).trigger("click");
                });
            });
        }
        timeout_func = setTimeout(create_block,flash_time);
    }
}


// Two targets drawn opposite along the diameter of a circle
// Click block then click the central cross to continue
function drawTargetsOpposite(target_array, distractor_array, distance_between, flash_time, callback) {
    $("#JQWC").addClass("jqcloud");
    var cloud_center_x = $("#JQWC").width() / 2.0;
    var cloud_center_y = $("#JQWC").height() / 2.0;
    // we have two target wrods, and we want to fix them onto a circle
    // that has the diameter of distance_between
    target0 = target_array[0];
    var font_size = target0["weight"];
    var word_span = $('<span>').attr(target0.html).addClass("ring0").attr("id", "target0");
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
    var x = Math.random() * (radius * 2) - radius;
    var y = Math.sqrt(Math.pow(radius, 2) - Math.pow(x, 2)); // and here y will always be positive
    var coefficient = [-1, 1];
    y = y * coefficient[Math.floor(Math.random() * coefficient.length)];

    left = cloud_center_x - width / 2.0 - x;
    top = cloud_center_y - height / 2.0 - y;

    word_span[0].style.position = "absolute";
    word_span[0].style.left = left + "px";
    word_span[0].style.top = top + "px";


    $(word_span).bind("click", function () { click_word($(this)); });
    $(word_span).bind("mouseover", function () { this.style.cursor = 'pointer'; });

    already_placed_targets.push(word_span[0]);

    target1 = target_array[1];
    var font_size = target1["weight"];
    var word_span = $('<span>').attr(target1.html).addClass("ring0").attr('id', 'target1');
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


    $(word_span).bind("click", function () { click_word($(this)); });
    $(word_span).bind("mouseover", function () { this.style.cursor = 'pointer'; });

    already_placed_targets.push(word_span[0])

    var target_0 = $("#target0");
    var target_1 = $("#target1");
    var targets_x_distance = Math.abs((target_0.width() / 2.0 + parseFloat(target_0[0].style.left)) - (target_1.width() / 2.0 + parseFloat(target_1[0].style.left)));
    var targets_y_distance = Math.abs((target_0.height() / 2.0 + parseFloat(target_0[0].style.top)) - (target_1.height() / 2.0 + parseFloat(target_1[0].style.top)));
    var targets_distance = Math.sqrt(Math.pow(targets_x_distance, 2) + Math.pow(targets_y_distance, 2));
    console.log("distance between the two target is: " + targets_distance);

    var flash = Boolean;
    if (flash_time !== -1){
        flash = true;
    } else {
        flash = false;
    }
    callback(distractor_array, flash, flash_time);
}

// Multiple targets drawn on a single circle
// Click the block first then click the central red cross to continue
function drawTargetsOnRing(target_array, distractor_array, radius, flash_time, callback) {
    // $("#Status_Bar").append('<div id="notification" style="font-size: larger; text-align: center;">Loading...</div>');
    $("#JQWC").addClass("jqcloud");
    var cloud_center_x = $("#JQWC").width() / 2.0;
    var cloud_center_y = $("#JQWC").height() / 2.0;
    target_array.forEach((target_word, index, array) => {
        var font_size = target_word["weight"];
        var word_span = $('<span>').attr(target_word.html)
            .addClass("ring0")
            .attr("id", "target" + index);
        word_span.append(target_word.text);
        $("#JQWC").append(word_span);
        word_span[0].style.visibility = "hidden";
        word_span[0].style.fontSize = font_size + "px";
        word_span[0].style.color = "black";
        var width = word_span.width();
        var height = word_span.height();
        // var radius = distance_between / 2.0
        var x = Math.random() * (radius * 2) - radius;
        var y = Math.sqrt(Math.pow(radius, 2) - Math.pow(x, 2)); // and here y will always be positive
        var coefficient = [-1, 1];
        y = y * coefficient[Math.floor(Math.random() * coefficient.length)];
        var left = cloud_center_x - width / 2.0 - x;
        var top = cloud_center_y - height / 2.0 - y;
        word_span[0].style.position = "absolute";
        word_span[0].style.left = left + "px";
        word_span[0].style.top = top + "px";
        $(word_span).bind("click", function () { click_word($(this)); });
        $(word_span).bind("mouseover", function () { this.style.cursor = 'pointer'; });

        var hitTest = function (elem, other_elems) {
            // Pairwise overlap detection
            var overlapping = function (a, b) {
                if (Math.abs(2.0 * a.offsetLeft + a.offsetWidth - 2.0 * b.offsetLeft - b.offsetWidth) < a.offsetWidth + b.offsetWidth) {
                    if (Math.abs(2.0 * a.offsetTop + a.offsetHeight - 2.0 * b.offsetTop - b.offsetHeight) < a.offsetHeight + b.offsetHeight) {
                        return true;
                    }
                }
                return false;
            };
            var i = 0;
            // Check elements for overlap one by one, stop and return false as soon as an overlap is found
            for (i = 0; i < other_elems.length; i++) {
                if (overlapping(elem, other_elems[i])) {
                    return true;
                }
            }
            return false;
        };

        do {
            var overlap = hitTest(word_span[0], already_placed_targets);
            if (overlap === true) {
                var x = Math.random() * (radius * 2) - radius;
                var y = Math.sqrt(Math.pow(radius, 2) - Math.pow(x, 2)); // and here y will always be positive
                var coefficient = [-1, 1];
                y = y * coefficient[Math.floor(Math.random() * coefficient.length)];
                var left = cloud_center_x - width / 2.0 - x;
                var top = cloud_center_y - height / 2.0 - y;
                word_span[0].style.left = left + "px";
                word_span[0].style.top = top + "px";
            }
        } while (overlap === true)

        already_placed_targets.push(word_span[0]);
    });
    var flash = Boolean;
    if (flash_time !== -1){
        flash = true;
    } else {
        flash = false;
    }
    callback(distractor_array, flash, flash_time);
}

function drawTargetsMultiRings(target_2Darray, distractor_array, flash_time) {
    $("#JQWC").addClass("jqcloud");
    var drawTargetsEachRing = (target_array, index, counter) => {
        var cloud_center_x = $("#JQWC").width() / 2.0;
        var cloud_center_y = $("#JQWC").height() / 2.0;
        var distance_between = index * 200 + 100;
        var ring_num = index;
        target_array.forEach((target_word, index, array) => {
            var font_size = target_word["weight"];
            var word_span = $('<span>').attr(target_word.html).addClass("ring" + ring_num).css("id", "ring" + ring_num + "target" + index);
            word_span.append(target_word.text);
            $("#JQWC").append(word_span);
            word_span[0].style.visibility = "hidden";
            word_span[0].style.fontSize = font_size + "px";
            word_span[0].style.color = "black";
            var width = word_span.width();
            var height = word_span.height();
            var radius = distance_between / 2.0
            var x = Math.random() * (radius * 2) - radius;
            var y = Math.sqrt(Math.pow(radius, 2) - Math.pow(x, 2)); // and here y will always be positive
            var coefficient = [-1, 1];
            y = y * coefficient[Math.floor(Math.random() * coefficient.length)];
            var left = cloud_center_x - width / 2.0 - x;
            var top = cloud_center_y - height / 2.0 - y;
            word_span[0].style.position = "absolute";
            word_span[0].style.left = left + "px";
            word_span[0].style.top = top + "px";
            $(word_span).bind("click", function () { click_word($(this)); });
            $(word_span).bind("mouseover", function () { this.style.cursor = 'pointer'; });

            var hitTest = function (elem, other_elems) {
                // Pairwise overlap detection
                var overlapping = function (a, b) {
                    if (Math.abs(2.0 * a.offsetLeft + a.offsetWidth - 2.0 * b.offsetLeft - b.offsetWidth) < a.offsetWidth + b.offsetWidth) {
                        if (Math.abs(2.0 * a.offsetTop + a.offsetHeight - 2.0 * b.offsetTop - b.offsetHeight) < a.offsetHeight + b.offsetHeight) {
                            return true;
                        }
                    }
                    return false;
                };
                var i = 0;
                // Check elements for overlap one by one, stop and return false as soon as an overlap is found
                for (i = 0; i < other_elems.length; i++) {
                    if (overlapping(elem, other_elems[i])) {
                        return true;
                    }
                }
                return false;
            };

            do {
                var overlap = hitTest(word_span[0], already_placed_targets);
                if (overlap === true) {
                    var x = Math.random() * (radius * 2) - radius;
                    var y = Math.sqrt(Math.pow(radius, 2) - Math.pow(x, 2)); // and here y will always be positive
                    var coefficient = [-1, 1];
                    y = y * coefficient[Math.floor(Math.random() * coefficient.length)];
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
    var ringsProcessed = 0;
    target_2Darray.forEach((target_array, index, array) => {
        drawTargetsEachRing(target_array, index, () => {
            ringsProcessed++;
            if (ringsProcessed === array.length) {
                drawDistractorsCallback(distractor_array, false, flash_time);
            }
        });
    });
}

function drawDistractorsCallback(word_array, block, flash_time) {
    $("#JQWC").jQCloud(word_array, already_placed_targets, "distractor",{
        delayedMode: false,
        afterCloudRender: () => {
            if ($(".target").length > target_num && $(".distractor").length >250) {
                console.log("too many targets and distractors appeared on screen")
                nextTask();
            }
            else {
                // console.log(block);
                // console.log(flash_time);
                $("#notification").html("Task loaded. Click the red cross to start")
                // $("#Status_Bar").append('<div id="notification" style="font-size: larger;">Task loaded. Click the red cross to start.</div>');
                $("#center_cross").css("cursor","pointer").off()
                    .bind("click",()=>{show_stim(block,flash_time)});
            }
        }
    });
}
function makeBlock(id, left, top) {
    var block = $('<span>').attr('id', id)
        .attr('class', 'block')
        .css('font-size', '25px')
        .css('padding-left', '30px')
        .css('background', '#2C3539')
        .css('position', 'absolute')
        .css('left', left)
        .css('top', top)
        .css('cursor', 'pointer')
        .html('&nbsp;&nbsp;&nbsp;&nbsp;');
    return block;
}


function click_word(clickedword) {
    endTime = new Date();
    clearTimeout(timeout_func);
    hide_word("both");
    $("#notification").html("Processing...");
    // $("#Status_Bar").append('<div id="notification" style="font-size: larger; text-align: center;">Processing...</div>');
    clicked_word_stack = clickedword;
    submit_word();
}

function submit_word() {
    if (clicked_word_stack != null) {
        switch (experiment) {
            case "opposite_on_circle":
                postData(clicked_word_stack);
                break;
            case "single_circle":
                postDataMulti(clicked_word_stack);
                break;
            case "multiple_circles":
                postDataMulti(clicked_word_stack);
                break;
            default:
                alert("Which postData() to use?");
        }
    }
    else {
        alert("You haven't select anything");
    }
}



// The postData function used for opposite_on_circle
function postData(clickedword) {
    // alert(task['flash_time'])
    clearTimeout(timeout_func);
    // endTime = new Date();
    var timeDiff = endTime - startTime; // in ms
    timeDiff /= 1000; // strip the ms
    // alert(typeof(timeDiff));
    // alert('time taken: ' + timeDiff);

    var question_index = total_num - tasklist.length + 1;

    if ($(".block").length !== 0){
        var block_width = $(".block").width() + parseInt($(".block").css("padding-left"));
        var block_height = $(".block").height();
    }

    var number_of_words = document.getElementById("JQWC").childElementCount - 1; // minus the dot span
    var span_content = document.getElementById("JQWC").innerHTML; //the span content

    var cloud_width = $("#JQWC").width(); // width of the container in int
    var cloud_height = $("#JQWC").height(); // height of the container in int

    var cloud_center_x = cloud_width / 2.0; // the center x in int
    var cloud_center_y = cloud_height / 2.0; // the center y in int

    var target_0 = $("#target0");
    var target_1 = $("#target1");
    var targets_x_distance = Math.abs((target_0.width() / 2.0 + parseFloat(target_0[0].style.left)) - (target_1.width() / 2.0 + parseFloat(target_1[0].style.left)));
    var targets_y_distance = Math.abs((target_0.height() / 2.0 + parseFloat(target_0[0].style.top)) - (target_1.height() / 2.0 + parseFloat(target_1[0].style.top)));
    var distance_between_targets = Math.sqrt(Math.pow(targets_x_distance, 2) + Math.pow(targets_y_distance, 2));

    var correct_word = target_0.css('font-size') > target_1.css('font-size') ? target_0 : target_1;
    var wrong_word = target_0.css('font-size') < target_1.css('font-size') ? target_0 : target_1;

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
    var correct_word_x = parseFloat(correct_word.css("left")) + correct_word_width / 2.0 - cloud_center_x;
    var correct_word_y = cloud_center_y - parseFloat(correct_word.css("top")) - correct_word_height / 2.0;
    var wrong_word_x = parseFloat(wrong_word.css("left")) + wrong_word_width / 2.0 - cloud_center_x;
    var wrong_word_y = cloud_center_y - parseFloat(wrong_word.css("top")) - wrong_word_height / 2.0;

    var correct_word_center_distance = Math.sqrt(Math.pow(correct_word_x, 2) + Math.pow(correct_word_y, 2));
    var wrong_word_center_distance = Math.sqrt(Math.pow(wrong_word_x, 2) + Math.pow(wrong_word_y, 2));

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
        "question_index": question_index,

        "block_width": block_width,
        "block_height": block_height,

        "flash_time": task["flash_time"]
    };

    // $.post("/randomStim/post_data", word_data);

    $.ajax({
        type: 'POST',
        url: post_data_url,
        data: JSON.stringify(word_data),
        contentType: "application/json",
        success: function (response) {
            nextTask();
            console.log(response);
        },
        error: function (error) {
            alert('error saving data');
            console.log(error);
        }
    });
}

function postDataMulti(clickedword) {
    // alert(task['flash_time'])
    // endTime = new Date();
    var timeDiff = endTime - startTime; // in ms
    timeDiff /= 1000; // strip the ms

    var question_index = total_num - tasklist.length + 1;

    if ($(".block").length !== 0){
        var block_width = $(".block").width() + parseInt($(".block").css("padding-left"));
        var block_height = $(".block").height();
    }

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
    $(".target").each((index, target) => { fontsizes.push(parseInt(target.style.fontSize)); });
    var correct_fontsize = Math.max(...fontsizes);
    var wrong_fontsize = Math.min(...fontsizes);

    var clicked_word_text = clickedword[0].innerHTML;
    var clicked_word_fontsize = parseInt(clickedword[0].style.fontSize);
    var clicked_word_width = clickedword.width();
    var clicked_word_height = clickedword.height();
    var clicked_word_x = parseFloat(clickedword.css("left")) + clicked_word_width / 2.0 - cloud_center_x;
    var clicked_word_y = cloud_center_y - parseFloat(clickedword.css("top")) - clicked_word_height / 2.0;
    var clicked_word_center_distance = Math.sqrt(Math.pow(clicked_word_x, 2) + Math.pow(clicked_word_y, 2));

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
        "clicked_word_width": clicked_word_width,
        "clicked_word_height": clicked_word_height,
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

        "question_index": question_index,
        "block_width": block_width,
        "block_height": block_height,

        "flash_time": task["flash_time"]
    };

    $.ajax({
        type: 'POST',
        url: post_data_multi_url,
        data: JSON.stringify(word_data),
        contentType: "application/json",
        success: function (response) {
            nextTask();
            console.log(response);
            // console.log(word_data);
        },
        error: function (error) {
            alert('error saving data');
            console.log(error);
        }
    });
}

function nextTask() {
    document.getElementById('JQWC').innerHTML = '<span id="center_cross" style="position: absolute;top: 480px;left: 487.0156px;font-size: 30px;color: red;">&#10011;</span>';

    tasklist.shift();
    if (tasklist.length == 0) {
        console.log('All tasks completed')
        var input = $("<input>").attr("type", "hidden").attr("name", "turker_id").val(turker_id);
        $('#get_completion_page').append(input).submit();
    } else {
        setTimeout(onStartButtonClicked);
    }
}

function shuffle(array) {
    var currentIndex = array.length, temporaryValue, randomIndex;
  
    // While there remain elements to shuffle...
    while (0 !== currentIndex) {
  
      // Pick a remaining element...
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;
  
      // And swap it with the current element.
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }
  
    return array;
}