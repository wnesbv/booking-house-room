if (typeof $ !== 'undefined') {
    $(document).ready(() => {
        $(document).on('click', 'a.liker', function (event) {
            event.preventDefault();
            const el = $(this);
            const replace_selector = el.attr('replace_selector');
            if (!replace_selector) { var replace_target = el.parents('.likes:first'); } else { var replace_target = $(replace_selector); }
            $.get(el.attr('href'), {}, (data) => {
                replace_target.html(data);
            });
        });
    });
}
