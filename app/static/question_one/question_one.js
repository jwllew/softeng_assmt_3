// Gets a single question by id
function getQuestion(id, question_num){
    var token = $(".user-token").html();
    
    $.ajax({
        url: "/api/question_one/" + id,
        type: "GET",
        headers: {
            "Authorization":  "Bearer " + token
          },
        dataType: "json",
        success: function(data) {
            formatQuestion(data, question_num)
        }
    });
}

// Uses the API to get all questions and uses 'formatQuestion()' to put on the page
function getAllQuestions(api){
    var token = $(".user-token").html();

    $.ajax({
        url: api,
        type: "GET",
        headers: {
            "Authorization":  "Bearer " + token
          },
        dataType: "json",
        success: function(data) {
            for(let i = 0 ; i < data.items.length ; i++)
            formatQuestion(data.items[i], i + 1)
        }
    });
}

// Formates the question on the page with the question nums
function formatQuestion(data, question_num){
    var question_wrapper = $('<form id="question_one_' + data.id + '" onsubmit="markQuestion(' + data.id + ')" class="container"/>');
    var question = $('<div class="form-group question"/>');
    var buttons = $('<div class="form-group buttons"/>');
    
    var question_title = $('<h2>' + question_num + ') ' + data.question + '</h2>');
    question.append(question_title);

    var text = data.lines.toString();
    
    for(var key in data.answers){
        let blank_num = key.match(/[0-9]+/g)[0];
        text = text.replace('(# Blank ' + blank_num + ' #)', '<input type="text" id="blank_' + blank_num + '" class="answer" required/> <b>(' + data.answers[key][1] + ')</b>');
    }

    var lines = text.split(',')
    
    for(let i = 0 ; i < lines.length ; i++){
        let white_space = lines[i].search(/[^ ]/g)
        lines[i] = '&nbsp '.repeat(white_space) + lines[i]
        question.append($('<p>' + lines[i] + '</p>'));
    }

    buttons.append($('<p>Difficulty: ' + data.difficulty + '/10</p>'))
    buttons.append($('<p>(' + data.total_marks + ')</p>'))
    buttons.append($('<button type="submit" id="mark">Mark</button>'))

    question_wrapper.append(question)
    question_wrapper.append(buttons)

    $('div#' + data.id + '.question-one-insert').replaceWith(question_wrapper);
}

// Calls the API to mark the question and then uses 'returnMark()' to format the page
function markQuestion(id) {
    event.preventDefault();

    var answers = $("#question_one_" + id).find('.answer');

    var data = {
        user_id: 1,
        assessment_id: 0,
        answers: {}
    };

    for(let i = 0 ; i < answers.length ; i++){
        data.answers[answers[i].id] = answers[i].value;
    }
    console.log(data)
    var token = $(".user-token").html();
    
    $.ajax({
        url: "/api/question_one/" + id + "/mark",
        type: "POST",
        /*headers: {
            "Authorization":  "Bearer " + token
          },*/
        contentType: "application/json",
        data: JSON.stringify(data),
        dataType: "json",
        success: function(data) {
            returnMarkFormative(data, id)
        }
        /*error: function (xhr, ajaxOptions, thrownError) {
            alert(xhr.status);
            alert(thrownError);
          }*/
    });
}

// Marks the question
function returnMarkFormative(data, id){
    var answers = $("#question_one_" + id);
    console.log(data)

    for(var key in data.question_mark){
        let val = answers.find('#' + key).val();
        let result;

        if(data.question_mark[key] != 0){
            result = $('<a class="result right">' + val + '</a>');
        } else {
            result = $('<a class="result wrong">' + val + '</a><a class="result correct-ans">' + data.answer[key][0] + '</a>');
        }

        answers.find('#' + key).replaceWith(result);
    }
    answers.find('#mark').replaceWith($('<p>You got ' + data.correct + '/' + data.num_blanks + ' correct and ' + data.mark + '/' + data.total_marks + ' marks</p>' ));
}

function returnMarkSummative(data, id){
    var answers = $("#question_one_" + id);

    for(var key in data.question_mark){
        let val = answers.find('#' + key).val();
        let result;

        result = $('<a class="result submitted">' + val + '</a>');

        answers.find('#' + key).replaceWith(result);
    }
}

let questions = $('.question-one-insert');

for(let i = 0 ; i < questions.length ; i++){
    getQuestion(questions[i].id, i+1)
}