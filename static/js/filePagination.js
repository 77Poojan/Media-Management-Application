let previousLink = null;
let nextLink = null;

// Function to fetch and display files
function loadFiles(url = "/api/file-list/") {
  fetch(url)
    .then((response) => {
      if (!response.ok)
        throw new Error(`HTTP error! Status: ${response.status}`);
      return response.json();
    })
    .then((data) => {
      if (data.results && Array.isArray(data.results)) {
        displayFilesInTable(data.results); // Display the files
        updatePagination(data.previous, data.next); // Update the pagination controls
      } else {
        displayError("Invalid data format received from the server.");
      }
    })
    .catch((error) => {
      console.error("Error fetching files:", error);
      displayError("An error occurred while fetching files: " + error.message);
    });
}

// Function to display files in the table
function displayFilesInTable(files) {
  const fileTableBody = document.getElementById("fileTableBody");
  fileTableBody.innerHTML = ""; // Clear existing rows

  files.forEach((file) => {
    const row = document.createElement("tr");

    // Determine the file type and how to display it in the preview
    let filePreview = "";
    if (file.file_type.startsWith("image/")) {
      filePreview = `<img src="${file.download_url}" alt="${file.file_name}" style="max-width: 50px; max-height: 50px; object-fit: contain;" class="preview-file" onclick="openPreviewModal('${file.download_url}', 'image')">`;
    } else if (file.file_type.startsWith("video/")) {
      filePreview = `
        <video style="max-width: 50px; max-height: 50px; cursor: pointer;" 
              class="preview-file" 
              muted 
              autoplay 
              loop 
              onclick="openPreviewModal('${file.download_url}', 'video')">
          <source src="${file.download_url}" type="${file.file_type}">
          Your browser does not support the video tag.
        </video>`;
    } else if (file.file_type.startsWith("audio/")) {
      filePreview = `<i class="fas fa-volume-up" style="cursor: pointer; font-size: 24px;" onclick="openPreviewModal('${file.download_url}', 'audio')"></i>`;
    } else {
      filePreview = "No preview available";
    }

    row.innerHTML = `
      <td style="display: flex; align-items: center;">
        ${filePreview} <!-- File Preview -->
        <span style="margin-left: 10px;">${
          file.file_name.split("/")[1]
        }</span> <!-- File Name -->
      </td>
      <td>${(file.file_size / 1024).toFixed(2)} KB</td>
      <td>${file.file_type.split("/")[1] || "N/A"}</td>
      <td>${file.category || "N/A"}</td>
      <td>${new Date(file.uploaded_at).toLocaleString()}</td>
      <td>
        <button class="btn btn-primary btn-sm" onclick="downloadFile('${
          file.download_url
        }')">
          <i class="fas fa-download"></i>
        </button>
        <button class="btn btn-danger btn-sm" onclick="deleteFile(${file.id})">
          <i class="fas fa-trash-alt"></i>
        </button>
      </td>
    `;
    fileTableBody.appendChild(row);
  });
}

// Function to update pagination controls
function updatePagination(previous, next) {
  previousLink = previous;
  nextLink = next;

  const previousButton = document.getElementById("previousButton");
  const nextButton = document.getElementById("nextButton");

  if (previous) {
    previousButton.disabled = false;
  } else {
    previousButton.disabled = true;
  }

  if (next) {
    nextButton.disabled = false;
  } else {
    nextButton.disabled = true;
  }
}

// Function to display error messages
function displayError(message) {
  const errorMessage = document.getElementById("errorMessage");
  errorMessage.innerHTML = `
    <div class="alert alert-danger alert-dismissible fade show" role="alert">
      ${message}
      <button type="button" class="close" onclick="closeAlert(this)">&times;</button>
    </div>
  `;
  // Hide the alert after 5 seconds
  setTimeout(() => {
    errorMessage.innerHTML = "";
  }, 5000);
}

// Function to close the alert
function closeAlert(button) {
  const alert = button.closest(".alert");
  alert.remove();
}

// Event Listeners for Pagination Buttons
document.getElementById("previousButton").addEventListener("click", () => {
  if (previousLink) {
    loadFiles(previousLink);
  }
});

document.getElementById("nextButton").addEventListener("click", () => {
  if (nextLink) {
    loadFiles(nextLink);
  }
});

// Function to handle file download
function downloadFile(fileUrl) {
  const link = document.createElement("a");
  link.href = fileUrl;
  link.download = "";
  setTimeout(() => {
    link.click();
  }, 250);
}

