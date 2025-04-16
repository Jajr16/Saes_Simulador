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
            const url = URL.createObjectURL(blob);
            video.src = url;
            
            await new Promise((resolve) => {
                video.onloadedmetadata = () => {
                    resolve();
                };
            });

            // Verificar si el video tiene datos antes de capturar la imagen
            if (video.videoWidth === 0 || video.videoHeight === 0) {
                console.error("El video no tiene datos válidos.");
                return;
            }

            // Ajustar el tamaño del canvas al tamaño del video
            canva.width = video.videoWidth;
            canva.height = video.videoHeight;

            // Dibujar el cuadro del video en el canvas
            dimension.drawImage(video, 0, 0, canva.width, canva.height);

            // Capturar la foto
            canva.toBlob((blobFoto) => {
                if (!blobFoto) {
                    console.error("Error al capturar la foto con toBlob, usando toDataURL.");
                    return;
                }

                // Crear archivos para el video y la foto
                const videoFile = new File([blob], "video.webm", { type: "video/webm" });
                const fotoFile = new File([blobFoto], "foto.png", { type: "image/png" });

                // Cargar los archivos en los inputs invisibles
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(videoFile);
                videoInput.files = dataTransfer.files;

                const fotoDataTransfer = new DataTransfer();
                fotoDataTransfer.items.add(fotoFile);
                fotoRutaInput.files = fotoDataTransfer.files;

                console.log("Foto capturada y guardada correctamente.");
            }, "image/png");
        };
    })
    .catch((error) => {
        console.error("Error accediendo a la cámara: ", error);
    });
});

grabarBtn.addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state === "inactive") {
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
        formData.append("video-file", videoFile);

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
                alert(data.message);
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
