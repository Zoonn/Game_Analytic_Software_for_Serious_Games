/**
 * Created by Omppu on 16/05/2017.
 */
$(document).ready(function() {



    var data = [{
		"start_datetime": 1431446400000,
		"end_datetime": 1431457200000
	},
	{
		"start_datetime": 1431532800000,
		"end_datetime": 1431543600000
	},
	{
		"start_datetime": 1431705600000,
		"end_datetime": 1431716400000
	},
	{
		"start_datetime": 1431792000000,
		"end_datetime": 1431802800000
	},
	{
		"start_datetime": 1432051200000,
		"end_datetime": 1432062000000
	},
	{
		"start_datetime": 1432137600000,
		"end_datetime": 1432148400000
	},
	{
		"start_datetime": 1432224000000,
		"end_datetime": 1432234800000
	},
	{
		"start_datetime": 1432396800000,
		"end_datetime": 1432407600000
	},
	{
		"start_datetime": 1432656000000,
		"end_datetime": 1432666800000
	},
	{
		"start_datetime": 1432742400000,
		"end_datetime": 1432753200000
	},
	{
		"start_datetime": 1432828800000,
		"end_datetime": 1432839600000
	},
	{
		"start_datetime": 1432915200000,
		"end_datetime": 1432926000000
	},
	{
		"start_datetime": 1433001600000,
		"end_datetime": 1433012400000
	},
	{
		"start_datetime": 1433260800000,
		"end_datetime": 1433271600000
	},
	{
		"start_datetime": 1433347200000,
		"end_datetime": 1433358000000
	},
	{
		"start_datetime": 1433520000000,
		"end_datetime": 1433530800000
	}
]


	var timeString = [];
	var timeString2 = [];

	var time;
	var time2;

	var subtraction;
	var minutes;


	for (i=0; i< data.length; i++) {
		timeString.push(data[i].start_datetime);
		timeString2.push(data[i].end_datetime);
		//if (timeString[i] > 0)

		subtraction = timeString2[i] - timeString[i];

		time = new Date(timeString[i]);
		time2 = new Date(timeString2[i]);


		minutes = Math.floor(subtraction / 60000);


		linode = document.createElement("li");
		linode.innerHTML = time + ":__________" + time2 + "_________session lasted: " + minutes + " minutes"+  "<br />";
		text.appendChild(linode);
	}




})
