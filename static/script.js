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


var newset_date = document.getElementById("newset_date");
newset_date.value = today_str;


var modal_setcreator  = document.getElementById("newsetpicker");
modal_setcreator.style.display = "none";


var newsetbutton2 = document.getElementById("newsetbutton2");

newsetbutton2.onclick = function() {
  if (modal_setcreator.style.display == "block") {
    modal_setcreator.style.display = "none";
  } else { 
    modal_setcreator.style.display = "block";
  }
}

window.onclick = function(event) {
  if (event.target == modal_setcreator) {
    modal_setcreator.style.display = "none";
  }
}


// --- Drag and Drop Support ---

const availableList = document.getElementById('all_songs');
const dropzoneList = document.getElementById('the_set');

// --- Function to show a brief "Saved" message ---
const showSavedMessage = () => {
    const statusDiv = document.getElementById('status');
    statusDiv.classList.add('visible');
    setTimeout(() => {
        statusDiv.classList.remove('visible');
    }, 1500); // Message disappears after 1.5 seconds
};
        

const the_message = document.getElementById('message');
const the_message_str = the_message.textContent;

if(the_message_str.length == 0 ){
  the_message.style.display = 'none';
  the_message.classList.add('hidden');
} else {
  the_message.style.display = 'block !important';
}

setTimeout(() => {
  the_message.style.display = 'none'; 
}, 3000); // Message disappears after 1.5 seconds




function dynamicSort(property) {
    var sortOrder = 1;
    if(property[0] === "-") {
        sortOrder = -1;
        property = property.substr(1);
    }
    return function (a,b) {
        /* next line works with strings and numbers, 
         * and you may want to customize it to your needs
         */
        var result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
        return result * sortOrder;
    }
  }


        // --- Function to save the state of both lists to the backend ---
const saveListsState = async () => {
    // 1. Get all <li> elements from each list and extract their text content.
    const availableItems = Array.from(availableList.querySelectorAll('li')).map(li => li.id);
    const dropzoneItems = Array.from(dropzoneList.querySelectorAll('li')).map(li => li.id);
    const the_selected_set = document.getElementById('set_selector').value;
    
    // 2. Prepare the data payload for the AJAX request.
    const payload = {
        available: availableItems,
        dropzone: dropzoneItems,
        the_selected_set: the_selected_set
    };

    console.log('Sending data to server:', payload);

    // 3. Send the data to the Flask backend using the Fetch API.
    try {
        const response = await fetch('/save_sets', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log('Server response:', result);
        showSavedMessage(); // Show visual feedback on success

    } catch (error) {
        console.error('Error saving lists:', error);
        // Here you could show an error message to the user
    }
};



// --- Initialize SortableJS for both lists ---
const options = {
    group: 'shared', // This is key! It allows dragging between lists with the same group name.
    animation: 150, // Animation speed in ms.
    // The 'onEnd' event is triggered when a drag-and-drop operation is completed.
    onEnd: function (evt) {
        // We call our save function whenever an item is moved.
        saveListsState();

      // if ended in the availableList then
      //       sort availableList
      //       remove duplicates
      // consider using 
      //      evt.item;  // dragged HTMLElement
		  //      evt.to;    // target list
      if(evt.to == availableList) {
        console.log('you dropped onto the song list');
        dragged_song = evt.item;
        newly_available_ids = Array.from(availableList.querySelectorAll('li')).map(li => li.id);

        filtered_array = newly_available_ids.filter(the_id => the_id == dragged_song.id)
        if (filtered_array.length > 1 ){
            dragged_song.style.display = 'none';
        }
      } 
    }
};

new Sortable(availableList, options);
new Sortable(dropzoneList, options);





the_songs_ul= document.getElementById('all_songs');
the_song_lis = the_songs_ul.getElementsByTagName('li');

var current_letter = '';
var first_letter_songs = [];
for (i = 0; i < the_song_lis.length; i++) {

  the_song_name = the_song_lis[i].textContent.trim();
  first_letter = the_song_name[0];
  if (first_letter != current_letter) { 

      // first_letter_songs.push(the_song_lis[i]);

      the_heading = document.createElement('h3');
      the_heading_content = document.createTextNode(first_letter);
      the_heading.appendChild(the_heading_content);
      

      the_song_lis[i].before(the_heading);
  }
  current_letter = first_letter;
}







  }

})(window, document, undefined);




// -- Search songs --------------

function filterSongs() {
  // Declare variables
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById('songsearch');
  filter = input.value.toUpperCase();
  ul = document.getElementById("all_songs");
  li = ul.getElementsByTagName('li');
  h3s = ul.getElementsByTagName('h3');


  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < li.length; i++) {
    txtValue = li[i].textContent || li[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }

  li_array = Array.from(li);
  visible_lis = li_array.filter(element => element.offsetParent !== null);
  n_visible = visible_lis.length;

  for (i = 0; i < h3s.length; i++) {
    if (n_visible <= 25) {
      h3s[i].style.display = "none";
    } else {
      h3s[i].style.display = "";
    }
  }

};
