$(function() {
    $('#_add').hide();

    $('#add_button').click(function(event) {
        event.preventDefault();
        $('#_add').show();
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