document.addEventListener("DOMContentLoaded", function() {
    const assignButton = document.getElementById("assign-button");
    const unassignButton = document.getElementById("unassign-button");
    const restoreButton = document.getElementById("restore-button");
    const availablePersonnel = document.getElementById("available-personnel");
    const assignedPersonnel = document.getElementById("assigned-personnel");
  
    assignButton.addEventListener("click", function() {
      moveSelectedOptions(availablePersonnel, assignedPersonnel);
    });
  
    unassignButton.addEventListener("click", function() {
      moveSelectedOptions(assignedPersonnel, availablePersonnel);
    });
  
    restoreButton.addEventListener("click", function() {
      moveAllOptions(assignedPersonnel, availablePersonnel);
    });
  
    function moveSelectedOptions(source, destination) {
      Array.from(source.selectedOptions).forEach(option => {
        destination.appendChild(option);
      });
    }
  
    function moveAllOptions(source, destination) {
      Array.from(source.options).forEach(option => {
        destination.appendChild(option);
      });
    }
  });