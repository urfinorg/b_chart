"use strict";


var g_timer = setInterval(onTimer, 1500);
var tick_count = 0;
var last_message_id = -1;

function onTimer(){
    tick_count = tick_count + 1;

    let form_data = new FormData();
    form_data.append("form_id", "get_message");
    form_data.append('last_message_id', 'last_message_id');

    ajax_param['data'] = form_data;

    $.ajax(ajax_param)
        .done( function(msg){
            if ((last_message_id != msg['message_id']) && (msg['err_code'] == 0)) {
                last_message_id = msg['message_id'];
                $('#message_area').append( msg['username'] + ':' + msg['msg'] +  "\n" );
            }
        });

    //$("#div_console").append("onTimer: " + tick_count);
}



$('.sync_form').on('submit', function(e) {
    e.preventDefault();
    let client_validation = true;

    let form_data = getFormData_FD($(this));
    ajax_param['data'] = form_data;

    if ( $(this).attr('id') == 'reg_form'){
        client_validation = valid_password(form_data);
    }

    if (client_validation) {
        $.ajax(ajax_param)
            .done( function(msg){

                if (msg['err_code'] == 0 ) {
                    username = msg['username'];
                    is_auth_user = 1;
                    show_is_auth_block();
                }

                var tmp_token = msg['csrf'];
                if (tmp_token != null){
                    //console.log('!!' + tmp_token)
                    ajax_param['headers'] =  { "X-CSRFToken": tmp_token };
                    jQuery("[name=csrfmiddlewaretoken]").val(tmp_token);
                }
                // DEBUG PURPOSE ONLY
                $('#div_console').append( '<p>' + 'ajax return(DEBUG PURPOSE ONLY): ' + msg  + "  "
                    +   msg['err_code'] + " "
                    + tmp_token +"   " + msg['msg']  +'</p>' );

            } );
    }

    return false;
});

$('#message_form').on('submit', function(e) {
    e.preventDefault();
    let sending_msg = $('#sending_message').val();
    if (sending_msg != "") {
        let f_data = new FormData();
        f_data.append("form_id", "message_form");
        f_data.append("msg", sending_msg);
        //$('#div_console').append('<p> inside ' + JSON.stringify(f_data) + f_data['msg'] + '</p>');
        ajax_param['data'] = f_data;
        $.ajax(ajax_param).done( function(msg){
            if (msg['err_code'] != 0 ) {
                $('#div_console').append('<p> ' + 'ajax return: ' +
                    msg['err_code'] + " " + msg['msg'] + '</p>');
                } else {
                    $('#div_console').append('<p> Message was accepted by server </p>');
                    }
        });
    }
    return false;
});

//var csrf_token = jQuery("[name=csrfmiddlewaretoken]").val();

var ajax_param = {
    headers: { "X-CSRFToken": jQuery("[name=csrfmiddlewaretoken]").val() },
    method: "POST",
    url: "../api",
    cache: false,
    contentType: false,
    processData: false,
};


if (is_auth_user){
    show_is_auth_block();
} else {
    show_login_form();
}


$('#show_reg_form').on('click', function(e) {
    e.preventDefault();
    show_registration_form();
    return false;
});

$('#show_login_form').on('click', function(e) {
    e.preventDefault();
    show_login_form();
    return false;
});


$('#logout_link').on('click', function(e) {
    e.preventDefault();
    var form_data = new FormData();
    form_data.append('form_id', 'logout' ) ;
    ajax_param['data'] = form_data;
    $.ajax(ajax_param).done( function(msg){
                //console.log(msg);
            });
    show_login_form();
    return false;
});

function getFormData_FD(form){
    let unindexed_array = form.serializeArray();
    let result = new FormData();
    $.map(unindexed_array, function(n, i){
        result.append(n['name'], n['value']);
    });
    result.append('form_id', form.attr('id') ) ;
    return result;
}

function valid_password(form_data) {
    var client_validation = true;
    $('#reg_form_validation').html('');
    if ( form_data.get('password') != form_data.get('confirm_password') ){
        client_validation = false;
        $('#reg_form_validation').html('<b>password and confirm_password does not match, ' +
                'you can stay empty pass, and it will generate automatic</b>');
        }
    return client_validation;
}

//*** show functions ********************

function show_login_form() {
    $('.sync_form').hide();
    $('#login_form').show();
}

function show_registration_form() {
    $('.sync_form').hide();
    $('#reg_form').show();
}

function show_is_auth_block() {
    $('.sync_form').hide();
    $('#is_auth_block').show();
    $('#label_user_name').html(username);
}



// function getFormData(form){
//     var unindexed_array = form.serializeArray();
//     var indexed_array = {};
//     $.map(unindexed_array, function(n, i){
//         indexed_array[n['name']] = n['value'];
//     });
//     indexed_array['form_id'] = form.attr('id');
//     return indexed_array;
// }

