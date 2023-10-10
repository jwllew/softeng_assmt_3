// Dynamic page format
$.ajax({
    url: "/api/modules",
    type: "GET",
    /*headers: {
        "Authorization":  "Bearer " + token
      },*/
    dataType: "json",
    success: function(data) {
        addSubjects(data.items)
    }
    /*error: function (xhr, ajaxOptions, thrownError) {
        alert(xhr.status);
        alert(thrownError);
      }*/
});

function addSubjects(data){
    let select = $('select#module')
    
    for(let i = 0 ; i < data.length ; i++){
        let option = $('<option value="' + data[i].id + '">' + data[i].name + '</option>');
        
        select.append(option);
    }
}

$(document).ready(function() {
    
    /*$("#message-btn").click(function() {
        console.log(btoa("Louis:gilder"))
        var data = {
            name: $(".question_name").val()
        }
        $.ajax({
            url: "/api/tokens",
            type: "POST",
            headers: {
                "Authorization":  "Basic TG91aXM6Z2lsZGVy"
              },
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: "json",
            success: function(data) {
                $(".message-result").html(data.token);
            }
        });
    });*/

    $("#add").click(function() {
        var lastField = $(".blank-answers div:last");
        var intId = (lastField && lastField.length && +lastField.data("idx") + 1) || 1;

        addBlankInput(intId);

        var txtarea = $(".text-input")
        var caretPos = txtarea[0].selectionStart;
        var txtToAdd = " (# Blank " + intId + " #) ";

        if( caretPos == 0 ){
            txtarea.val( (i, text) => text + txtToAdd)
        } else {
            txtarea.val((i, text) => text.substring(0, caretPos) + txtToAdd + text.substring(caretPos) );
        }
        var newMark = parseInt($("#marks").text())  + 1;
        $("#marks").text(newMark);
    });
});

function addBlankInput(intId){
    var fieldWrapper = $('<div class="blank" id="field' + intId + '"/>');
    fieldWrapper.data("idx", intId);
    var fLabel = $('<label>Blank ' + intId + ' : </label>');
    var fName = $('<input type="text" class="blank-input" id="blank_' + intId + '" required/>');
    var fMark = $('<input type="number" class="blank-mark-input" id="blank_mark_' + intId + '" min="1" max="10" value="1"/>');
    var removeButton = $('<a class="remove-blank"><span>&#128465;</span></a>');

    removeButton.click(function() {
        let remove_id = $(this).parent().attr("id").match(/\d+/g)[0];
        let remove_txt = "(# Blank " + remove_id + " #)";
        let remove_mark = $(this).siblings(".blank-mark-input").val();
        let newMark = parseInt($("#marks").text()) - remove_mark;

        $("#marks").text(newMark);
        $(".text-input").val( (i, text) => text.replace(remove_txt, "") )
        $(this).parent().remove();
    });

    fieldWrapper.append(fLabel);
    fieldWrapper.append(fName);
    fieldWrapper.append(fMark);
    fieldWrapper.append(removeButton);
    $(".blank-answers").append(fieldWrapper);

    return fieldWrapper;
}

// Updates the total marks when changed blank mark
$(".blank-answers").on('change', function() {
    var marks = $(".blank-mark-input");
    var updateMark = 0;
    for(let i = 0 ; i < marks.length ; i++){
        updateMark += parseInt(marks[i].value);
    }
    $('#marks').text(updateMark);
});

