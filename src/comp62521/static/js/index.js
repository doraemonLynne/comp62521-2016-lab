/**********
Ease to nav
**********/
$(function() {
    $().UItoTop({
        easingType: 'easeOutQuart'
    });
    $(".scroll").click(function(event) {
        event.preventDefault();
        $('html,body').animate({
            scrollTop: $(this.hash).offset().top
        }, 1000);
    });
});


/**************
Nav menu effect
**************/
$(function() {
    $(".nav-fir").mouseenter(function() {
        $(this).find(".nav-sec").animate({
            "height": "170%",
        }, 400)
    })
    $(".nav-fir").mouseleave(function() {
        $(this).find(".nav-sec").animate({
            "height": "0",
        }, 400)
    })
});


/*****************************
Total Publications and authors
******************************/
$(function() {
    $.getJSON('/index/totalPub', function(data) {
        $(".totalPub").text(data.totalPub);
    });
    $.getJSON('/index/totalAuth', function(data) {
        $(".totalAuth").text(data.totalAuth);
    });
});


/********************
Figures for year data
*********************/
$(function() {
    $.ajax({
        url: '/index/pubByYear',
        type: 'GET',
        async: true,
        dataType: "json",
        success: function(data) {
            var Data = data.args.data[1];
            var year = [];
            var journals = [];
            var books = [];
            var conference = [];
            var chapers = [];
            var total = [];
            for (i = 0; i < Data.length; i++) {
                year.push(parseInt(Data[i][0]));
                conference.push(parseInt(Data[i][1]));
                journals.push(parseInt(Data[i][2]));
                books.push(parseInt(Data[i][3]));
                chapers.push(parseInt(Data[i][4]));
                total.push(parseInt(Data[i][5]));
            }
            pubByYearData(year, conference, journals, books, chapers, total);
        }
    });

    $.ajax({
        url: '/index/authByYear',
        type: 'GET',
        async: true,
        dataType: "json",
        success: function(data) {
            var Data = data.args.data[1];
            var year = [];
            var journals = [];
            var books = [];
            var conference = [];
            var chapers = [];
            var total = [];
            for (i = 0; i < Data.length; i++) {
                year.push(parseInt(Data[i][0]));
                conference.push(parseInt(Data[i][1]));
                journals.push(parseInt(Data[i][2]));
                books.push(parseInt(Data[i][3]));
                chapers.push(parseInt(Data[i][4]));
                total.push(parseInt(Data[i][5]));
            }
            authByYearData(year, conference, journals, books, chapers, total);
        }
    });

    function pubByYearData(year, conference, journals, books, chapers, total) {
        Highcharts.chart('pubByYear', {
            title: {
                text: 'Publication by Year',
            },
            xAxis: {
                categories: year
            },
            yAxis: {
                title: {
                    text: 'Number'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: [{
                name: 'Number of conference papers',
                data: conference
            }, {
                name: 'Number of journals',
                data: journals
            }, {
                name: 'Number of books',
                data: books
            }, {
                name: 'Number of book chapers',
                data: chapers
            }, {
                name: 'Total',
                data: total
            }]
        });
    };

    function authByYearData(year, conference, journals, books, chapers, total) {
        Highcharts.chart('authByYear', {
            title: {
                text: 'Author by Year',
            },
            xAxis: {
                categories: year
            },
            yAxis: {
                title: {
                    text: 'Number'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: [{
                name: 'Number of conference papers',
                data: conference
            }, {
                name: 'Number of journals',
                data: journals
            }, {
                name: 'Number of books',
                data: books
            }, {
                name: 'Number of book chapers',
                data: chapers
            }, {
                name: 'Total',
                data: total
            }]
        });
    };
});