// Function to handle file deletion
function deleteFile(fileId) {
  if (confirm(`Are you sure you want to delete this file?`)) {
    fetch(`/api/delete-file/${fileId}`, {
      method: "DELETE",
    })
      .then((response) => {
        if (!response.ok)
          throw new Error(`Failed to delete file: ${response.status}`);
        loadFiles(); // Reload the files
      })
      .catch((error) => {
        displayError(
          "An error occurred while deleting the file: " + error.message
        );
      });
  }
}

// Function to open the preview modal
// function openPreviewModal(fileUrl, fileType) {
//   console.log(fileUrl, fileType);
//   const previewContainer = document.getElementById("filePreviewContainer");
//   let previewContent = "";

//   // Display the appropriate preview based on file type
//   if (fileType === "image") {
//     previewContent = `<img src="${fileUrl}" alt="Image preview" style="max-width: 100%; max-height: 100%;">`;
//   } else if (fileType === "video") {
//     previewContent = `
//       <video controls style="max-width: 100%; max-height: 100%;">
//         <source src="${fileUrl}" type="video/mp4">
//         Your browser does not support the video tag.
//       </video>`;
//   } else if (fileType === "audio") {
//     previewContent = `
//       <audio controls style="max-width: 100%;">
//         <source src="${fileUrl}" type="audio/mpeg">
//         Your browser does not support the audio element.
//       </audio>`;
//   }

//   previewContainer.innerHTML = previewContent;
//   $("#filePreviewModal").modal("show"); // Assuming jQuery is used for modal
// }

// Load the first page on page load
document.addEventListener("DOMContentLoaded", () => {
  loadFiles();
});

// Reload Table from page 1
function reloadTable() {
  previousLink = null;
  nextLink = null;

  const fileTableBody = document.getElementById("fileTableBody");
  fileTableBody.innerHTML = "";

  loadFiles("/api/file-list/");
}

// Event Listener for the Reload Button
document.getElementById("reloadIcon").addEventListener("click", () => {
  reloadTable();
});

// Function to open the preview modal and play the media
function openPreviewModal(fileUrl, fileType) {
  const previewContainer = document.getElementById("filePreviewContainer");
  let previewContent = "";

  // Determine media type and create appropriate HTML
  if (fileType === "image") {
    previewContent = `<img src="${fileUrl}" alt="Image preview" style="max-width: 100%; max-height: 100%;">`;
  } else if (fileType === "video") {
    previewContent = `
      <video id="modalMedia" controls style="width: 100%; max-height: 100%;">
        <source src="${fileUrl}" type="video/mp4">
        Your browser does not support the video tag.
      </video>`;
  } else if (fileType === "audio") {
    previewContent = `
      <audio id="modalAudio" controls style="width: 100%;">
        <source src="${fileUrl}" type="audio/mp3">
        Your browser does not support the audio element.
      </audio>`;
  } else {
    previewContent = "Preview not available for this file type.";
  }

  // Update the modal content and show it
  previewContainer.innerHTML = previewContent;
  $("#filePreviewModal").modal("show");

  // Automatically play the media after the modal opens
  $("#filePreviewModal").on("shown.bs.modal", function () {
    const mediaElement = document.getElementById("modalMedia");
    const audioElement = document.getElementById("modalAudio");

    // Play video or audio automatically after the modal opens
    if (mediaElement) {
      mediaElement.play().catch((error) => {
        console.warn("Autoplay prevented by browser policy:", error);
      });
    } else if (audioElement) {
      audioElement.play().catch((error) => {
        console.warn("Autoplay prevented by browser policy:", error);
      });
    }
  });

  // Pause media when the modal is closed
  $("#filePreviewModal").on("hidden.bs.modal", function () {
    const mediaElement = document.getElementById("modalMedia");
    const audioElement = document.getElementById("modalAudio");

    if (mediaElement) {
      mediaElement.pause();
      mediaElement.currentTime = 0;
    } else if (audioElement) {
      audioElement.pause();
      audioElement.currentTime = 0;
    }
  });
}

// Function to toggle play/pause for audio or video
function toggleMedia(type) {
  let mediaElement, toggleButton;

  if (type === "audio") {
    mediaElement = document.getElementById("modalAudio");
    toggleButton = document.getElementById("toggleAudio");
  } else if (type === "video") {
    mediaElement = document.getElementById("modalMedia");
    toggleButton = document.getElementById("toggleVideo");
  }

  if (mediaElement.paused) {
    mediaElement.play();
  } else {
    mediaElement.pause();
  }
}
