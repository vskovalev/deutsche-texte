import React from 'react';

const WordList = ({ words, onDelete }) => (
  <div className="word-list">
    <h3>Ваш словарь</h3>
    <ul>
      {words.map(word => (
        <li key={word.id}>
          {word.article ? `${word.article} ${word.german}` : word.german} - {word.translation}
          <button onClick={() => onDelete(word.id)}>Удалить</button>
        </li>
      ))}
    </ul>
  </div>
);

export default WordList;