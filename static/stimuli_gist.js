/*
 * WordCloud.js
 * Muyang Shi, 19 December 2019
 * 
 * Create stimuli (place the words) for gist experiment
 * tasklist_gist.csv specifies the mean size of the words.
 * placement is done by using the jqcloud spiral algorithm.
 * Size and Placement each has two levels -- stratified versus random
 * 'Method' is the word used for differnet conditions: A1, B, C, D, etc.
 */

tasklist = shuffle(tasklist);

var task;

// var total_num = tasklist.length;
// var target_num;

var startTime;
var endTime;

var already_placed_targets;



(function initialize() {
    // var start = document.getElementById('Button_startStimuli');
    // start.onclick = onStartButtonClicked;
    console.log("device pixel ratio is: " + window.devicePixelRatio);
    // $("#center_cross").bind("click",function(){onStartButtonClicked();});
    // $("#center_cross").trigger("click");
    onStartButtonClicked();
})();



function onStartButtonClicked() {
    task = tasklist[0]; // A1
    // task = tasklist[1]; // A2
    // task = tasklist[2]; // B
    // task = tasklist[3]; // C
    // task = tasklist[4]; // D
        
    // Clear the page content to contain only the fixation cross, and empty the word arrays
    already_placed_targets = [];
    $("#center_cross").css("cursor", "pointer").off();
    document.getElementById("Status_Bar").innerHTML = '<div id="progress_bar" style="text-align: left;"><h3>You have ' + tasklist.length + ' tasks left</h3></div>';
    $("#JQWC").show();
    // Add Process bar to the Status_Bar div
    $("#Status_Bar").append('<div id="notification" style="font-size: larger; text-align: left;">Loading...</div>');
    
    // Draw the word cloud
    load_cloud();
}
 
function load_cloud(){
    var method = task["method"];
    var topic_num = task["topic_num"];
    var size1mean = task["size1mean"];
    var size1sd = task["size1sd"];
    var dist1mean = task["dist1mean"];
    var dist1sd = task["dist1sd"];
    var n1 = task["n1"];
    var size2mean = task["size2mean"];
    var size2sd = task["size2sd"];
    var dist2mean = task["dist2mean"];
    var dist2sd = task["dist2sd"];
    var n2 = task["n2"];
    var targets;
    var topics;
    $.ajax({
        url:$SCRIPT_ROOT + "/" + `_getTopicWords/${topic_num}/${size1mean}/${size1sd}/${dist1mean}/${dist1sd}/${n1}/${size2mean}/${size2sd}/${dist2mean}/${dist2sd}/${n2}`,
        success:
            function (data) {
                topics = data["topics"];
                let word_list = data["word_list"];
                targets = word_list.map(function (w){
                    return {
                        text: w['text'],
                        weight: w['fontsize'],
                        radius: w['dist'],
                        html: {class: w['html']},
                        handler:{
                            click: function() {console.log($(this));},
                            mouseover: function(){this.style.cursor = 'pointer';}
                        }
                    }
                }); // data.map()

                // targets.sort(function(a,b){
                //     return b.weight - a.weight
                // }); // sort everything based on font size (sort together)

                // const n = targets.length;
                // let arr1 = targets.splice(0,n/2);
                // let arr2 = targets;
                // arr1.sort(function(a,b){return b.weight - a.weight});
                // arr2.sort(function(a,b){return b.weight - a.weight});
                // targets = arr1.concat(arr2); // sort within each topic

                switch(method){
                    case "A1": // A1: topic2 Smaller words outside, topic1 Bigger words inside
                        targets.sort(function(a,b){
                            return b.weight - a.weight
                        }); // sort everything descending based on font size (sort together)
                        break;
                    case "A2": // A2: topic2 Bigger words outside, topic1 smaller words inside
                        targets.sort(function(a,b){
                            return a.weight - b.weight
                        }); // sort everything descending based on font size (sort together)
                        break;
                    case "B": // B1: topic 1 is placed towards the center, topic 2 to the exterior
                        break;
                    case "C": // Shuffle the targets. The two topics differ only in size
                        targets = shuffle(targets);
                        break;
                    case "D1": // The two topics do not differ from each other
                        // targets = shuffle(targets);
                        targets.sort(function(a,b){
                            return b.weight - a.weight
                        }); // sort everything based on font size (sort together) baseline for A1
                        break;
                    case "D2":
                        targets = shuffle(targets);
                        break;
                    default:
                        alert("unspecified");
                        throw new Error("Something went badly wrong!");
                }
                // targets = shuffle(targets);
                // const n = targets.length
                // const t1 = targets.splice(0,n/2);
                // const t2 = targets;
                // const n = t1.length;
                // let merge = [];
                // let flag = 1;
                // for(let i=0;i<n;i++){
                    // if(flag == 1){
                        // merge[i] = t1[Math.floor(i/2)];
                        // flag=2;
                    // } else {
                        // merge[i] = t2[Math.floor(i/2)];
                        // flag=1;
                    // }
                // }
                // targets = merge;
                $('#JQWC').jQCloud(targets,already_placed_targets,"place_holder",{
                    delayedMode: false,
                    afterCloudRender: ()=>{
                        $(".target").css("visibility","hidden").css('color','black');
                        $("#notification").html("Task loaded. Click the red cross to start");
                        $("#center_cross").css("cursor","pointer").off().bind("click",()=>{
                            $(".target").css("visibility","visible");
                            $("#notification").html('<label for="wordcloud_name" style="display: block;">Name(s) this word cloud:</label>');
                            $("#notification").append('<input type="text" id="wordcloud_name" required size="15">')
                            $("#notification").append('<button type="button" id="next_button">Next</button>')
                            $("#next_button").off().css("cursor","pointer")
                                .on("click",{task_method:method,topics:topics},collect_response);
                            $("#wordcloud_name").keypress(function(e){
                                    if (e.which == 13){
                                        $("#next_button").click();
                                    }
                                });
                            $("#center_cross").off().css("cursor","default")
                            startTime = new Date();
                        });
                             // ajax call
                    }
                }); // jqcloud
                //drawTargets(targets,task["flash_time"]);
            },
        dataType: "json"
    });
}

