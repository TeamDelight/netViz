function searchAutoComplete() {
        remove_table();
        $.ajax({
                type: "POST",
                url: '/searchlist',
                data: $('#autocomplete').serialize()
        }).done(function (data) {
                $('#autocomplete').autocomplete({
                        source: data,
                        minLength: 1
                });
        });
}

function remove_table() {
        if (($("#search_result_table").is(":visible"))) {
                ($("#search_result_table")).hide();
        }

        if (($("#no_records").is(":visible"))) {
                ($("#no_records")).hide();
        }

}

$('tr.table-data').click( function() {
        console.log( "hello");
        window.location = $(this).find('a').attr('href');
    }).hover( function() {
        $(this).toggleClass('hover');
    });