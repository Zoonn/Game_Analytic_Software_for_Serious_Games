$(document).ready(function() {

	// This is test data. It has to be replaced with data from DB
	var testData = [{"a1":17,"a2":13,"a3":12},{"a1":27,"a2":23,"a3":22},{"a1":11,"a2":15,"a3":16},{"a1":21,"a2":24,"a3":22}];

	var count1 = 0;
	var count2 = 0;
	var count3 = 0;
	
	for (var i = 0; i < testData.length; i++) {
		count1 += testData[i].a1;
        count2 += testData[i].a2;
        count3 += testData[i].a3;
   }
	  chart(count1, count2, count3);  
})
 
	function chart(d1, d2, d3) {
		// Modified from Highcharts
		Highcharts.chart('container', {
    chart: {
        type: 'bar'
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
        name: 'First',
        data: [d1]
    }, {
        name: 'Second',
        data: [d2]
    }, {
        name: 'Third',
        data: [d3]
    }]
});
	}	