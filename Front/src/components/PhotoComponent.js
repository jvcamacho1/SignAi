import React, { useState, useEffect } from 'react';
import shuffle from 'lodash/shuffle';
import './PhotoComponent.css';

const PhotoComponent = () => {
  const [photo, setPhoto] = useState(null);
  const [loading, setLoading] = useState(true);
  const [options, setOptions] = useState([]);
  const [query, setQuery] = useState(null);

  const fetchRandomWord = async () => {
    const response = await fetch('http://127.0.0.1:8000/palavra-aleatoria');
    const data = await response.json();
    setQuery(data["Palavra em ingles"]);
    const correctAnswer = data["Palavra em portugues"];
    const shuffledAnswers = [correctAnswer, getWordWithOneLetterChanged(correctAnswer), getWordWithOneLetterChanged(correctAnswer), getWordWithOneLetterChanged(correctAnswer)];
    setOptions(shuffledAnswers);
  };

  const fetchPhoto = async () => {
    setLoading(true);
    const response = await fetch(`https://api.unsplash.com/photos/random?query=${query}&client_id=_APIKEY_`);
    const data = await response.json();
    setPhoto(data.urls.regular);
    setLoading(false);
  };

  useEffect(() => {
    fetchRandomWord();
  }, []);

  useEffect(() => {
    if (query) {
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

  const getWordWithOneLetterChanged = (word) => {
    let newWord;
    do {
      const alphabet = 'abcdefghijklmnopqrstuvwxyz';
      const index = Math.floor(Math.random() * word.length);
      const randomLetter = alphabet[Math.floor(Math.random() * alphabet.length)];
      newWord = word.substring(0, index) + randomLetter + word.substring(index + 1);
    } while (newWord === word);
    return newWord;
  }

  return (
    <div className="photo-box">
      <div className="photo-image" style={{ backgroundImage: `url(${photo})` }}></div>
      <div className="photo-options">
        {shuffle(options).map((option, index) => (
          <div className="photo-option" key={index} onClick={() => handleOptionClick(option)}>{option}</div>
        ))}
      </div>
    </div>
  );
};

export default PhotoComponent;
