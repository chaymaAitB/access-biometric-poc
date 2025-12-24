const video = document.getElementById('video');
const overlay = document.getElementById('overlay');
let attempts = 0;
const maxAttempts = 10; // 10 seconds timeout

async function startVideo() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: {} });
        video.srcObject = stream;
    } catch (err) {
        console.error("Error accessing webcam:", err);
        alert("Impossible d'accéder à la webcam. Vérifiez vos permissions.");
    }
}

async function loadModels() {
    await faceapi.nets.tinyFaceDetector.loadFromUri('/static/models');
}

async function startFaceDetection() {
    attempts = 0;
    
    const btn = document.querySelector('button[onclick="startFaceDetection()"]');
    if(btn) {
        btn.disabled = true;
        btn.innerText = "Analyse en cours...";
    }

    await loadModels();
    await startVideo();

    video.addEventListener('play', () => {
        // Setup canvas for drawing
        const displaySize = { width: video.width, height: video.height };
        faceapi.matchDimensions(overlay, displaySize);

        const intervalId = setInterval(async () => {
            const detections = await faceapi.detectAllFaces(
                video,
                new faceapi.TinyFaceDetectorOptions()
            );

            // Resize detections to match display size
            const resizedDetections = faceapi.resizeResults(detections, displaySize);
            
            // Clear previous drawings
            overlay.getContext('2d').clearRect(0, 0, overlay.width, overlay.height);
            
            // Draw detections box
            faceapi.draw.drawDetections(overlay, resizedDetections);

            if (detections.length > 0) {
                // Visual success feedback before redirect
                overlay.getContext('2d').strokeStyle = '#00ff00';
                overlay.getContext('2d').lineWidth = 5;
                overlay.getContext('2d').strokeRect(0, 0, overlay.width, overlay.height);
                
                setTimeout(() => {
                    clearInterval(intervalId);
                    window.location.href = "/?result=success";
                }, 1000); // 1s delay to see the green box
                
            } else {
                attempts++;
                console.log(`Tentative ${attempts}/${maxAttempts}: Visage non détecté...`);
                
                if (attempts >= maxAttempts) {
                    clearInterval(intervalId);
                    window.location.href = "/?result=fail";
                }
            }
        }, 500); // Check every 500ms for smoother UI
    });
}
