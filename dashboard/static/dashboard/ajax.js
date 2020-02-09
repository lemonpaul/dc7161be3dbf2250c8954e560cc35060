$(function() {
    $('#_add').hide();

    $('#add_button').click(function(event) {
        event.preventDefault();
        $('#_add').show();
    });

    $('#add_form').submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/add/',
            data: $('#add_form').serialize(),
            success: function (data, textStatus, xhr) {
                if (xhr.status == 202)
                {
                    $('#_add').html(data);
                } else {
                    $('#_list').html(data);
                    $('#_add').hide();
                }
            }
        });
    });

    $('#done_form').submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/done/',
            data: $('#done_form').serialize(),
            success: function (data, textStatus) {
                $('#_list').html(data);
            }
        });
    });
});