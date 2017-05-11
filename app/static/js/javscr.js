function search() {
    var req = new XMLHttpRequest();
    var url = document.getElementById("box").value;
	

	req.open("GET", url, true);
    req.onreadystatechange = function(){

        if (req.readyState==4) {
            if (req.status==200){    
                    info= JSON.parse(req.responseText);
                    teeTaulukko(info);
            }    
            else {
                alert("Tiedon noutaminen ei onnistu (error code: "+ req.statusText + ")");
            }
        }
    }
    req.send();
}


function teeTaulukko(info) {

    // Silmukoidaan JSON:sta saatua tietoa
	// tietorivi-muuttuja sisaltaa otsikon ja kuvauksen
	for (i=0;i<info.length;i++){
        // Haetaan kaikki allaolevat jutut JSON-tiedoista
		
        var tietorivi = (info[i].id);

		
		// Dokumenttiin luodaan li elementti.
		// linode on DOM noodi johon voidaan antaa tekstia
		linode = document.createElement("li");
		
		// tietorivi-muuttujan sisalto annetaan dokumentille tulostettavaksi
		linode.innerHTML = "Value of id is "+tietorivi;
		
		// OL elementtiin sisallytetaan linodeja
		// eli listataan tapahtumat numeroilla
		text.appendChild(linode);
    }
	document.getElementById("butn").style.display = "none";
}

// Kuuntelija napin painallukselle
butn.addEventListener("click", function() {
    search();
});

