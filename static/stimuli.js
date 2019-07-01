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

function onStartButtonClicked() {
    var num = 15; //somthing to be read from an Array, that is from the CSV

    $.ajax({
        url: '/randomStim/'+ num,
        // data: data,
        success: 
            function(data){
                //forming data
                formed_data = data.map(function(word) {
                    return { 
                        text: word, 
                        weight: 10 + Math.random() * 90,
                        html: {"class": "CloudWord"}
                        // handlers: { click: function() { alert("I was clicked!"); } }
                    };
                });
                console.log(formed_data)
                words = formed_data;
                createCloud();
            },
        dataType: "json"
    });
}

function alertData(){
    console.log(words)
}





function getBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + '5000';
    return baseURL
}

var words = [];

function onGetWordListButtonClicked() {
    var numberOfWords = document.getElementById('numberOfWords').value;
    var url = '/randomStim/' + numberOfWords;

    fetch(url, {method: 'get'})
    
    .then((response) => response.json())

    .then(function(wordList) {
        for (var k = 0; k < wordList.length; k++) {
            words.push(wordList[k]);
        }
    })



    // onGetJQWCButtonClicked(createCloud);

}


function createCloud() {
    console.log(words)
    $("#JQWC").jQCloud(words, {
        afterCloudRender: function() {  //click and gain data
            var container = document.getElementById("JQWC");
            var containerSize = $(".jqcloud").css(['width','height']);
            var numberOfCloudWords = container.childElementCount;
            var theCloud = container.innerHTML;
            
            $(".CloudWord").click(function() {
                var wordPosition = $(this).css(["left","top"]);
                
                var word_data = {
                    "container size": containerSize,
                    "word": $(this)[0].innerHTML, //the word itself, but why $(this)[0]
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
                        alert('success!');
                        console.log(response);
                    },
                    error: function(error) {
                        alert('error saving data');
                        console.log(error);
                    }
                });

            }); 
        }
    });
}