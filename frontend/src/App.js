import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [words, setWords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Загрузка слов с бэкенда
  useEffect(() => {
    const fetchWords = async () => {
      try {
        const response = await fetch('/api/words');
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Убеждаемся, что data - массив
        if (Array.isArray(data)) {
          setWords(data);
        } else {
          console.error('Ожидался массив, получено:', data);
          setWords([]);
        }
      } catch (err) {
        console.error('Ошибка при загрузке слов:', err);
        setError(err.message);
        setWords([]);
      } finally {
        setLoading(false);
      }
    };

    fetchWords();
  }, []);

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div>Ошибка: {error}</div>;

  return (
    <div className="app-container">
      <h1>Немецкий словарь</h1>
      
      <div className="words-list">
        <h2>Ваши слова:</h2>
        {words.length > 0 ? (
          <ul>
            {words.map((word, index) => (
              <li key={index}>
                <strong>{word.german}</strong> - {word.translation}
              </li>
            ))}
          </ul>
        ) : (
          <p>Слова не найдены</p>
        )}
      </div>
    </div>
  );
}

export default App;