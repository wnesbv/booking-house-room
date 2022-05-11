$(() => {
    $('.js-slider').each(function () {
        const self = $(this);
            const shift = self.data('shift');
            const carousel = self.data('carousel');
            const autoSlide = self.data('auto-slide');
            const swipe = self.data('swipe');

        if (swipe) {
            self.find('.view-layer').css({
                width: '307px',
            });
        }
        var slider = self.isystkSlider({
            parentKey: '.parent',
            childKey: '.child',
            shift,
            carousel,
            isMouseDrag: swipe,
            autoSlide,
            prevBtnKey: self.find('.prev-btn'),
            nextBtnKey: self.find('.next-btn'),
            slideCallBack(data) {
                slider.find('.paging li').removeClass('active');
                slider.find(`.paging li:eq(${data.pageNo - 1})`).addClass('active');
            },
        });
        slider.find('.paging li').click(function (e) {
            e.preventDefault();
            slider.changePage($(this).data('pageno'), $.fn.isystkSlider.ANIMATE_TYPE.SLIDE);
        });
        if (self.find('.prev-btn').length > 0) {
            self.find('.view-layer').css({
                'margin-left': '36px',
            });
        }
    });
});
