function sendMessage(msg) {
  chrome.runtime.sendMessage(msg);
}
function handleMessage(message) {
  console.log(message);
  switch (message.command) {
    case "rec_getSettings":
      oldUid = message.data.uid;
      oldEmail = message.data.email;
      oldCountry = message.data.country;
      oldRecheck = message.data.dontRecheck;

      recordsInput.value = message.data.postedRecordCount;
      emailInput.value = oldEmail;
      countryInput.value = oldCountry;
      //dontRecheckInput.checked = oldRecheck;
      break;
  }
}
chrome.runtime.onMessage.addListener(handleMessage);

var messageDiv      = document.querySelector("#message");
var recordsInput    = document.querySelector("#posted_records");
var emailInput      = document.querySelector("#email");
var dontRecheckInput= document.querySelector("#dontRecheck");
var countryInput    = document.querySelector("#country");
var termsInput      = document.querySelector("#terms");

var oldEmail="", oldEmail="", oldUid=0;oldRecheck=false;

function showMessage(msg, type){
  messageDiv.className = "alert alert-" + type;
  messageDiv.innerHTML = "<strong>" + msg + "</strong>";
  messageDiv.style.display = "block";
}
document.querySelector("#btnSave").onclick = function(){
  var email     = emailInput.value;
  var country   = countryInput.value;
  var dontRecheck = dontRecheckInput.checked;
  var terms = termsInput.checked;
  
  if(country == ""){
    email.parentNode.classList.add("has-error");
    return false;
  }
  
  if(terms == false){
    showMessage("You are required to agree to terms before proceeding..", "danger");
    return false;
  }
  
  if(email == oldEmail && country == oldCountry){
    if(dontRecheck == false)
      showMessage("We have saved this info and you will be asked to validate this again after one week, unless you have checked that box", "success");
    else
      showMessage("We have saved this info and you will NEVER be asked to validate this again.", "success");
    sendMessage({
      "command":"saveUid",
      "data" : {
        "uid"       : oldUid,
        "email"     : email,
        "country"   : country,
        "dontRecheck" : dontRecheck,
        "timestamp" : (new Date().getTime())
      }
    });      
      
    return false;
  }
  
  // else now get a new UID
  showMessage("Please wait while we are validating..", "info");
  
  var xmlhttp = new XMLHttpRequest;
  var authUrl = "http://kiarash.scripts.mit.edu/blockedonline_debug/load";
  var authData = JSON.stringify({
    "email": email,
    "country" : country
  });
  xmlhttp.open("POST", authUrl, true);
  xmlhttp.setRequestHeader("Content-Type", "application/json");
  xmlhttp.onreadystatechange = function () {
    if (xmlhttp.readyState == 4) {
      if(xmlhttp.status == 200){
        console.log(this.responseText);
        var r = JSON.parse(this.responseText);
        
        if(r.uid){
          showMessage("We have saved this info.", "success");
          sendMessage({
            "command":"saveUid",
            "data" : {
              "uid"       : r.uid,
              "email"     : emailInput.value,
              "country"   : countryInput.value,
              "dontRecheck" : dontRecheckInput.checked,
              "timestamp" : (new Date().getTime())
            }
          });
        }else{
          showMessage("Please try again..", "danger");
        }
      }else{
        showMessage("Please try again..", "danger");
      }
    }
  }
  xmlhttp.send(authData ? authData : null);
  return false;
}

document.querySelector("#btnClose").onclick = function(){window.close(); return false}
sendMessage({"command":"getSettings"});      