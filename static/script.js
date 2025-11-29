document.addEventListener('DOMContentLoaded', () => {
    const speakBtn = document.getElementById('speakBtn');
    const textInput = document.getElementById('textInput');
    const audioPlayer = document.getElementById('audioPlayer');
    const audioContainer = document.getElementById('audioContainer');
    const statusMessage = document.getElementById('statusMessage');
    const loader = document.querySelector('.loader');
    const btnText = document.querySelector('.btn-text');

    speakBtn.addEventListener('click', async () => {
        const text = textInput.value.trim();

        if (!text) {
            showStatus('Please enter some text.', 'error');
            return;
        }

        setLoading(true);
        showStatus('');
        audioContainer.style.display = 'none';

        try {
            const response = await fetch('/synthesize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text }),
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.error || 'Failed to synthesize speech');
            }

            const blob = await response.blob();
            const url = URL.createObjectURL(blob);

            audioPlayer.src = url;
            audioContainer.style.display = 'block';
            audioPlayer.play();

        } catch (error) {
            showStatus(error.message, 'error');
        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        speakBtn.disabled = isLoading;
        if (isLoading) {
            loader.style.display = 'inline-block';
            btnText.textContent = 'Generating...';
        } else {
            loader.style.display = 'none';
            btnText.textContent = 'Speak';
        }
    }

    function showStatus(message, type = 'info') {
        statusMessage.textContent = message;
        statusMessage.className = type;
    }
});
