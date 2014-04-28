function main(){
    var raw = document.getElementById('raw').value;
    raw = raw.replace(/\s/g,'|');
//    console.log(raw);
    var lst = raw.split('|');
//    console.log(lst)

    var dig = [];
    for (var i = 0; i < lst.length; i++) {
	   dig[i] = parseFloat(lst[i])
    };
    dig.sort(function(a, b){return b-a})

    W = parseFloat(document.getElementById('sum').value);

    var result = select([], dig, W);
    //alert(result)
    var res = document.getElementById('results');
    var output = result.join("\n") + "\n----\nSUM = " + sumList(result) + "\nDIF = " + (Math.abs(sumList(result) - W));
    res.innerHTML = output;

//    console.log(output)
}

function select(result, vault, w){
	//console.log("Calling select " + sumList(result) + ", result = "+ result.length + ", vault = "+vault.length+", w = " + w)
	if(sumList(vault) <= w){
		console.log("Not enough elements!")
		return result.concat(vault);
	}else{
		var tmpVault = digSlice(vault, w);
	//console.log(tmpVault)
	//console.log(tmpVault.length)
		var sum = 0;
		for (var i = 0; i < tmpVault.length; i++) {
			sum += tmpVault[i];
			if(sum > w){
				sum -= tmpVault[i];
				break;
			}
		};
		result = result.concat(tmpVault.slice(0, i));
		//if(Math.abs(w - sum) <= 500 || i == tmpVault.length){
		if(i == tmpVault.length){
			return result;
		}else{
			return select(result, tmpVault.slice(i,tmpVault.length), w - sum);
		}
	}
}
function digSlice(vault, w){
	//vault.sort(function(a, b){return b-a});
	//find vault index less than w
	for (var i = 0; i < vault.length; i++) {
		if(vault[i] <= w)
			break;
	};
	vault = vault.slice(i, vault.length);
	return vault;
}
function range(len){
	var r = [];
	for (var i = 0; i < len; i++) {
		r[i] = i;
	};
	return r;
}
function sumList(vault){
	var sum = 0;
	for (var i = 0; i < vault.length; i++) {
		sum += vault[i];
	};
	return sum;
}
