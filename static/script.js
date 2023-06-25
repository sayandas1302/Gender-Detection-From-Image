document.getElementById("uploadForm").addEventListener("submit", function(event) {
	var fileInput = document.getElementById("fileInput");
	var file = fileInput.files[0];
	
	if (!file) {
	  event.preventDefault();
	  alert("No file selected.");
	  return;
	}
	
	var allowedExtensions = /(\.jpg|\.png)$/i;
	if (!allowedExtensions.exec(file.name)) {
	  event.preventDefault();
	  alert("Please select a file in JPG or PNG format.");
	  return;
	}
	
	var fileSize = file.size / 1024 / 1024; // File size in MB
	if (fileSize > 10) {
	  event.preventDefault();
	  alert("File size should be less than or equal to 10MB.");
	  return;
	}
  });
  