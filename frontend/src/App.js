import './App.css';
import React, { useState } from 'react';
import { useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

function App() {
  const [responseData, setResponseData] = useState(null); // state hooks const [state, setState] = useState(initial state)
  const [loading, setLoading] = useState(false); 
  const [query, setQuery] = useState(''); 
  const [fractalImage, setFractalImage] = useState(null);
  const [error, setError] = useState(null);
  const [fractalParams, setFractalParams] = useState({
    formula: 'z**2 + c',
    width: 800,
    height: 800,
    div_thresh: 2,
    realBounds: '-2.5, 2.5',
    imagBounds: '-1.5, 1.5',
    maxItr: 100,
  });
  const labelMapping = {
    'formula': 'formula f(z, c)',
    'realBounds': 'real bounds',
    'imagBounds': 'imaginary bounds',
    'div_thresh': 'divergence threshold',
    'width': 'width (resolution)',
    'height': 'height (resolution)',
    'maxItr': 'iterations'
  }

  useEffect(() => { //lambda func to detail side effects
    document.title = 'MandelbrotGPT';
  }, []); // dependencies tells react when to update (if dependencies update), empty means just do once

  const fetchRandomMathematician = async() => { //async arrow function to fetch llama data
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/llama/random_mathematician/'); //try fetching data from api endpoint, speciifically random mm
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

  const queryLlama = async () => {
    if (!query) {
      alert('Please enter a prompt!');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/llama/query_llama/?prompt=${query}`);
      const data = await response.json();
      setResponseData(data);
    } catch (error) {
      console.error('Error querying LLaMA:', error);
      setResponseData({ error: 'Failed to query' });
    } finally {
      setLoading(false);
    }
  };

  const generateFractal = async () => {
    setError(null); // Clear previous errors

    const requestData = {
      formula: fractalParams.formula,
      width: parseInt(fractalParams.width),
      height: parseInt(fractalParams.height),
      div_thresh: parseFloat(fractalParams.div_thresh),
      realBounds: fractalParams.realBounds.split(',').map(Number),
      imagBounds: fractalParams.imagBounds.split(',').map(Number),
      maxItr: parseInt(fractalParams.maxItr),
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/api/fractal/', {
        method: 'POST', //posting to api
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to generate fractal');
      }

      const data = await response.json();
      setFractalImage(`data:image/png;base64,${data.fractal}`);
    } catch (err) {
      setError(err.message);
    }
  };

  const updateParam = (key, value) => { //field name, new val
    setFractalParams((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <div style={styles.container}>
      <div style={styles.fractalSection}>
        <h1>Fractal Creator!</h1>

        <div style={styles.paramInputs}>
          {Object.keys(fractalParams).map((key) => ( //get keys and map lambda to each one, create a div for each
            <div key={key} style={styles.inputGroup}> 
              <label style={styles.label}>{labelMapping[key] || key}</label>
              <input
                type="text"
                value={fractalParams[key]}
                onChange={(e) => updateParam(key, e.target.value)}
                style={styles.input}
              />
            </div>
          ))}
          <button onClick={generateFractal} style={styles.genButt}>
          Generate
        </button>
        </div>


        {error && <p style={{ color: 'red' }}>Error: {error}</p>}

        {fractalImage && (
          <div>
            <h3>Your creation:</h3>
            <img src={fractalImage} alt="Fractal" style={styles.img} />
          </div>
        )}
      </div>

      <div style={styles.llamaSection}>
        <h2>MandelbrotGPT</h2>

        <button onClick={fetchRandomMathematician} style={styles.buttonR}>
          Random mathematician
        </button>

        <input
          type="text"
          placeholder="Ask anything..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={styles.input}
        />
        <button onClick={queryLlama} style={styles.button}>
          Submit
        </button>

        {loading && <p>Loading...</p>}

        {responseData && (
          <div style={styles.responseBox}>
            {responseData.error ? (
              <p style={styles.error}>{responseData.error}</p>
            ) : (
              <ReactMarkdown>{responseData.llama_response}</ReactMarkdown>
            )}
          </div>
        )}

        <img src='cat.gif' alt='i love you' style={styles.cat}>
        </img>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: '15px',
    fontFamily: 'Arial, sans-serif',
  },
  fractalSection: {
    flex: '0 0 72.5%',
    textAlign: 'center',
    padding: '20px',
    borderRight: '1px solid #ccc',
  },
  llamaSection: {
    flex: 1,
    padding: '10px',
    textAlign: 'center',
  },
  paramInputs: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '10px',
    marginBottom: '20px',
  },
  inputGroup: {
    width: '30%',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',
  },
  label: {
    fontWeight: 'bold',
    marginBottom: '5px',
  },
  input: {
    padding: '10px',
    fontSize: '16px',
    borderRadius: '5px',
    border: '1px solid #ccc',
    width: '50%',
    marginRight: '10px',
  },
  button: {
    backgroundColor: '#007BFF',
    color: '#fff',
    padding: '10px 20px',
    fontSize: '16px',
    borderRadius: '5px',
    border: 'none',
    cursor: 'pointer',
  },
  buttonR: {
    backgroundColor: '#007BFF',
    color: '#fff',
    padding: '10px 20px',
    fontSize: '16px',
    borderRadius: '5px',
    border: 'none',
    cursor: 'pointer',
    alighSelf: 'center',
    marginBottom: '20px',
  },
  genButt: {
    backgroundColor: '#007BFF',
    color: '#fff',
    padding: '10px 20px',
    fontSize: '16px',
    borderRadius: '5px',
    border: 'none',
    cursor: 'pointer',
    width: '17.5%',
    height: '75%',
    alignSelf: 'center',
    marginTop: '-10px', 
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
  img: {
    display: 'block',
    margin: '20px auto',
    maxWidth: '100%',
    border: '1px solid #000',
  },
  cat: {
    padding: '15px',
  }
};

export default App;
