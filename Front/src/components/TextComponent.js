import React, { useState, useEffect } from 'react';
import shuffle from 'lodash/shuffle';
import './TextComponent.css';

const TextComponent = () => {
  const [text, setText] = useState(null);
  const [photo, setPhoto] = useState(null);
  const [loading, setLoading] = useState(true);
  const [options, setOptions] = useState([]);
  const [query, setQuery] = useState(null);
  const [randomWord, setRandomWord] = useState(null);

  const fetchRandomWord = async () => {
    const response = await fetch('http://127.0.0.1:8000/palavra-aleatoria');
    const data = await response.json();
    setQuery(data["Palavra em ingles"]);
    const correctAnswer = data["Palavra em portugues"];
    const shuffledAnswers = shuffle([correctAnswer]);
    setOptions(shuffledAnswers);
  };

  const fetchPhoto = async () => {
    setLoading(true);
    const response = await fetch(`https://api.unsplash.com/photos/random?query=${query}&client_id=rX58ilzGPFa7AZUeLrxKgsivcgvKn1sZo5pkg9eDSJo`);
    const data = await response.json();
    setPhoto(data.urls.regular);
    setLoading(false);
  };

  const fetchPhotos = async () => {
    setLoading(true);
    const response = await fetch(`https://api.unsplash.com/photos/random?count=3&client_id=rX58ilzGPFa7AZUeLrxKgsivcgvKn1sZo5pkg9eDSJo`);
    const data = await response.json();
    const shuffledPhotos = shuffle(data.map(photo => photo.urls.regular));
    setOptions(options => options.map((option, index) => {
      if (index === 0) {
        return photo;
      } else {
        return shuffledPhotos[index - 1];
      }
    }));
    setLoading(false);
  };

  useEffect(() => {
    fetchRandomWord();
  }, []);

  useEffect(() => {
    if (query) {
      fetchPhotos();
      fetchPhoto();
    }
  }, [query]);

  const handleOptionClick = (option) => {
    if (option === options[0]) {
      alert('Você acertou!');
    } else {
      alert('Você errou!');
    }

    window.location.reload();
  };

  return (
    <div className="text-box">
      <div className="text" style={{fontSize: '32px', textAlign: 'center', marginBottom: '20px'}}>{randomWord}</div>
      <div className="text-options">
        {options.map((option, index) => (
          <div className="text-option" key={index} onClick={() => handleOptionClick(option)} style={{ backgroundImage: `url(${option})` }}></div>
        ))}
      </div>
    </div>
  );
};

export default TextComponent;
