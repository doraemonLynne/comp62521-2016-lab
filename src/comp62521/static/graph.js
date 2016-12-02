$(function () {
    var publications=[];
    $("tbody tr:nth-child(1) td").not(":first").each(function(){
      publications.push(parseInt($(this).text()));
    });
    var authors=[];
    $("tbody tr:nth-child(2) td").not(":first").each(function(){
      authors.push(parseInt($(this).text()));
    });
    Highcharts.chart('container', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Publication Summary',
        },
        xAxis: {
            categories: ['Conference', 'Journal','Book','Book Chapter','Total']
        },
        yAxis: {
            title: {
                text: 'Numbers'
            },
        },
        series: [{
            name: 'Number of publications',
            data: publications
        }, {
            name: 'Number of authors',
            data: authors
        }]
    });
});