// function getTopics(){
//     var topics = new Set();
//     $(".target").each(function(index,word){
//         topics.add(word.classList[1]);
//     })
//     return topics
// }

function getMeasure(topics){ // get the mean distance and size of words for each topic
    const measurements = [];
    const cloud_center_x = $('#JQWC').width()/2.0;
    const cloud_center_y = $('#JQWC').height()/2.0;
    topics.forEach((topic)=>{
        $("."+topic).each((index,word)=>{
            x_dist = Math.abs($(word).position()["left"]+$(word).width()/2.0 - cloud_center_x);
            y_dist = Math.abs($(word).position()["top"]+$(word).height()/2.0 - cloud_center_y);
            center_dist = Math.sqrt(x_dist*x_dist + y_dist*y_dist);
            size = parseInt($(word).css("font-size"),10);
            const measure = {"topic":topic,"size":size,"center_dist":center_dist,"x_dist":x_dist,"y_dist":y_dist,"word":word}
            measurements.push(measure);
        });
    });
    return measurements;
}

function categorizeWords(topics,measurements){ //Create a 2D array, each element is an array of a single topic
    const categorized_arr = [];
    topics.forEach((topic)=>{
        const obj_arr = measurements.filter((element)=>{return element["topic"] === topic});
        categorized_arr.push(obj_arr);
    });
    return categorized_arr
}

