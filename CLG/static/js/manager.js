// This section contains the Javascript used for interface elements %>
var check = false;
// Disables the checkbox feature %>
function dis() {
	check = true;
}

var DOM = 0, MS = 0, OP = 0, b = 0;
// Determine the browser type %>
function CheckBrowser() {
	if (b == 0) {
		if (window.opera)
			OP = 1;
		// Moz or Netscape
		if (document.getElementById)
			DOM = 1;
		// Micro$oft
		if (document.all && !OP)
			MS = 1;
		b = 1;
	}
}
// Allows the whole row to be selected %>
function selrow(element, i) {
	var erst;
	CheckBrowser();
	if ((OP == 1) || (MS == 1))
		erst = element.firstChild.firstChild;
	else if (DOM == 1)
		erst = element.firstChild.nextSibling.firstChild;
	// MouseIn %>
	if (i == 0) {
		if (erst.checked == true)
			element.className = 'mousechecked';
		else
			element.className = 'mousein';
	}
	// MouseOut %>
	else if (i == 1) {
		if (erst.checked == true)
			element.className = 'checked';
		else
			element.className = 'mouseout';
	}
	// MouseClick %>
	else if ((i == 2) && (!check)) {
		if (erst.checked == true)
			element.className = 'mousein';
		else
			element.className = 'mousechecked';
		erst.click();
	} else
		check = false;
}
// Filter files and dirs in FileList%>
function filter(begriff) {
	var suche = begriff.value.toLowerCase();
	var table = document.getElementById("filetable");
	var ele;
	for (var r = 1; r < table.rows.length; r++) {
		ele = table.rows[r].cells[1].innerHTML.replace(/<[^>]+>/g, "");
		if (ele.toLowerCase().indexOf(suche) >= 0)
			table.rows[r].style.display = '';
		else
			table.rows[r].style.display = 'none';
	}
}
//(De)select all checkboxes%>	
function AllFiles() {
	for (var x = 0; x < document.FileList.elements.length; x++) {
		var y = document.FileList.elements[x];
		var ytr = y.parentNode.parentNode;
		var check = document.FileList.selall.checked;
		if (y.name == 'selfile' && ytr.style.display != 'none') {
			if (y.disabled != true) {
				y.checked = check;
				if (y.checked == true)
					ytr.className = 'checked';
				else
					ytr.className = 'mouseout';
			}
		}
	}
}

function shortKeyHandler(_event) {
	if (!_event)
		_event = window.event;
	if (_event.which) {
		keycode = _event.which;
	} else if (_event.keyCode) {
		keycode = _event.keyCode;
	}
	var t = document.getElementById("text_Dir");
	//z
	if (keycode == 122) {
		document.getElementById("but_Zip").click();
	}
	//r, F2
	else if (keycode == 113 || keycode == 114) {
		var path = prompt("Please enter new filename", "");
		if (path == null)
			return;
		t.value = path;
		document.getElementById("but_Ren").click();
	}
	//c
	else if (keycode == 99) {
		var path = prompt("Please enter filename", "");
		if (path == null)
			return;
		t.value = path;
		document.getElementById("but_NFi").click();
	}
	//d
	else if (keycode == 100) {
		var path = prompt("Please enter directory name", "");
		if (path == null)
			return;
		t.value = path;
		document.getElementById("but_NDi").click();
	}
	//m
	else if (keycode == 109) {
		var path = prompt("Please enter move destination", "");
		if (path == null)
			return;
		t.value = path;
		document.getElementById("but_Mov").click();
	}
	//y
	else if (keycode == 121) {
		var path = prompt("Please enter copy destination", "");
		if (path == null)
			return;
		t.value = path;
		document.getElementById("but_Cop").click();
	}
	//l
	else if (keycode == 108) {
		document.getElementById("but_Lau").click();
	}
	//Del
	else if (keycode == 46) {
		document.getElementById("but_Del").click();
	}
}
function popUp(URL){
	fname = document.getElementsByName("myFile")[0].value;
	if (fname != "")
		window.open(URL+"?first&uplMonitor="+encodeURIComponent(fname),"","width=400,height=150,resizable=yes,depend=yes")
}
document.onkeypress = shortKeyHandler;