$(function () {

    // add medicine
    $("#btn_add").bind('click', function () {
        var add_medicine_name = $('#add_medicine_name').val();
        var add_medicine_symptom = $('#add_medicine_symptom').val();
        console.log(add_medicine_name);
        console.log(add_medicine_symptom);

        if (add_medicine_name != "" && add_medicine_symptom != "") {
            $.ajax({
                url: "/admin_add_ajax",
                type: "POST",
                data: {
                    'add_medicine_name': add_medicine_name,
                    'add_medicine_symptom': add_medicine_symptom
                },
                dataType: "json",
                success: function (data) {
                    $('.add_complete').text(data['medicine']);
                    $('.add_status').text(data['status']);
                    console.log('success add medicine');

                    if ($('.add_status').text() == 'success') {
                        var med = $('.add_complete').text();
                        iziToast.success({
                            title: '成功！',
                            message: med + ' 中藥材已成功新增！',
                        });
                    }
                },
            });
        } else {
            console.log('add medicine ajax error')
        }
        // 清空 input
        $('#add_medicine_name').val('');
        $('#add_medicine_symptom').val('');
    });

    // del medicine
    $("#btn_del").click(function () {
        var del_medicine_name = $('#del_medicine_name').val();
        console.log(del_medicine_name);

        if (del_medicine_name != "") {
            $.ajax({
                url: "/admin_del_ajax",
                type: "POST",
                data: {
                    'del_medicine_name': del_medicine_name
                },
                dataType: "json",
                success: function (data) {
                    $('.del_complete').text(data['medicine']);
                    $('.del_status').text(data['status']);

                    if ($('.del_status').text() == 'success') {
                        var med = $('.del_complete').text();
                        iziToast.success({
                            title: '成功！',
                            message: med + ' 中藥材已成功刪除！',
                        });
                    } else if ($('.del_status').text() == 'error') {
                        var med = $('.del_complete').text();
                        iziToast.error({
                            title: '失敗！',
                            message: '知識庫中沒有 ' + med + ' 中藥材！',
                        });
                    }
                },
            });
        } else {
            console.log('del medicine ajax error')
        }
        // 清空input
        $('#del_medicine_name').val('');
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

    // 超連結點擊後的滾動動畫設定
    $('#up_down>#add_section_circle, #up_down>#del_section_circle').bind('click', function (e) {
        var anchor = $(this);
        var animationTime = 1500;
        var timingFunction = 'easeInOutCubic';
        var target = anchor.attr('href');
        console.log(target);

        $('html, body').stop().animate({
            scrollTop: ($(target).offset().top)
        }, animationTime, timingFunction);

        // 取消預設會直接飛過去的方法
        e.preventDefault();
    });

    // 右側圓點
    $('#up_down>#add_section_circle').bind('click', function () {
        $('#up_down>#add_section_circle>i').attr('class', 'circle icon');
        $('#up_down>#del_section_circle>i').attr('class', 'circle thin icon');
    });

    $('#up_down>#del_section_circle').bind('click', function () {
        $('#up_down>#add_section_circle>i').attr('class', 'circle thin icon');
        $('#up_down>#del_section_circle>i').attr('class', 'circle icon');
    });

});
