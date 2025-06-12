(function(window, document, undefined) {

  // code that should be taken care of right away

  window.onload = init;

  function init(){
    // the code to be called when the dom has loaded
    // #document has its nodes


const today = new Date();
var year = today.getFullYear().toString(); // Gets the four-digit year (e.g., 2025)
var month = today.getMonth();
month = month + 1;
month = month.toString().padStart(2,'0'); // Gets the month as a number (0-11, where 0 is January)
var day = today.getDate().toString().padStart(2,'0'); // Gets the day of the month (1-31)
var today_str = year + '-' + month + '-' + day
console.log(today_str)


var newset_date = document.getElementById("newset_date");
newset_date.value = today_str;

var modal        = document.getElementById("newsetpicker");
  modal.style.display = "none";
var newsetbutton = document.getElementById("newsetbutton");

newsetbutton.onclick = function() {
  if (modal.style.display == "block") {
    modal.style.display = "none";
  } else { 
    modal.style.display = "block";
  }

}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}





  }

})(window, document, undefined);