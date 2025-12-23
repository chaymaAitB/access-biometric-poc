const video = document.getElementById('video');

async function startVideo() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: {} });
    video.srcObject = stream;
}

async function loadModels() {
    await faceapi.nets.tinyFaceDetector.loadFromUri('/static/models');
}

async function startFaceDetection() {
    await loadModels();
    startVideo();

    video.addEventListener('play', () => {
        setInterval(async () => {
            const detections = await faceapi.detectAllFaces(
                video,
                new faceapi.TinyFaceDetectorOptions()
            );

            if (detections.length > 0) {
                // Redirige vers la page principale avec succès
                window.location.href = "/?result=success";
            } else {
                // Si aucun visage détecté, accès refusé
                window.location.href = "/?result=fail";
            }
        }, 3000);
    });
}