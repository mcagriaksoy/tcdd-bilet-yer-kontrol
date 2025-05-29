import React, { useState } from "react";
import "./App.css";

function App() {
  const [from, setFrom] = useState("");
  const [to, setTo] = useState("");
  const [date, setDate] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResults(null);

    try {
      const res = await fetch("/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ from, to, date }),
      });
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error("Error fetching results:", err);
      setResults({ error: "Error fetching results." });
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h2>Ticket Search</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="From"
          value={from}
          onChange={(e) => setFrom(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="To"
          value={to}
          onChange={(e) => setTo(e.target.value)}
          required
        />
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>
      </form>
      {results && (
        <div>
          <h3>Results</h3>
          {results.error ? (
            <div style={{ color: "red" }}>{results.error}</div>
          ) : (
            <pre>{JSON.stringify(results, null, 2)}</pre>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
