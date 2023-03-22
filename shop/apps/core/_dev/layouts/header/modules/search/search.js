import './search.scss';

function init() {
    $('.search_form input[name="s"]').on('input', function () {
        var search = $('.search_form input[name="s"]').val();
        var searchResult = $('.search_form .search-result')
        if (search.length < 4) {
            searchResult.removeClass('show')
            return false;
        }
        var data = {
            s: search,
            action: 'search_action',
            nonce: search_form.nonce
        };
        $.ajax({
            url: search_form.url,
            data: data,
            type: 'POST',
            dataType: 'json',
            beforeSend: function (xhr) {
            },
            success: function (data) {
                if (data.out) {
                    searchResult.addClass('show')
                } else {
                    searchResult.removeClass('show')
                }
                searchResult.html(data.out);
            }
        });
    });
}

export default init;