// Used to get the data from the form
function formatData() {
    event.preventDefault();

    var data = {
        'question': $(".question-input").val(),
        'difficulty': +$("#difficulty").val(),
        'total_marks': +$("#marks").text(),
        'lines': $(".text-input").val().split("\n"),
        'answers':{},
        'feedback': $("#feedback").val(),
        'feedforward': $("#feedforward").val(),
        'author_id': +$(".user-id").html(),
        'module_id': +$("#module").val()
    }

    

    var blanks = $(".blank-input");
    var blanksMark = $(".blank-mark-input");

    data['num_blanks'] = blanks.length;
    
    for(let i = 0 ; i < blanks.length ; i++){
        data.answers[blanks[i].id] = [blanks[i].value, blanksMark[i].value];
    };

    let blank_inputs = $(".text-input").val().match(/(\(# Blank )(\d+)( #\))/g);
    let blank_keys = Object.keys(data.answers);
    console.log(blank_inputs)
    if(blank_keys == null){
        return errorThrow("There are no blanks");
    }

    if(blank_inputs.length == blank_keys.length){
        for(let i = 0 ; i < blank_inputs.length ; i++){
            let blank_num = blank_inputs[i].match(/[0-9]+/g)

            if(blank_num.length != 1){
                return errorThrow("One of the blanks in the textarea has multiple numbers");
            }
                
            let key = 'blank_' + blank_num[0];
            
            if(!data.answers.hasOwnProperty(key)){
                return errorThrow("The blank's numbers don't match up")
            }
        }
    } else{
        return errorThrow("The number of blanks in the textarea doesn't match the amount inputted")
    }

    data.lines = JSON.stringify(data.lines);
    data.answers = JSON.stringify(data.answers);
    console.log(data)
    return data;
}

// Throws erros in a readable way
function errorThrow(error){
    var wrapper = $('<div class="error popup"/>');
    var message = $('<p>Error: ' + error + '</p>');
    var removeButton = $('<a class="remove-error"><span>&#10005;</span></a>');

    removeButton.click(function() {
        $(this).parent().remove();
    });

    wrapper.append(message);
    wrapper.append(removeButton);
    $(".save_button").append(wrapper);

    return false;
}

// Create function
function createQuestion(id = '') {
    var data = formatData();

    if(id != ''){
        data['assessment_id'] = id
    }

    if(data == false){
        return false;
    }
    console.log(data)
    var token = $(".user-token").html();
    
    $.ajax({
        url: "/api/question_one",
        type: "POST",
        headers: {
            "Authorization":  "Bearer " + token
          },
        contentType: "application/json",
        data: JSON.stringify(data),
        dataType: "json",
        success: function(data) {
            window.location.replace("http://127.0.0.1:5000/question_one/" + data.id);
        }
        /*error: function (xhr, ajaxOptions, thrownError) {
            alert(xhr.status);
            alert(thrownError);
          }*/
    });

    
}

// Edit functions
function editQuestion(id){
    var token = $(".user-token").html();
    
    $.ajax({
        url: "/api/question_one/" + id,
        type: "GET",
        headers: {
            "Authorization":  "Bearer " + token
          },
        dataType: "json",
        success: function(data) {
            formatEdit(data);
        }
    });
}

function formatEdit(data){
    $('input.question-input').val(data.question);
    console.log(data)

    var lines = data.lines.join('\n');
    $('textarea.text-input').val(lines);

    for(var key in data.answers){
        let blank_num = key.match(/[0-9]+/g)[0];
        let elem = addBlankInput(blank_num);
        elem.children('input.blank-input').val(data.answers[key][0]);
        elem.children('input.blank-mark-input').val(data.answers[key][1]);
    }

    $('select#difficulty').val(data.difficulty);
    $('a#marks').text(data.total_marks);
    $('select#subject').val(data.subject_id);

    var deleteButton = $('<button id="delete" type="button">Delete question</button>');

    deleteButton.click(function() {
        deleteQuestion(data.id)
    });

    $('div.save_button').append(deleteButton)
}

function saveEdit(id) {
    
    var data = formatData();

    if(data == false){
        return false;
    }
    
    var token = $(".user-token").html();
    
    $.ajax({
        url: "/api/question_one/" + id,
        type: "PUT",
        headers: {
            "Authorization":  "Bearer " + token
          },
        contentType: "application/json",
        data: JSON.stringify(data),
        dataType: "json",
        success: function(data, textStatus, request) {
            window.location.replace("http://127.0.0.1:5000/question_one/" + data.id);
        }
        /*error: function (xhr, ajaxOptions, thrownError) {
            alert(xhr.status);
            alert(thrownError);
          }*/
    });
}

function deleteQuestion(id){
    var wrapper = $('<div class="delete_question popup"/>');
    var message = $('<p>Are you sure you want to delete this question?</p>');
    var deleteQuesition = $('<button>Yes</button>');
    var close = $('<button>No</button>');

    close.click(function() {
        $(this).parent().remove();
    });

    deleteQuesition.click(function() {
        $.ajax({
            url: "/api/question_one/" + id,
            type: "DELETE",
            /*headers: {
                "Authorization":  "Bearer " + token
              },*/
            dataType: "json",
            success: function(data, textStatus, request) {
                window.location.replace("http://127.0.0.1:5000/question_one/create");
            }
            /*error: function (xhr, ajaxOptions, thrownError) {
                alert(xhr.status);
                alert(thrownError);
              }*/
        });
    })

    wrapper.append(message);
    wrapper.append(deleteQuesition);
    wrapper.append(close);
    $(".save_button").append(wrapper);

    return false;
}


var question_id = $('div.question-id').html();

if(question_id != ''){editQuestion(question_id)}