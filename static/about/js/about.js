        $(() => {
            const $cn_next = $('#cn_next');
            const $cn_prev = $('#cn_prev');
            const $cn_list = $('#cn_list');
            const $pages = $cn_list.find('.cn_page');
            const cnt_pages = $pages.length;
            let page = 1;
            const $items = $cn_list.find('.cn_item');
            const $cn_preview = $('#cn_preview');
            let current = 1;

            $items.each(function (i) {
                const $item = $(this);
                $item.data('idx', i + 1);

                $item.bind('click', function () {
                    const $this = $(this);
                    $cn_list.find('.selected').removeClass('selected');
                    $this.addClass('selected');
                    const idx = $(this).data('idx');
                    const $current = $cn_preview.find(`.cn_content:nth-child(${current})`);
                    const $next = $cn_preview.find(`.cn_content:nth-child(${idx})`);

                    if (idx > current) {
                        $current.stop().animate({ top: '-100%' }, 600, 'easeOutBack', function () {
                            $(this).css({ top: '100%' });
                        });
                        $next.css({ top: '100%' }).stop().animate({ top: '0%' }, 600, 'easeOutBack');
                    } else if (idx < current) {
                        $current.stop().animate({ top: '100%' }, 600, 'easeOutBack', function () {
                            $(this).css({ top: '100%' });
                        });
                        $next.css({ top: '-100%' }).stop().animate({ top: '0%' }, 600, 'easeOutBack');
                    }
                    current = idx;
                });
            });

            $cn_next.bind('click', function (e) {
                const $this = $(this);
                $cn_prev.removeClass('disabled');
                ++page;
                if (page === cnt_pages) { $this.addClass('disabled'); }
                if (page > cnt_pages) {
                    page = cnt_pages;
                    return;
                }
                $pages.hide();
                $cn_list.find(`.cn_page:nth-child(${page})`).fadeIn();
                e.preventDefault();
            });

            $cn_prev.bind('click', function (e) {
                const $this = $(this);
                $cn_next.removeClass('disabled');
                --page;
                if (page === 1) { $this.addClass('disabled'); }
                if (page < 1) {
                    page = 1;
                    return;
                }
                $pages.hide();
                $cn_list.find(`.cn_page:nth-child(${page})`).fadeIn();
                e.preventDefault();
            });
        });