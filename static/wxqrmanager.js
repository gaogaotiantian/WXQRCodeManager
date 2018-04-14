$(function() {
    $('#upload-file-input').change(function() {
        var fileName = $('#upload-file-input')[0].files[0].name;
        console.log(fileName);
        if (fileName) {
            $('#upload-file-label').text(fileName);
        } else {
            $('#upload-file-label').text("选择文件");
        }
    });

    $('#upload_form').submit(function(e) {
        e.preventDefault();
        $.ajax({
            url: '/api/v1/qrcode',
            type: 'post',
            data: new FormData(this),
            processData: false,
            contentType: false,
            success: function(d, st, xhr) {
                $('#upload_result').empty();
                $('#upload_result').append($('<span>').text('Success!')).append('<br>');
                $('#upload_result').append($('<span>').text(d)).append('<br>');
                $('#upload_result').append($('<span>').text(st)).append('<br>');
            },
            error: function(d, st, xhr) {
                $('#upload_result').empty();
                $('#upload_result').append($('<span>').text('Error!')).append('<br>');
                $('#upload_result').append($('<span>').text(d)).append('<br>');
                $('#upload_result').append($('<span>').text(st)).append('<br>');
            }
        });
    });

    $('#download_button').click(function(){
        $('#download_img').attr('src','/api/v1/qrcode?id='+$('#download_text').val());
    });

    $('#search_button').click(function(){
        $.ajax({
            url: '/api/v1/groups',
            type: 'get',
            data: {'keywords':$('#search_text').val()},
            success: function(d, st, xhr) {
                $('#search_result').empty();
                $('#search_result').append($('<span>').text('Success!')).append('<br>');
                $('#search_result').append($('<span>').text(d)).append('<br>');
                $('#search_result').append($('<span>').text(st)).append('<br>');
            },
            error: function(d, st, xhr) {
                $('#search_result').empty();
                $('#search_result').append($('<span>').text('Error!')).append('<br>');
                $('#search_result').append($('<span>').text(d)).append('<br>');
                $('#search_result').append($('<span>').text(st)).append('<br>');
            }
        });
    });
})
