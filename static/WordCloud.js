/*
 * WordCloud.js
 * Muyang Shi, 25 June 2019
 *
 * Question: how to embed the Jason Davie word cloud into here
 */

// initialize();

function initialize() {
    var element = document.getElementById('Button_getWC');
    if (element) {
        element.onclick = onGetWCButtonClicked;
    }
}

function getBaseUrl() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + '5000';
    return baseURL
}

function onGetWCButtonClicked() {
    var numberOfWords = document.getElementById('numberOfWords').value;
    var url = getBaseUrl + '/' + numberOfWords;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(wordList) {
        // Build the table body.
        var tableBody = '';
        for (var k = 0; k < wordList.length; k++) {
            tableBody += '<tr>';

            tableBody += '<td>' + wordList[k] + '</td>';

            tableBody += '</tr>';
        }

        // Put the table body we just built inside the table that's already on the page.
        var Cloud_Table = document.getElementById('Cloud_Table');
        if (Cloud_Table) {
            Cloud_Table.innerHTML = tableBody;
        }
    })
}