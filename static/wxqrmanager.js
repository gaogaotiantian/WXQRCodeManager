// List groups
getGroupDom = function(data) {
    var $template = $('#card-tmpl').clone();
    $template.removeClass('d-none');
    $template.removeAttr('id');
    if (data.id) {
        $template.find('.qrcode-img').attr('qrcode-id', data.id.toString());
    }
    if (data.name) {
        $template.find('.card-title').text(data.name);
        $template.find('.qrcode-img').attr('qrcode-name', data.name);
    }
    if (data.tags) {
        for (idx in data.tags) {
            $template.find('.card-badges').append($('<a>').attr('href', '#').addClass("badge badge-primary mr-1 badge-add").text(data.tags[idx]));
        }
    }
    if (data.description) {
        $template.find('.card-text').text(data.description);
        $template.find('.qrcode-img').attr('qrcode-description', data.description);
    }
    return $template
}

listPage = function(data = {}) {
    $.ajax({
        url: '/api/v1/groups',
        type: 'get',
        data: data,
        success: function(d, st, xhr) {
            $('#group-list-div').empty();
            for (idx in d.results) {
                $('#group-list-div').append(getGroupDom(d.results[idx]));
            }
            
        }
    })
}

refreshTags = function() {
    $('#tags-list-div').empty();
    var tags = $('#tags-list-div').data("tags").split(' ');
    for (var idx in tags) {
        var tag = tags[idx];
        if (tag != "") {
            $('#tags-list-div').append($('<a>').attr('href', '#').addClass("badge badge-primary mr-1 badge-remove").text(tag+" ").append($('<i>').addClass("fas fa-times")));
        }
    }
    listPage(data = {"keywords":$('#tags-list-div').data("tags")});
}

// Upload functions
uploadQrcode = function() {
    $.ajax({
        url: '/api/v1/groups',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({
            "id":$('#upload-data-div').data("id"),
            "name":$('#upload-data-name-input').val(),
            "description":$('#upload-data-description-input').val(),
            "tags":$('#upload-data-tags-input').val()
        }),
        success: function(d, st, xhr) {
            $('#upload-file-input').val('');
            $('#upload-file-label').text('选择文件');
            $('#upload-data-div').hide();
            $('#upload-img-preview').hide();
            $('#upload-success-div').hide();
            $('#upload-error-div').hide();
            $('#upload-modal').modal('hide');
        }
    });
};

$(function() {
    $('#upload-file-input').change(function() {
        var fileName = $('#upload-file-input')[0].files[0].name;
        if (fileName) {
            $('#upload-file-label').text(fileName);
            var fdata = new FormData($("#upload-form")[0])
            $.ajax({
                url: '/api/v1/qrcode',
                type: 'post',
                data: fdata,
                processData: false,
                contentType: false,
                success: function(d, st, xhr) {
                    $('#upload-data-div').data("id", d.id)
                    $('#upload-img-preview').attr('src', '/api/v1/qrcode?id=1');
                    $('#upload-img-preview').show();
                    $('#upload-data-div').show();
                    $('#upload-error-div').hide();
                    $('#upload-success-div').show();
                    $('#upload-success-div').text("上传成功！");
                    $('#upload-data-name-input').val(d.name);
                    $('#upload-data-description-input').val(d.description);
                    $('#upload-data-tags-input').val(d.tags.join(" "));
                    $('#upload-confirm-button').removeClass("disabled");
                },
                error: function(d, st, xhr) {
                    $('#upload-img-preview').hide();
                    $('#upload-data-div').hide();
                    $('#upload-success-div').hide();
                    $('#upload-error-div').show();
                    $('#upload-error-div').text(d.responseJSON.err_msg);
                    $('#upload-confirm-button').addClass("disabled");
                }
            });
        } else {
            $('#upload-file-label').text("选择文件");
        }
    });

    $('#download_button').click(function(){
        $('#download_img').attr('src','/api/v1/qrcode?id='+$('#download_text').val());
    });

    $('#search_button').click(function(){
        listPage(data = {"keywords":$('#search_text').val()});
    });

    $('#upload-confirm-button').click(function(){
        uploadQrcode();
    });

    $('#tags-list-div').data("tags", "");

    $('body').on("click", "a.badge.badge-add", function() {
        var tags = $('#tags-list-div').data("tags").split(' ');
        if (tags[0] == "") {
            $('#tags-list-div').data("tags", $(this).text());
        } else if (tags.indexOf($(this).text()) < 0) {
            tags.push($(this).text());
            console.log(tags)
            console.log(tags.join(' '))
            $('#tags-list-div').data("tags", tags.join(' '));
        }
        refreshTags();
    });

    $('body').on("click", "a.badge.badge-remove", function() {
        var tags = $('#tags-list-div').data("tags").split(' ');
        var idx = tags.indexOf($(this).text().split(' ')[0]);
        if (idx > -1) {
            tags.splice(idx, 1);
            $('#tags-list-div').data("tags", tags.join(' '));
            refreshTags();
        }
    });

    $('body').on('click', 'img.qrcode-img', function() {
        $('#display-group-name').text($(this).attr('qrcode-name'));
        $('#display-group-description').text($(this).attr('qrcode-description'))
        $('#display-img-preview').attr('src', "/api/v1/qrcode?id=" + $(this).attr('qrcode-id'));
        $('#display-img-download').attr('href', "/api/v1/qrcode?id=" + $(this).attr('qrcode-id'));
        $('#display-modal').modal("show");
    });
    listPage();
})
