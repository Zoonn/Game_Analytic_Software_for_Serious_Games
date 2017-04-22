$(document).ready(function() {

	// This is test data. It has to be replaced with data from DB
	var testData1 = [{"a1":17,"a2":13,"a3":12},{"a1":27,"a2":23,"a3":22},{"a1":11,"a2":15,"a3":16},{"a1":21,"a2":24,"a3":22}];

	var count1a = 0;
	var count2a = 0;
	var count3a = 0;
	
	for (var i = 0; i < testData1.length; i++) {
		count1a += testData1[i].a1;
        count2a += testData1[i].a2;
        count3a += testData1[i].a3;
	}
    chart1(count1a, count2a, count3a);

	var testData2 = [{"b1":10.3},{"b2":35.5},{"b3":54.2}];

	var share1 = testData2[0].b1;
	var share2 = testData2[1].b2;
	var share3 = testData2[2].b3;

    chart2(share1, share2, share3);

})

    // First chart is made here
	function chart1(d1, d2, d3) {
		// Modified from Highcharts
		Highcharts.chart('container1', {
    chart: {
        type: 'bar'
    },
    title: {
        text: 'Working hours of employees'
    },
    xAxis: {
        categories: ['Employees'],
        title: {
            text: null
        }
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Hours / week',
            align: 'high'
        },
        labels: {
            overflow: 'justify'
        }
    },
    series: [{
        name: 'Employee 1',
        data: [d1]
    }, {
        name: 'Employee 2',
        data: [d2]
    }, {
        name: 'Employee 3',
        data: [d3]
    }]
});
	}


	// Seconf chart is made here
    function chart2(e1, e2, e3) {
		// Modified from Highcharts
		Highcharts.chart('container2', {
    chart: {
        type: 'pie'
    },
    title: {
        text: 'Browser distribution'
    },
    xAxis: {
        categories: 'testnumbers',
        title: {
            text: null
        }
    },
    yAxis: {
        min: 0,
        title: {
            text: '',
            align: 'high'
        },
        labels: {
            overflow: 'justify'
        }
    },
    series: [{
            name: 'Brands',
            colorByPoint: true,
            data: [{
                name: 'Microsoft Internet Explorer',
                y: e1
            }, {
                name: 'Chrome',
                y: e2,
                sliced: true,
                selected: true
            }, {
                name: 'Firefox',
                y: e3
            }]
        }]
});
	}