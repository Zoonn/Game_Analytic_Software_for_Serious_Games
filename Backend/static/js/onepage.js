
$(document).ready(function() {
/*
var url = "http://visittampere.fi:80/api/search?type=event&free=false&limit=20";
sendRequest (url);
function sendRequest (url) {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var data = JSON.parse(xmlhttp.responseText);
			
			var ff = JSON.stringify(data);
			
		}
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

*/
	var data = [{"id":1695,"start_datetime":1431446400000,"end_datetime":1431457200000},{"id":1696,"start_datetime":1431532800000,"end_datetime":1431543600000},{"id":1697,"start_datetime":1431705600000,"end_datetime":1431716400000},{"id":1698,"start_datetime":1431792000000,"end_datetime":1431802800000},{"id":1699,"start_datetime":1432051200000,"end_datetime":1432062000000},{"id":1700,"start_datetime":1432137600000,"end_datetime":1432148400000},{"id":1701,"start_datetime":1432224000000,"end_datetime":1432234800000},{"id":1702,"start_datetime":1432396800000,"end_datetime":1432407600000},{"id":1703,"start_datetime":1432656000000,"end_datetime":1432666800000},{"id":1704,"start_datetime":1432742400000,"end_datetime":1432753200000},{"id":1705,"start_datetime":1432828800000,"end_datetime":1432839600000},{"id":1706,"start_datetime":1432915200000,"end_datetime":1432926000000},{"id":1707,"start_datetime":1433001600000,"end_datetime":1433012400000},{"id":1708,"start_datetime":1433260800000,"end_datetime":1433271600000},{"id":1709,"start_datetime":1433347200000,"end_datetime":1433358000000},{"id":1710,"start_datetime":1433520000000,"end_datetime":1433530800000}];
	
	var ff = JSON.stringify(data);
	
	
document.getElementById("container").innerHTML = ff;
	

});