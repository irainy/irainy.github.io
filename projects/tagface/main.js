var tags = {'rainy': 1, 'defsniky': 1, 'lab407': 1};


var cloud = document.getElementById('cloud');
for( tag in tags){
	var tagWraper = document.createElement('span');
	tagWraper.innerHTML = tag;
	tagWraper.style.fontSize = ""+Math.floor(Math.random() * 140)+"px";
	tagWraper.style.background = rgba(255, 2, 200, 1);
	cloud.appendChild(tagWraper);
}