function collect_response(event){
    // $("#next_button").off();
    let wordcloud_name_trim=$.trim($("#wordcloud_name").val());
    if(wordcloud_name_trim.length>0){
        endTime = new Date();
        const time = (endTime - startTime)/1000;
        const method = event.data.task_method;
        // const topics = getTopics();
        const topics = event.data.topics.slice(0,2); // the two real topics
        const categorized_arr = categorizeWords(topics, getMeasure(topics));
        const cloud = $("#JQWC").html();

        const topic_1 = topics[0],
              topic_2 = topics[1],
              topic_distractor = event.data.topics[2];

        // let topic_iter = topics.values();
        // const topic_2 = topic_iter.next().value,
        //       topic_1 = topic_iter.next().value;
        
        $("#notification").hide();
        // console.log($("#wordcloud_name").val());
        console.log(wordcloud_name_trim);
        $("#JQWC").children().hide();
        $("#JQWC").hide();
        // $("form#collect_response").append(`How confident are you to say that the wordcloud contains words about #${topic_1}?`)
        //                             .append('<br />1 (no such thing) <input type="range" id="topic_1_range" min="1" max="10" value="5"> 10 (contains this topic)')
        //                             .append('<br /><p>Value: <span id="topic_1_value"></span></p>')
        //                             .append(`How confident are you to say that the wordcloud contains words about #${topic_2}?`)
        //                             .append('<br />1 (no such thing) <input type="range" id="topic_2_range" min="1" max="10" value="5"> 10 (contains this topic)')
        //                             .append('<br /><p>Value: <span id="topic_2_value"></span></p>')
        //                             .append('<br /><input type="submit" value="Next" id="submit" >')
        
        // Prompt question
        let q_topic1 = $(document.createDocumentFragment())
                .append(`How confident are you to say that the wordcloud contains words about <strong> #${topic_1}? </strong> <br />`)
                .append('<input type="radio" name="topic_1_radio" value=1 required />Not Present At All <br />')
                .append('<input type="radio" name="topic_1_radio" value=2 required />Barely Present <br />')
                .append('<input type="radio" name="topic_1_radio" value=3 required />Somewhat Present <br />')
                .append('<input type="radio" name="topic_1_radio" value=4 required />Mostly Present <br />')
                .append('<input type="radio" name="topic_1_radio" value=5 required />Definitely Present <br />')
                .append('<br />'),
            q_topic2 = $(document.createDocumentFragment())
                .append(`How confident are you to say that the wordcloud contains words about <strong> #${topic_2}? </strong> <br />`)
                .append('<input type="radio" name="topic_2_radio" value=1 required />Not Present At All <br />')
                .append('<input type="radio" name="topic_2_radio" value=2 required />Barely Present <br />')
                .append('<input type="radio" name="topic_2_radio" value=3 required />Somewhat Present <br />')
                .append('<input type="radio" name="topic_2_radio" value=4 required />Mostly Present <br />')
                .append('<input type="radio" name="topic_2_radio" value=5 required />Definitely Present <br />')
                .append('<br />'),
            q_topic3 = $(document.createDocumentFragment())
                .append(`How confident are you to say that the wordcloud contains words about <strong> #${topic_distractor}? </strong> <br />`)
                .append('<input type="radio" name="topic_dis_radio" value=1 required />Not Present At All <br />')
                .append('<input type="radio" name="topic_dis_radio" value=2 required />Barely Present <br />')
                .append('<input type="radio" name="topic_dis_radio" value=3 required />Somewhat Present <br />')
                .append('<input type="radio" name="topic_dis_radio" value=4 required />Mostly Present <br />')
                .append('<input type="radio" name="topic_dis_radio" value=5 required />Definitely Present <br />')
                .append('<br />');
        let q_arr = [q_topic1,q_topic2,q_topic3];
        $("form#collect_response")
            .append(q_arr.splice(Math.floor(Math.random()*q_arr.length),1))
            .append(q_arr.splice(Math.floor(Math.random()*q_arr.length),1))
            .append(q_arr.splice(Math.floor(Math.random()*q_arr.length),1))
            .append('<input type="submit" value="Next" id="submit" >');

        
        $("#submit").keypress(function(e){
            if (e.which == 13){
                $("#submit").click();
            }
        });

        // $("#topic_1_range").on("input",function() {$("#topic_1_value")[0].innerHTML = this.value;});
        // $("#topic_2_range").on("input",function() {$("#topic_2_value")[0].innerHTML = this.value;});


        $("form#collect_response").off().on("submit",function(){
            // if($("#topic_1_value").html() != "" && $("#topic_2_value").html() != ""){
            // alert("submit button clicked!");
            $("#submit").off();


            let topic_1_value = document.querySelector('input[name="topic_1_radio"]:checked').value,
                topic_2_value = document.querySelector('input[name="topic_2_radio"]:checked').value,
                topic_dis_value = document.querySelector('input[name="topic_dis_radio"]:checked').value;
            const response = [topic_1_value,topic_2_value,topic_dis_value];

            $.ajax({
                type: 'POST',
                url: $SCRIPT_ROOT + "/_postTopicMeasurements",
                data: JSON.stringify({ 
                    "method": method, 
                    "arr": categorized_arr, 
                    "cloud": cloud, 
                    "time": time,
                    "distractor": topic_distractor,
                    "response": response,
                    "wordcloud_name": wordcloud_name_trim}),
                contentType: "application/json",
                success: function (data) {
                    console.log(data);
                    nextTask()
                },
                error: function (error) {
                    console.log(error);
                }
            });
            return false
            // }
            // return false
        }); //form submit
    }
}

