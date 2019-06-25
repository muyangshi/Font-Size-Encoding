/*
 * WordCloud.js
 * Muyang Shi, 25 June 2019
 *
 * Question: how to embed the Jason Davie word cloud into here
 */

initialize();

function initialize() {
    var getWordList = document.getElementById('Button_getWordList');
    if (getWordList) {
        getWordList.onclick = onGetWordListButtonClicked;
    }
    var getWordCloud = document.getElementById('Button_getWordCloud')
    if (getWordCloud) {
        getWordCloud.onclick = onGetWordCloudButtonClicked;
    }
}

function getBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + '5000';
    return baseURL
}

var words = [];

function onGetWordListButtonClicked() {
    var numberOfWords = document.getElementById('numberOfWords').value;
    var url = getBaseURL() + '/randomStim/' + numberOfWords;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(wordList) {
        for (var k = 0; k < wordList.length; k++) {
            words.push(wordList[k]);
        }
    });
}
function onGetWordCloudButtonClicked() {
    // var numberOfWords = document.getElementById('numberOfWords').value;
    // var url = getBaseURL() + '/randomStim/' + numberOfWords;
    // fetch(url, {method: 'get'})
    // .then((response) => response.json())
    // .then(function(wordList) {
    //     for (var k = 0; k < wordList.length; k++) {
    //         words.push(wordList[k]);
    //     }
    // });    

    var svg = d3.select('#WordCloud')
    words = words.map(function(d) {
        return {text: d, size: 10 + Math.random() * 90};
    });
    var cloudLayout = d3.layout.cloud()
        .size([960, 500])
        .words(words)
        //.overflow(true) NOTE: this is not part of the d3
        .padding(5)
        .rotate(0)
        .spiral('archimedean')
        .font('Impact')
        .fontSize(function (d) { return d.size; })
        .on('end', draw);
    // Draw function for building the SVG
    function draw(words) {
        svg
            .selectAll(".cloudWord")
            .data(words)
            .enter().append("text")
            .attr('class', 'cloudWord')
            .style("font-size", function (d) {
                return d.size + "px"; // NOTE: this line uses the UPDATED size
            })
            .style("font-family", "Impact")
            //.style(“fill”, function(d, i) { return fillFunc(i); })
            .style('fill', 'BLUE')
            .attr("text-anchor", "middle")
            .attr("transform", function (d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text(function (d) {
                return d.text;
            });
    }
    cloudLayout.start();
}