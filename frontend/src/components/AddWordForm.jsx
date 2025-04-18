import React, { useState } from 'react';

const AddWordForm = ({ onAdd }) => {
  const [word, setWord] = useState({
    german: '',
    translation: '',
    article: '',
    level: 'A1'
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onAdd(word);
    setWord({ german: '', translation: '', article: '', level: 'A1' });
  };

  return (
    <form onSubmit={handleSubmit}>
      <select
        value={word.article}
        onChange={(e) => setWord({...word, article: e.target.value})}
      >
        <option value="">Без артикля</option>
        <option value="der">der</option>
        <option value="die">die</option>
        <option value="das">das</option>
      </select>
      <input
        type="text"
        value={word.german}
        onChange={(e) => setWord({...word, german: e.target.value})}
        placeholder="Немецкое слово"
        required
      />
      <input
        type="text"
        value={word.translation}
        onChange={(e) => setWord({...word, translation: e.target.value})}
        placeholder="Перевод"
        required
      />
      <button type="submit">Добавить</button>
    </form>
  );
};

export default AddWordForm;