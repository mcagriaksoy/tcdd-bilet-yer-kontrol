import React, { useState } from 'react';

function App() {
  const [formData, setFormData] = useState({
    nereden: '',
    nereye: '',
    tarih: '',
    saat: '',
    telegram_msg: false,
    bot_token: '',
    chat_id: '',
    ses: false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      const result = await response.json();
      alert(result.message);
    } catch (error) {
      console.error('Error:', error);
      alert('Bir hata oluştu.');
    }
  };

  return (
    <div className="App">
      <h1>TCDD Bilet Arama</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Nereden:
          <input type="text" name="nereden" value={formData.nereden} onChange={handleChange} required />
        </label>
        <label>
          Nereye:
          <input type="text" name="nereye" value={formData.nereye} onChange={handleChange} required />
        </label>
        <label>
          Tarih:
          <input type="date" name="tarih" value={formData.tarih} onChange={handleChange} required />
        </label>
        <label>
          Saat:
          <input type="time" name="saat" value={formData.saat} onChange={handleChange} required />
        </label>
        <label>
          Telegram Mesajı Gönder:
          <input type="checkbox" name="telegram_msg" checked={formData.telegram_msg} onChange={handleChange} />
        </label>
        {formData.telegram_msg && (
          <>
            <label>
              Bot Token:
              <input type="text" name="bot_token" value={formData.bot_token} onChange={handleChange} />
            </label>
            <label>
              Chat ID:
              <input type="text" name="chat_id" value={formData.chat_id} onChange={handleChange} />
            </label>
          </>
        )}
        <label>
          Ses Çal:
          <input type="checkbox" name="ses" checked={formData.ses} onChange={handleChange} />
        </label>
        <button type="submit">Ara</button>
      </form>
    </div>
  );
}

export default App;
