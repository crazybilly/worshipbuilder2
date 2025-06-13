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
        
        // --- Function to save the state of both lists to the backend ---
const saveListsState = async () => {
    // 1. Get all <li> elements from each list and extract their text content.
    const availableItems = Array.from(availableList.querySelectorAll('li')).map(li => li.id);
    const dropzoneItems = Array.from(dropzoneList.querySelectorAll('li')).map(li => li.id);
    
    // 2. Prepare the data payload for the AJAX request.
    const payload = {
        available: availableItems,
        dropzone: dropzoneItems
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


saveListsState();



// --- Initialize SortableJS for both lists ---
const options = {
    group: 'shared', // This is key! It allows dragging between lists with the same group name.
    animation: 150, // Animation speed in ms.
    // The 'onEnd' event is triggered when a drag-and-drop operation is completed.
    onEnd: function (evt) {
        // We call our save function whenever an item is moved.
        saveListsState();
    }
};

new Sortable(availableList, options);
new Sortable(dropzoneList, options);




  }

})(window, document, undefined);