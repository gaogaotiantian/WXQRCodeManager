// Global variables
var qrcodeView = "list";
var qrcodeData = {};

// List groups
getGroupDom = function(data) {
    if (qrcodeView === "list") {
        var $template = $('#card-list-tmpl').clone();
    } else if (qrcodeView === "block") {
        var $template = $('#card-block-tmpl').clone();
    }
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
        if (data.description.length > 30) {
            $template.find('.card-text').text(data.description.substring(0, 30) + "…… ");
            $template.find('.card-text').append($('<a>').attr('href', '#/').text("展开").css("font-weight", "bolder").click(function() {
                $template.find('.card-text').text(data.description);
                adjustCardsHeight();
            }));
        } else {
            $template.find('.card-text').text(data.description);
        }
        $template.find('.qrcode-img').attr('qrcode-description', data.description);
    } else {
        $template.find('.qrcode-img').attr('qrcode-description', "");
    }

    if (data.image) {
        $template.find('.qrcode-img').attr('src', 'data:image/png;base64, '+data.image);
    }

    if (data.read >= 0) {
        $template.find('.read-time-span').text(data.read);
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

            if (d.results.length > 0) {
                displayQRCode(d.results);

                $('#group-list-div').data('args', JSON.stringify(data));
                $('#group-list-div').data('offset', d.results.length);
                if ($(document).height() <= $(window).height()) {
                    var finish = function(resultNum) {
                        if (resultNum > 0 && $(document).height() <= $(window).height()) {
                            appendPage(finish);
                        }
                    };
                    appendPage(finish)
                }
            } else {
                $('#group-list-div').text("We cannot find any QR code with tag \"" + data.keywords + "\".");
            }
        }
    })
}

appendPage = function(finish) {
    var data = JSON.parse($('#group-list-div').data('args'));
    data['offset'] = $('#group-list-div').data('offset');
    if ($(document).width() >= 576) {
        data['limit'] = 12;
    } else {
        data['limit'] = 5;
    }
    $.ajax({
        url: '/api/v1/groups',
        type: 'get',
        data: data,
        success: function(d, st, xhr) {
            displayQRCode(d.results);

            $('#group-list-div').data('offset', data['offset'] + d.results.length);
            if (finish) {
                finish(d.results.length);
            }
        }
    })
}

displayQRCode = function(results) {
    if (qrcodeView === "list") {
        var cardsPerRow = 3;
    } else if (qrcodeView === "block") {
        var cardsPerRow = 4;
    }

    for (idx in results) {
        if ($(window).width() >= 768 ) {
            if (idx % cardsPerRow === 0) {
                if (idx > 0) {
                    var seperator = $(document.createElement('hr')).addClass('bs-docs-separator');
                    $('#group-list-div').append(seperator)
                }
                var tempRow = $(document.createElement('div')).addClass('row cardWrapper');
                $('#group-list-div').append(tempRow);
            }
            var tempCol = $(document.createElement('div'));
            if (qrcodeView === "list") {
                tempCol.addClass('col-12 col-md-4');
            } else if (qrcodeView === "block") {
                tempCol.addClass('col-6 col-md-3');
            }
            tempCol.append(getGroupDom(results[idx]));
            $('#group-list-div').find($('.cardWrapper:last')).append(tempCol);
        } else {
            qrcodeView = "list";
            $('#group-list-div').append(getGroupDom(results[idx]));
        }

        adjustCardsHeight();
    }
}

adjustCardsHeight = function() {
    $('#group-list-div').find($('.cardWrapper')).each(function() {
        var cards = $(this).children().find($('.card'));

        // remove the previous setted height
        cards.each(function() {
            $(this).css('height', 'auto');
        });

        var maxHeight = 0;
        cards.each(function() {
            if ($(this).height() > maxHeight) {
                maxHeight = $(this).height();
            }
        });
        cards.height(maxHeight);
    });
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
    qrcodeData = {"tags":$('#tags-list-div').data("tags")};
    listPage(qrcodeData);
}

// Upload functions
resetUploadDom = function() {
    $('#upload-file-input').val('');
    $('#upload-file-label').text('选择文件');
    $('#upload-data-div').hide();
    $('#upload-img-preview').hide();
    $('#upload-success-div').hide();
    $('#upload-error-div').hide();
    $('#upload-confirm-button').addClass("disabled");
    $('#upload-delete-button').addClass("disabled");
}

uploadQrcode = function() {
    $.ajax({
        url: '/api/v1/groups',
        type: 'post',
        contentType: 'application/json',
        data: JSON.stringify({
            "id":$('#upload-data-div').data("id"),
            "name":$('#upload-data-name-input').val(),
            "description":$('#upload-data-description-input').val(),
            "tags":$('#upload-data-tags-input').val(),
            "session_id":$('#upload-modal').data('session_id')
        }),
        success: function(d, st, xhr) {
            resetUploadDom()
            $('#upload-modal').modal('hide');
        },
        error: function(d, st, xhr) {
            uploadShowError(d.responseJSON.err_msg);
        }
    });
};

uploadShowError = function(text) {
    $('#upload-success-div').hide();
    $('#upload-error-div').show();
    $('#upload-error-div').text(text);
}

