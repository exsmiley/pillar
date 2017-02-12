// function openTab(evt, tabName) {
//     // Declare all variables
//     var i, tabcontent, tablinks;

//     // Get all elements with class="tabcontent" and hide them
//     // Get all elements with class="tablinks" and remove the class "active"
//     // active = document.getElementsByClassName("active");
//     // for (i = 0; i < active.length; i++) {
//     //     active[i].className = active[i].className.replace("tablinks", "");
//     // }

//     tabcontent = document.getElementsByClassName("tabcontent");
//     for (i = 0; i < tabcontent.length; i++) {
//         tabcontent[i].style.display = "none";
//     }

//     // Get all elements with class="tablinks" and remove the class "active"
//     tablinks = document.getElementsByClassName("tablinks");
//     for (i = 0; i < tablinks.length; i++) {
//         tablinks[i].className = tablinks[i].className.replace(" active", "");
//     }

//     // Show the current tab, and add an "active" class to the link that opened the tab
//     document.getElementById(tabName).style.display = "block";
//     evt.currentTarget.className += " active";
// }

// $(document).ready(function(){
//     document.getElementById('Current').style.display = "block";
//     evt.currentTarget.className += " active";
// })
