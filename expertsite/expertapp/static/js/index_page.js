$(function () {

    // 超連結點擊後的滾動動畫設定
    $('#face_section>.get_start>a').bind('click', function (e) {
        var anchor = $(this);
        var animationTime = 1500;
        var timingFunction = 'easeInOutCubic';
        var target = anchor.attr('href');
        console.log(target);

        $('html, body').stop().animate({
            scrollTop: ($(target).offset().top)
        }, animationTime, timingFunction);

        //取消預設會直接飛過去的方法
        e.preventDefault();
    });

    // nav-toggle
    $('#nav_bar').hide();
    $("#nav-toggle").bind("click", function () {
        this.classList.toggle("active");
        $('#nav_bar').toggle();
    });

    // list_database Modal 
    $('#nav_bar>a.list_database').bind('click', function () {
        $.ajax({
            url: "/list_database_ajax",
            type: "POST",
            data: {
                'modal': 'modal'
            },
            dataType: "json",
            success: function (data) {
                for (var key in data['med_list']) {
                    $('#list_database').append('<h4>' + data['med_list'][key] + ' : ' + data['sym_list'][key] + '</h4>');
                    console.log(data['med_list'][key], data['sym_list'][key]);
                }
                console.log('success list database');
            },
        });

        $('.ui.modal').modal({
            observeChanges: true,
            onHide: function () {
                $('#list_database').empty();
                console.log('hidden and clear');
            }
        }).modal('show');
    });

});