uploadShowSuccess = function(text) {
    $('#upload-success-div').show();
    $('#upload-error-div').hide();
    $('#upload-success-div').text(text);
}

deleteQrcode = function() {
    $.ajax({
        url: '/api/v1/groups',
        type: 'delete',
        contentType: 'application/json',
        data: JSON.stringify({
            "id":$('#upload-data-div').data("id"),
            "session_id":$('#upload-modal').data('session_id')
        }),
        success: function(d, st, xhr) {
            resetUploadDom()
            $('#upload-modal').modal('hide');
        },
        error: function(d, st, xhr) {
            uploadShowError(d.responseJSON.err_msg);
        }
    })
}

$(function() {
    // Upload Image to server
    $('#upload-file-input').change(function() {
        var fileName = $('#upload-file-input')[0].files[0].name;
        var fileSize = $('#upload-file-input')[0].files[0].size;
        if (fileName) {
            if (fileSize < 1024 * 1024 * 2) {
                $('#upload-file-label').text(fileName);
                var fdata = new FormData($("#upload-form")[0]);
                $('#upload-progress-bar').css("width", '0%');
                $('#upload-progress-div').show();
                var reader = new FileReader();
                reader.readAsDataURL($('#upload-file-input')[0].files[0]);
                $.ajax({
                    xhr:function() {
                        var xhr = new window.XMLHttpRequest();
                        xhr.upload.addEventListener("progress", function(evt) {
                            if (evt.lengthComputable) {
                                var percentComplete = evt.loaded/evt.total;
                                $('#upload-progress-bar').css("width", percentComplete*100+'%');
                            }
                        });
                        return xhr;
                    },
                    url: '/api/v1/qrcode',
                    type: 'post',
                    data: fdata,
                    processData: false,
                    contentType: false,
                    success: function(d, st, xhr) {
                        $('#upload-progress-div').hide();
                        $('#upload-progress-bar').css("width", '0%');
                        $('#upload-data-div').data("id", d.id);
                        $('#upload-img-preview').attr('src', reader.result);
                        $('#upload-img-preview').show();
                        $('#upload-data-div').show();
                        $('#upload-data-name-input').val(d.name);
                        $('#upload-data-description-input').val(d.description);
                        $('#upload-data-tags-input').val(d.tags.join(" "));
                        $('#upload-confirm-button').removeClass("disabled");
                        $('#upload-delete-button').removeClass("disabled");
                        $('#upload-modal').data('session_id', d['session_id']);
                        uploadShowSuccess("上传成功！");
                    },
                    error: function(d, st, xhr) {
                        $('#upload-progress-div').hide();
                        $('#upload-img-preview').hide();
                        $('#upload-data-div').hide();
                        $('#upload-confirm-button').addClass("disabled");
                        $('#upload-delete-button').addClass("disabled");
                        uploadShowError(d.responseJSON.err_msg);
                    }
                });
            } else {
                $('#upload-img-preview').hide();
                $('#upload-data-div').hide();
                $('#upload-confirm-button').addClass("disabled");
                $('#upload-delete-button').addClass("disabled");
                uploadShowError("File size is too large! Only support images under 2MB");
            }
        } else {
            $('#upload-file-label').text("选择文件");
        }
    });

    $('#upload-confirm-button').click(function() {
        if (!$(this).hasClass('disabled')) {
            uploadQrcode();
        }
    });

    $('#upload-delete-button').click(function() {
        if (!$(this).hasClass('disabled')) {
            deleteQrcode();
        }
    });

    // Download
    $('#download_button').click(function() {
        $('#download_img').attr('src','/api/v1/qrcode?id='+$('#download_text').val());
    });

    // Search
    $('body').on("click", "#search-button", function() {
        qrcodeData = {"keywords":$('#search-text').val()};
        listPage(qrcodeData);
    });

    $('#search-text').keypress(function(event) {
        if (event.which == 13) {
            console.log('click');
            $('#search-button').trigger("click");
        }
    })

    // Change view
    $('#change-view-list-button').click(function() {
        $(this).addClass("active");
        $('#change-view-block-button').removeClass("active");
        qrcodeView = "list";
        listPage(qrcodeData);
    });

    $('#change-view-block-button').click(function() {
        $('#change-view-list-button').removeClass("active");
        $(this).addClass("active");
        qrcodeView = "block";
        listPage(qrcodeData);
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

    $(window).scroll(function() {
        if ($(window).scrollTop() + $(window).height() == $(document).height()) {
            appendPage()
        }
    });
    listPage();

    if ($(window).width() < 768) {
      $('#change-view-button-group').addClass("d-none");
    }

    // Things to do when user resize the window
    $(window).resize(function() {
        // Restrict to list view when window width is less than 768
        if ($(window).width() < 768) {
          $('#change-view-button-group').addClass("d-none");
          qrcodeView = "list";
        } else {
          $('#change-view-button-group').removeClass("d-none");
          if ($('#change-view-list-button').hasClass("active")) {
            qrcodeView = "list";
          } else if ($('#change-view-block-button').hasClass("active")) {
            qrcodeView = "block";
          }
        }

        // reset the  height for cards in each row
        adjustCardsHeight();
    });
})
