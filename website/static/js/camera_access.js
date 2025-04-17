const captura = document.getElementById('captura-btn');
const grabarBtn = document.getElementById('grabar-btn');
const canva = document.getElementById('foto');
const dimension = canva.getContext('2d');
const video = document.getElementById('camara');
const videoInput = document.getElementById('video-file');
const fotoRutaInput = document.getElementById('foto-file');
const fotoperfil = document.querySelector(".fotoperfil");

let mediaRecorder;
let recordedChunks = [];

captura.addEventListener('click', () => {
    navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then((stream) => {
        video.srcObject = stream;
        video.style.display = "block";
        grabarBtn.style.display = "block";
        captura.style.display = "none";
        fotoperfil.style.display = "none";

        mediaRecorder = new MediaRecorder(stream);
        recordedChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                recordedChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = async () => {
            const blob = new Blob(recordedChunks, { type: "video/webm" });
        
            // Limpiar el src anterior si existía
            if (video.src) {
                URL.revokeObjectURL(video.src);
            }
            const url = URL.createObjectURL(blob);
            video.src = url;
        
            await new Promise((resolve) => {
                video.onloadedmetadata = () => {
                    resolve();
                };
            });
        
            // Asegurarte de que tiene datos válidos
            if (video.videoWidth === 0 || video.videoHeight === 0) {
                console.error("El video no tiene datos válidos.");
                return;
            }
        
            // Capturar la foto actual del video
            canva.width = video.videoWidth;
            canva.height = video.videoHeight;
            dimension.drawImage(video, 0, 0, canva.width, canva.height);
        
            // Crear los archivos nuevos
            const videoFile = new File([blob], "video.webm", { type: "video/webm" });
        
            const fotoBlob = await new Promise((resolve) => {
                canva.toBlob((blobFoto) => {
                    if (!blobFoto) {
                        console.error("Error al capturar la foto con toBlob");
                        return;
                    }
                    resolve(blobFoto);
                }, "image/png");
            });
        
            const fotoFile = new File([fotoBlob], "foto.png", { type: "image/png" });
        
            // Sobrescribir inputs con los nuevos archivos
            const videoTransfer = new DataTransfer();
            videoTransfer.items.add(videoFile);
            videoInput.files = videoTransfer.files;
        
            const fotoTransfer = new DataTransfer();
            fotoTransfer.items.add(fotoFile);
            fotoRutaInput.files = fotoTransfer.files;
        
            console.log("Video y foto actualizados correctamente.");
        };
    })
    .catch((error) => {
        console.error("Error accediendo a la cámara: ", error);
    });
});

grabarBtn.addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state === "inactive") {
        recordedChunks = [];
        mediaRecorder.start();
        grabarBtn.innerText = "Grabando...";
        setTimeout(() => {
            mediaRecorder.stop();
            grabarBtn.innerText = "Iniciar Grabación";
        }, 5000);
    }
});

document.querySelector("form").addEventListener("submit", function(e) {
    const videoFile = videoInput.files[0];
    const fotoRuta = fotoRutaInput.value;

    if (!videoFile || !fotoRuta) {
        e.preventDefault();
        alert("Debes grabar un video y tomar una foto antes de guardar.");
    } else {
        console.log("Formulario listo para enviarse.");

        let formData = new FormData(this);
        formData.set("video-file", videoFile);

        fetch(this.action, {
            method: "POST",
            body: formData
        }) .then(response => {
            if (!response.ok) {
                throw new Error("Error en la solicitud");
            }
            return response.json();
        })
        .then(data => {
            console.log("Respuesta del servidor:", data);
            if (data.Error) {
                alert(JSON.stringify(data.message));
                location.reload(); 
            } else {
                alert(data.message);
                location.reload(); 
            }
        })
        .catch(error => {
            console.error("Error al enviar el formulario:", error);
        });

        e.preventDefault();
    }
});
