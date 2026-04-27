const { showElement, hideElement, setButtonState, showToast, showError } =
  await import('./utils.js');
const fetchBtn = document.getElementById('fetch-btn');

let currentUrl = '';
const videoDate = '';
let title = '';
let extension = '';

async function fetchVideoInfo() {
  let inputUrl = document.getElementById('video-url');
  let url = inputUrl.value.trim();
  currentUrl = url;

  if (!url) {
    showToast('Please enter a video URL', 'warning');
    return;
  }
  console.log('fetching video info for url:', url);

  hideElement('video-info-section');
  hideElement('error-alert');
  showElement('loader');
  setButtonState('fetch-btn', true, 'Fetching...');

  try {
    const response = await fetch('/api/video-info', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Received video info:', data);
      displayVideoInfo(data);
    } else {
      const data = await response.json();
      console.error('Error fetching video info:', data.detail);
      throw new Error(data.detail);
    }
  } catch (error) {
    showError(
      error.message ||
        'An error occurred while fetching video info. Please try again.',
    );
  } finally {
    hideElement('loader');
    setButtonState('fetch-btn', false, 'Get Video Info');
  }
}

async function displayVideoInfo(data) {
  showElement('video-info-section');
  document.getElementById('video-thumbnail').src =
    data.thumbnail || 'https://placehold.net/default.png';

  document.getElementById('video-title').textContent =
    data.title || 'Unknown Title';
  document.getElementById('video-uploader').innerHTML =
    `<i class="fa-solid fa-user"></i> ${data.uploader || 'Unknown Uploader'}`;
  document.getElementById('video-duration').innerHTML =
    `<i class="fa-solid fa-stopwatch"></i> ${data.duration || '-- --'}`;
  document.getElementById('video-description').textContent =
    data.description || 'No description available.';

  title = data.title;
  const videoFormatsContainer = document.getElementById('video-formats');
  videoFormatsContainer.innerHTML = '';

  if (data.video_formats && data.video_formats.length > 0) {
    data.video_formats.forEach((format) => {
      const button = createFormatButton(format, 'video');
      videoFormatsContainer.appendChild(button);
    });
  } else {
    videoFormatsContainer.innerHTML =
      '<p class="text-sm text-base-content/50">No video formats available</p>';
  }

  const audioFormatsContainer = document.getElementById('audio-formats');
  audioFormatsContainer.innerHTML = '';

  if (data.audio_formats && data.audio_formats.length > 0) {
    data.audio_formats.forEach((format) => {
      if (format.ext == 'webm') {
        return;
      }
      const button = createFormatButton(format, 'audio');
      audioFormatsContainer.appendChild(button);
    });
  } else {
    audioFormatsContainer.innerHTML =
      '<p class="text-sm text-base-content/50">No audio formats available</p>';
  }
}

function createFormatButton(format, type) {
  const button = document.createElement('button');
  button.className = 'btn btn-outline btn-sm justify-start';
  button.onclick = () => downloadVideo(format.format_id, format.ext);
  const icon =
    type === 'video'
      ? '<i class="fa-solid fa-video"></i>'
      : '<i class="fa-solid fa-music"></i>';
  const audioIndicator = format.has_audio
    ? ' <i class="fa-solid fa-volume-high text-blue-500"></i>'
    : ' <i class="fa-solid fa-volume-xmark text-red-500"></i>';

  if (type === 'video') {
    button.innerHTML = `
        <span class="text-left flex-1">
            ${icon} ${format.label}${audioIndicator}
        </span>
    `;
  } else {
    button.innerHTML = `
        <span class="text-left flex-1">
            ${icon} ${format.label}
        </span>
    `;
  }

  return button;
}

async function downloadVideo(formatId, ext) {
  extension = ext;
  try {
    showToast('Getting download URL...', 'info');
    openModalLoader('show');
    const response = await fetch('/api/get-download-url', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: currentUrl, format_id: formatId }),
    });

    console.log('passing data to modal');

    if (response.ok) {
      const data = await response.json();
      console.log(data);

      openModal(data);
      console.log('Modal opened!');
    } else {
      const data = await response.json();
      console.log(data);

      console.error('Error getting download URL:', data.detail);
      throw new Error(
        data.detail || 'Failed to get download URL. Please try again.',
      );
    }
  } catch (error) {
    openModalLoader();
    document.getElementById("modal")?.close()
    showError(
      error.message ||
        'An error occurred while starting the download. Please try again.'
    );
  }
}

function openModalLoader(state = 'close') {
  const modal = document.getElementById('modal');
  const modalContent = document.getElementById('modal-content');
  modalContent.innerHTML = '';

  if (state === 'show') {
    modalContent.innerHTML = `
    <div id="loader" class="">
      <div class="flex flex-col items-center justify-center py-12">
        <span class="loading loading-spinner loading-lg mb-4"></span>
        <p class="text-lg">Loading...</p>
      </div>
    </div>
  `;
    modal.showModal();
  } else {
    modalContent.innerHTML = `
    <div id="loader" class="hidden">
      <div class="flex flex-col items-center justify-center py-12">
        <span class="loading loading-spinner loading-lg mb-4"></span>
        <p class="text-lg">Loading...</p>
      </div>
    </div>
  `;
  }
}

