import React, { useState, useEffect } from 'react';
import WordList from './components/WordList';
import AddWordForm from './components/AddWordForm';
import SentenceExercises from './components/SentenceExercises';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [words, setWords] = useState([]);
  const [selectedWord, setSelectedWord] = useState(null);

  useEffect(() => {
    fetchWords();
  }, []);

  const fetchWords = async () => {
    try {
      const response = await fetch('http://localhost:8000/words');
      const data = await response.json();
      setWords(data);
    } catch (error) {
      console.error('Ошибка при загрузке слов:', error);
    }
  };

  const addWord = async (word) => {
    try {
      const response = await fetch('http://localhost:8000/words', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(word)
      });
      const newWord = await response.json();
      setWords([...words, newWord]);
    } catch (error) {
      console.error('Ошибка при добавлении слова:', error);
    }
  };

  return (
    <div className="app">
      <h1>Изучение немецких слов</h1>
      <div className="container">
        <div className="word-section">
          <AddWordForm onAdd={addWord} />
          <WordList words={words} />
        </div>
        {selectedWord && (
          <div className="exercises-section">
            <SentenceExercises word={selectedWord} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;