// function foo(){
//     // validate the response information

//     alert("submit onclick!")
// }

// function drawTargets(target_array,flash_time){
//     $('#JQWC').addClass('jqcloud');
//     var cloud_center_x = $('#JQWC').width()/2.0;
//     var cloud_center_y = $('#JQWC').height()/2.0;
//     target_array.forEach((word,index,array)=>{
//         var word_span = $('<span>').attr('class',word.html['class'])
//                                     .css("visibility","hidden")
//                                     .append(word.text)
//                                     .bind("click",function(){console.log($(this))})
//                                     .bind("mouseover",function(){this.style.cursor='default'});
//         $('#JQWC').append(word_span);

//         var fontsize = word['weight'];
//         word_span[0].style.fontSize = fontsize + 'px';

//         var radius = word['radius'];
//         var width = word_span.width();
//         var height = word_span.height();
//         var alpha = 2 * Math.PI * Math.random();
//         var x = radius * Math.cos(alpha);
//         var y = radius * Math.sin(alpha);
//         var left = cloud_center_x - width / 2.0 - x;
//         var top = cloud_center_y - height / 2.0 - y;
//         word_span[0].style.position = "absolute";
//         word_span[0].style.left = left + "px";
//         word_span[0].style.top = top + "px";
//         word_span[0].style.color = 'black';

//         var hitTest = function (elem, other_elems) {
//             // Pairwise overlap detection
//             var overlapping = function (a, b) {
//                 if (Math.abs(2.0 * a.offsetLeft + a.offsetWidth - 2.0 * b.offsetLeft - b.offsetWidth) < a.offsetWidth + b.offsetWidth) {
//                     if (Math.abs(2.0 * a.offsetTop + a.offsetHeight - 2.0 * b.offsetTop - b.offsetHeight) < a.offsetHeight + b.offsetHeight) {
//                         return true;
//                     }
//                 }
//                 return false;
//             };
//             var i = 0;
//             // Check elements for overlap one by one, stop and return false as soon as an overlap is found
//             for (i = 0; i < other_elems.length; i++) {
//                 if (overlapping(elem, other_elems[i])) {
//                     return true;
//                 }
//             }
//             return false;
//         };

//         do {
//             var overlap = hitTest(word_span[0], already_placed_targets);
//             if (overlap === true) {
//                 var alpha = 2 * Math.PI * Math.random();
//                 var x = radius * Math.cos(alpha);
//                 var y = radius * Math.sin(alpha);
//                 var left = cloud_center_x - width / 2.0 - x;
//                 var top = cloud_center_y - height / 2.0 - y;
//                 word_span[0].style.left = left + "px";
//                 word_span[0].style.top = top + "px";
//             }
//         } while (overlap === true)
//         already_placed_targets.push(word_span[0]);
//     });
//     $("#notification").html("Task loaded. Click the red cross to start");
//     $("#center_cross").css("cursor","pointer").off()
//         .bind("click",()=>{
//             $(".target").css("visibility","visible");
//             $("#center_cross").css("cursor","default").off();
//             startTime = new Date();
//             setTimeout(resp_window,flash_time);
//             endTime = new Date();
//         });   
// }



// show the cloud
// start the timer



function nextTask() {
    document.getElementById('JQWC').innerHTML = '<span id="center_cross" style="position: absolute;top: 480px;left: 487.0156px;font-size: 30px;color: red;">&#10011;</span>';
    $("form#collect_response").html('');
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