$(function () {
    $(".multi-menu .title").click(function () {
        // 对设置或移除被选元素进行切换，说白了就是，有就去掉，没有就加上
        // bs3: hide,  bs5: visually-hidden
        $(this).next().toggleClass('visually-hidden');
    });
})