/**
 *  author :Komal
 */

/*function removeValues(){
	alert("inside removed values funstion::"+summerId);
	alert("internshipIds::"+summerInternshipId);
	for(var i=0;i<summerId.length;i++){
		if($('#'+summerInternshipId[i]).is(":checked")){
			
		}else{
			alert("inside else condition::")
			summerId.splice( i,summerId[i] );
			alert("after splice")
		}
	}
	alert(summerId);
}*/

function setOtherInternshipValue(count){
	if ($("#otherInternship"+count+"Lock").is(":checked")){
		var idVal = $("#otherHiddenLock"+count).val();
   		$("#otherHiddenLock"+count).val("1");
	}else{
    	var idVal = $("#otherHiddenLock"+count).val();
   		$("#otherHiddenLock"+count).val("0");
    	
	}
}

function setOtherInternshipApprove(count){
	if ($("#otherInternship"+count+"Approve").is(":checked")){
		var idVal = $("#otherHiddenApprove"+count).val();
   		$("#otherHiddenApprove"+count).val("2");
	}else{
    	var idVal = $("#otherHiddenApprove"+count).val();
   		$("#otherHiddenApprove"+count).val("0");
    	
	}
}

function setWorkLockValues(count){
	if ($("#workExperience"+count+"Lock").is(":checked")){
		var idVal = $("#whLock"+count).val();
   		$("#whLock"+count).val("1");
	}else{
    	var idVal = $("#whLock"+count).val();
   		$("#whLock"+count).val("0");
    	
	}
}

function setWorkApproveValue(count){
	if ($("#workExperience"+count+"Approve").is(":checked")){
		var idVal = $("#whApprove"+count).val();
   		$("#whApprove"+count).val("2");
	}else{
    	var idVal = $("#whApprove"+count).val();
   		$("#whApprove"+count).val("0");
    	
	}
}

function setcvApprove(count){
	if ($("#cv"+count+"Approve").is(":checked")){
		var idVal = $("#cvApproveHidden"+count).val();
   		$("#cvApproveHidden"+count).val("2");
	}else{
    	var idVal = $("#cvApproveHidden"+count).val();
   		$("#cvApproveHidden"+count).val("0");
    	
	}
}

function setcvLock(count){
	if ($("#cv"+count+"Lock").is(":checked")){
		var idVal = $("#cvLockHidden"+count).val();
   		$("#cvLockHidden"+count).val("1");
	}else{
    	var idVal = $("#cvLockHidden"+count).val();
   		$("#cvLockHidden"+count).val("0");
    	
	}
}

