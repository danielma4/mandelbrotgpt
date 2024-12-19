import './App.css';
import React, {useState} from 'react';

function App() {
  const [responseData, setResponseData] = useState(null); //variables which store states of llama response + loading state
  const [loading, setLoading] = useState(false);

  const fetchRandomMathematician = async() => { //async arrow function to fetch llama data
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/llama/rand_mathematician/'); //try fetching data from api endpoint, speciifically random mm
      const data = await response.json(); //json response returned from fetch
      console.log('API Response:', data);
      setResponseData(data);
    } catch (error) {
      console.error('Error fetching random mathematician:', error);
      setResponseData({error: 'failed to fetch mathematician'});
    } finally {
      setLoading(false);
    }
  };

  //frontend display and styling
  return (
    <div style={styles.container}>
      <h1>Ask MathEQGPT about a random mathematician from history!</h1>

      {/* Button to call the API */}
      <button onClick={fetchRandomMathematician} style={styles.button}>
        Get random mathematician
      </button>

      {/* Show loading message */}
      {loading && <p>Loading...</p>}

      {/* Show the API response */}
      {responseData && (
        <div style={styles.responseBox}>
          {responseData.error ? (
            <p style={styles.error}>{responseData.error}</p>
          ) : (
            <>
              <h2>{responseData.mathematician}</h2>
              <p>{responseData.llama_response}</p>
            </>
          )}
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    textAlign: 'center',
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
  },
  button: {
    backgroundColor: '#007BFF',
    color: '#fff',
    padding: '10px 20px',
    fontSize: '16px',
    borderRadius: '5px',
    border: 'none',
    cursor: 'pointer',
    marginBottom: '20px',
  },
  responseBox: {
    backgroundColor: '#f4f4f9',
    padding: '20px',
    borderRadius: '5px',
    marginTop: '20px',
    boxShadow: '0 0 10px rgba(0,0,0,0.1)',
  },
  error: {
    color: 'red',
    fontWeight: 'bold',
  },
};


export default App;
