document.getElementById('download-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const urlInput = document.getElementById('spotify-url');
  const progressDiv = document.getElementById('progress');
  const resultDiv = document.getElementById('result');
  progressDiv.textContent = 'Starting download...';
  resultDiv.innerHTML = '';

  try {
    const response = await fetch('/download', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ spotify_url: urlInput.value })
    });

    if (!response.ok) {
      throw new Error('Download failed');
    }

    const data = await response.json();

    if (data.error) {
      progressDiv.textContent = '';
      resultDiv.textContent = 'Error: ' + data.error;
      return;
    }

    progressDiv.textContent = '';
    // Show result page content dynamically
    const songInfoHtml = `
      <img src="${data.cover_url}" alt="Cover" />
      <h2>${data.title}</h2>
      <h3>${data.artist}</h3>
    `;
    resultDiv.innerHTML = songInfoHtml + `<a href="${data.download_url}" download>Download MP3</a>`;
  } catch (error) {
    progressDiv.textContent = '';
    resultDiv.textContent = 'Error: ' + error.message;
  }
});
