function searchAutoComplete() {
    $.ajax({
        type: "POST",
        url: '/autocomplete',
        data: $('#autocomplete').serialize()
    }).done(function(data) {
        $('#autocomplete').autocomplete({
            source: data,
            minLength: 1
        });
    });
}