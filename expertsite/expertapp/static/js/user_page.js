$(function () {

    $("#btn_send_symptom").click(function () {
        var user_symptom = $('#user_symptom').val();

        // 清空#predict及#re_callback
        $('#predict').empty();
        $('#re_callback').empty();

        if (user_symptom != "") {
            $.ajax({
                url: "/user_symptom_ajax",
                type: "POST",
                data: {
                    'user_symptom': user_symptom,
                },
                dataType: "json",
                success: function (data) {
                    // 清空使用者原本輸入
                    $('#user_symptom').val('');

                    $('#predict').append("<p class='animated fadeInUp'>您的症狀為 " + data['predict_sym'] + "</p>")

                    if (data['predict'] == 'none') {
                        $('#re_callback').append('<p>沒有這種中藥材呦ＱＱ</p>');
                    } else if (data['predict'].length == 1) {
                        $('#re_callback').append('<p>您可能需要 ' + data['predict'] + ' 中藥材!');
                    } else {
                        var predict = data['predict'];
                        var comparison_symptom = data['comparison_symptom'];

                        var remember = new Array(); // 記住已問過的症狀

                        var count = 0;
                        var hidden = ''; // 進畫面先隱藏其他元素
                        for (var key_pre in predict) {
                            for (var key_sym in comparison_symptom) {
                                for (var key in comparison_symptom[key_sym]) {
                                    if (remember.indexOf(comparison_symptom[key_sym][key]) != -1) {
                                        // pass
                                    } else {
                                        remember.push(comparison_symptom[key_sym][key]);

                                        // 定義模板
                                        var ask_html = '<p>請問您有 ' + comparison_symptom[key_sym][key] + ' 的症狀嗎？</p>';
                                        var yes_btn_html = '<button class="large ui blue button" style="margin-right:30px;"' + ' id=' + count + 'yes' + '>有</button>';
                                        var no_btn_html = '<button class="large ui red button" style="margin-left:30px;"' + ' id=' + count + 'no' + '>沒有</button>';
                                        var recommend_html = '<p class="recommend animated fadeInUp" style="display: none;">推薦您' + predict[key_sym] + '中藥材！</p>';

                                        var div_html = '<div class=' + '"' + 'animated fadeInUp ' + count + '"' + hidden + '>' + ask_html + yes_btn_html + no_btn_html + recommend_html + '</div>'

                                        $('#re_callback').append(div_html);

                                        count++;
                                        hidden = "style='display: none;'"

                                        // 更改右側圓點
                                        $('#up_down>#user_symptom_section_circle>i').attr('class', 'circle thin icon');
                                        $('#up_down>#predict_section_circle>i').attr('class', 'circle icon');

                                        console.log(comparison_symptom[key_sym][key]);
                                        console.log('推薦您' + predict[key_sym] + '中藥材！');
                                    }
                                }
                            }
                        }

                        // 綁定yes按鈕
                        $("button[id*='yes']").bind('click', function () {
                            $(this).nextAll('p').css('display', '');
                            $(this).prev().hide();
                            $(this).hide();
                            $(this).nextAll('button').hide();
                        });

                        // 綁定no按鈕
                        $("button[id*='no']").bind('click', function () {
                            if ($(this).parent().next().length > 0) {
                                $(this).parent().next().css('display', '');
                                $(this).parent().hide();
                            } else {
                                $(this).parent().hide();
                                $('#last_none').append('<p class="animated fadeInUp">沒有這種中藥材呦ＱＱ</p>');
                                console.log('沒了');
                            }
                        });
                    }
                    console.log('success');
                },
            });
        } else {
            console.log('nothing input ajax')
        }

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
    $('#btn_send_symptom, #up_down>#user_symptom_section_circle, #up_down>#predict_section_circle').bind('click', function (e) {
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
    $('#up_down>#user_symptom_section_circle').bind('click', function () {
        $('#up_down>#user_symptom_section_circle>i').attr('class', 'circle icon');
        $('#up_down>#predict_section_circle>i').attr('class', 'circle thin icon');
    });

    $('#up_down>#predict_section_circle').bind('click', function () {
        $('#up_down>#user_symptom_section_circle>i').attr('class', 'circle thin icon');
        $('#up_down>#predict_section_circle>i').attr('class', 'circle icon');
    });

});
