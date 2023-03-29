import { useRef, useEffect, useState } from "react";
import './WebCamComponent.css'

function WebCamComponent() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [showButton, setShowButton] = useState(true);
  const [requestInProgress, setRequestInProgress] = useState(false);
  const [query, setQuery] = useState('');
  const [label, setLabel] = useState('');
  const [photo, setPhoto] = useState('');
  const [loading, setLoading] = useState(false);

  const startCapture = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
    } catch (error) {
      console.error(error);
    }
  };

  const stopCapture = () => {
    const stream = videoRef.current.srcObject;
    if (stream) {
      const tracks = stream.getTracks();
      tracks.forEach((track) => {
        track.stop();
      });
    }
    videoRef.current.srcObject = null;
  };

  const fetchRandomWord = async () => {
    const response = await fetch('http://127.0.0.1:8000/palavra-aleatoria');
    const data = await response.json();
    setQuery(data["Palavra em ingles"]);
    setLabel(data["Palavra em portugues"]);
  };

  const fetchPhoto = async () => {
    setLoading(true);
    const response = await fetch(`https://api.unsplash.com/photos/random?query=${query}&client_id=_APIKEY_`);
    const data = await response.json();
    setPhoto(data.urls.regular);
    setLoading(false);
  };

  const captureImage = async () => {
    if (!requestInProgress) {
      setShowButton(false);
      const video = videoRef.current;
      const canvas = canvasRef.current;
      if (video && canvas) {
        const context = canvas.getContext("2d");
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        canvas.toBlob(async (blob) => {
          await sendRequest(blob);
        }, "image/jpeg");
      }
    }
  };

  const sendRequest = async (imageBlob) => {
    const formData = new FormData();
    formData.append("file", imageBlob,"image.jpg");
    formData.append("label", label);
    formData.append("flag", '1');

    try {
      setRequestInProgress(true);
      const response = await fetch("http://127.0.0.1:8000/Sign-Verify/", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      console.log(data);
      if (response.ok && data['message'] === label) {
        alert("Resposta Certa");
        setShowButton(true);
        fetchRandomWord();
        fetchPhoto();
      } else {
        alert("Resposta Errada");
        setShowButton(true);
      }
    } catch (error) {
      console.error(error);
      alert("Erro ao cortar foto");
      setShowButton(true);
    } finally {
      setRequestInProgress(false);
    }
  };

  useEffect(() => {
    fetchRandomWord();
    startCapture();
    return stopCapture;
  }, []);
  useEffect(() => {
    if (query) {
      fetchPhoto();
    }
  }, [query]);
  return (
    <div className="webcam-container">
      <div className="photo-box">
        <img src={photo} alt="Unsplash" className="photo" />
      </div>
      
      <div className="webcam-box">
        <video ref={videoRef}  className="video"></video>
        {showButton && <button onClick={captureImage} className="capture-button">Capture Image</button>}
        <canvas ref={canvasRef} style={{ display: "none" }}></canvas>
      </div>
    </div>
  );
};

export default WebCamComponent;