function openModal(data) {
  // ✅ Convert extension to standard format

  const standardExt = normalizeExtension(extension);

  const response = data;
  const modal = document.getElementById('modal');
  const modalContent = document.getElementById('modal-content');

  openModalLoader();
  // ✅ Clear previous content
  modalContent.innerHTML = '';

  // ✅ Build styled modal content
  modalContent.innerHTML = `
    <div class="mt-2">
        <div class="w-full alert alert-info shadow-lg hidden mb-2.5" id="modalToast">
          <div>
            <span id="modal-toast-content" class="text-center"></span>
          </div>
        </div>
      
        <div class="w-full alert alert-info shadow-lg hidden" id="modalToastCopy">
          <div>
            <span id="modal-copy-toast" class="text-center"></span>
          </div>
        </div>
    </div>

    <!-- Close button -->
    <form method="dialog">
      <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
    </form>
    
    <!-- Success Icon -->
    <div class="flex justify-center mb-4">
      <div class="w-16 h-16 bg-success/20 rounded-full flex items-center justify-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-success" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
      </div>
    </div>
    
    <!-- Title -->
    <h3 class="font-bold text-xl text-center mb-2">Download Ready!</h3>
    
    <!-- Video Title -->
    <div class="bg-base-200 p-3 rounded-lg mb-4">
      <p class="text-sm font-semibold text-center wrap-break-words">${escapeHtml(title)}</p>
      <p class="text-xs text-center text-base-content/60 mt-1">Format: ${standardExt.toUpperCase()}</p>
    </div>
    
    <!-- Download Button -->
    <a href="${response.download_url}" 
       download="${sanitizeFilename(title)}.${standardExt}"
       class="btn btn-primary btn-lg btn-block mb-4">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
      </svg>
      Download ${standardExt.toUpperCase()}
    </a>
    
    <!-- Divider -->
    <div class="divider">Support Us</div>
    
    <!-- Thank You Message -->
    <div class="bg-primary/10 border border-primary/20 rounded-lg p-4 mb-4">
      <p class="text-sm text-center">
        💙 Thank you for using EagleFetchIt! If you found this helpful, please share our website with your friends.
      </p>
    </div>
    
    <!-- Share Buttons -->
    <div class="flex gap-2 justify-center">
      <button onclick="shareLink()" id="share-btn" class="btn btn-sm btn-outline">
        Share
      </button>
      
      <button onclick="copyLink()" id="share-link" class="btn btn-sm btn-outline">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
        </svg>
        Copy Link
      </button>
    </div>
  `;

  modal.showModal();
}

// ✅ Extension normalization
function normalizeExtension(ext) {
  console.log('ext:', ext);

  if (!ext) return 'mp4';

  if (ext === 'mp4' || ext === 'mp3') {
    return ext;
  }

  // Video extensions → mp4
  const videoExts = ['webm', 'mkv', 'avi', 'mov', 'flv', '3gp'];
  if (videoExts.includes(ext)) {
    return 'mp4';
  }

  // Audio extensions → mp3
  const audioExts = ['m4a', 'aac', 'ogg', 'opus', 'flac', 'wav'];
  if (audioExts.includes(ext)) {
    return 'mp3';
  }
  return 'mp4';
}

// ✅ Sanitize filename (remove invalid characters)
function sanitizeFilename(filename) {
  return filename
    .replace(/[<>:"/\\|?*]/g, '') // Remove invalid chars
    .replace(/\s+/g, ' ') // Normalize whitespace
    .trim()
    .substring(0, 200); // Limit length
}

// ✅ Escape HTML to prevent XSS
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

window.copyLink = function () {
  const modalContent = document.getElementById('modal-copy-toast');
  navigator.clipboard.writeText(window.location.origin);
  showElement('modalToastCopy');
  modalContent.innerHTML = 'Link copied to clipboard!';
  setTimeout(() => {
    hideElement('modalToastCopy');
    modalContent.innerHTML = '';
  }, 5000);
};

window.shareLink = async function () {
  const modalContent = document.getElementById('modal-toast-content');
  if (!navigator.share) {
    copyLink();
    showElement('modalToast');
    modalContent.innerHTML =
      'Your browser does not allow sharing, link is copied to clipboard!';
    setTimeout(() => {
      hideElement('modalToast');
      modalContent.innerHTML = '';
    }, 5000);
    console.log('cannot share');
    return;
  }

  try {
    const shareData = {
      title: 'EagleFetchIt',
      text: 'I just downloaded a video using EagleFetchIt! Check it out:',
      url: window.location.origin,
    };
    await navigator.share(shareData);
  } catch (error) {
    showError(error);
  }
};

fetchBtn.addEventListener('click', fetchVideoInfo);
document.getElementById('video-url')?.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    fetchVideoInfo();
  }
});
