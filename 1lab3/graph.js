var MAX_NUM = 100;

var LABELS = {
        pl : "Плазма", 
        cr : "Криопреципитат",
        fib: "Фибриноген",
        rib: "Добавление упаковки",
        trig:"Триггер",
        targ:"Целевой уровень"
    },
    XAXISES= {
        a: {
            ticks: 5,
            min: 0.5,
            max: 2.5,
            tickDecimals: 1
        },
        b: {
            ticks: 6,
            min: 0,
            max: 100,
            tickDecimals: 1
        },
        c: {
            ticks: 4,
            min: 0.5,
            max: 2.5,
            tickDecimals: 1
        }
    },
    YAXISES= {
        a: {
            ticks: 11,
            min: 0,
            max: 10,
            tickDecimals: 1
        },
        b: {
            ticks: 11,
            min: 0,
            max: 100,
            tickDecimals: 1
        },
        c: {
            ticks: 4,
            min: 0,
            max: 20,
            tickDecimals: 1
        }
    };

    var draw = function () {

        var xaxis = YAXISES['a'],
            yaxis = YAXISES['b'];
        
        data = [{data: [[0.5, 0], [1.5, 10.6], [1.9, 21.7], [2.5, 38.7], [3.5, 57.1], [4.5, 66.5], [5.5, 72.8], [6.5, 76.8], [7.5, 79.8], [8.5, 82.1], [9.5, 84.1], [10.5, 85.7]]}]

        $.plot("#chart", data, {
            series: {
                lines: { show: true },
                points: { show: true }
            },
            legend: {
                container: "#fiblabel"
            },
            xaxis: YAXISES.a,
            yaxis: YAXISES.b,
            grid: {
                backgroundColor: { colors: [ "#fff", "#eee" ] },
                borderWidth: {
                    top: 1,
                    right: 1,
                    bottom: 2,
                    left: 2
                }
            }
        });
    };

    draw()