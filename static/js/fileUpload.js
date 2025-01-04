const fileList = document.getElementById("fileList");
const fileInput = document.getElementById("fileInput");
const uploadButton = document.getElementById("uploadButton");
const successMessage = document.getElementById("successMessage");
const errorMessage = document.getElementById("errorMessage");

let pendingFiles = [];

// Function to render the file list
function renderFileList() {
  fileList.innerHTML = "";

  // Show or hide the file list based on the number of files
  if (pendingFiles.length > 0) {
    fileList.classList.remove("hidden");
  } else {
    fileList.classList.add("hidden");
  }

  pendingFiles.forEach((file, index) => {
    const fileItem = document.createElement("div");
    fileItem.className = "file-item";
    fileItem.innerHTML = `
        <span class="file-name">${file.name}</span>
        <span class="remove-btn" onclick="removeFile(${index})">&times;</span>
      `;
    fileList.appendChild(fileItem);
  });
}

// Function to remove a file from the pending list
function removeFile(index) {
  pendingFiles.splice(index, 1);
  renderFileList();
}

// Add files to the pending list when selected
fileInput.addEventListener("change", () => {
  const files = Array.from(fileInput.files);

  // Check the number of files
  if (pendingFiles.length + files.length > 10) {
    errorMessage.innerHTML = `<div class="alert alert-danger" role="alert">
        You can upload a maximum of 10 files at a time.
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>`;
    hideMessageAfterTime(errorMessage);
    return;
  }

  // Add selected files to the pending list
  pendingFiles = pendingFiles.concat(files);
  renderFileList();
  fileInput.value = ""; // Clear the file input
});

// Upload all files
uploadButton.addEventListener("click", async () => {
  if (pendingFiles.length === 0) {
    errorMessage.innerHTML = `<div class="alert alert-danger" role="alert">
        No files to upload.
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>`;
    hideMessageAfterTime(errorMessage);
    return;
  }

  const formData = new FormData();
  pendingFiles.forEach((file) => formData.append("file", file));

  try {
    const response = await fetch("/api/upload/", {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
          .value,
      },
    });

    const data = await response.json();

    if (data.success) {
      successMessage.innerHTML = `
          <div class="alert alert-success alert-dismissible fade show" role="alert">
            ${data.message}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
        `;
      hideMessageAfterTime(successMessage);
      pendingFiles = [];
      renderFileList();
    } else {
      errorMessage.innerHTML = `
          <div class="alert alert-danger alert-dismissible fade show" role="alert">
            ${data.errors.join("<br>")}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
        `;
      hideMessageAfterTime(errorMessage);
    }
  } catch (error) {
    console.error("Error:", error);
    errorMessage.innerHTML = `
        <div class="alert alert-danger" role="alert">
          Error uploading files.
          <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
      `;
    hideMessageAfterTime(errorMessage);
  }
});

// Function to hide messages after a timeout
function hideMessageAfterTime(element) {
  setTimeout(() => {
    element.innerHTML = "";
  }, 5000); // 5 seconds delay
}
