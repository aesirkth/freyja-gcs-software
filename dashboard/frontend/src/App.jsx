import { useState, useEffect, useRef } from 'react'
import aesirLogo from './assets/ÆSIR.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [socketData, setSocketData] = useState("None")
  const [serPortButtons, setSerPortButtons] = useState([])
  const socketRef = useRef(null);

  useEffect(() => {
    socketRef.current = new WebSocket("ws://localhost:8000/ws");

    socketRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        if (data.ports) {
          setSerPortButtons(data.ports);
          console.log("Ports received:", data.ports);
        }
        
        if (data.data) {
          setSocketData(data.data);
        }

        console.log("Full data object:", data);
      } catch (error) {
        console.error("Error parsing WebSocket message:", error);
      }
    };

    socketRef.current.onopen = () => {
      console.log('WebSocket connection established!');
      socketRef.current.send('Hello Server!');
    };

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, []);
  
  const handleOtherClick = () => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(1);
    } else {
      console.error("WebSocket is not open.");
    }
  }

  return (
    <>
    <section className="parent-container">
        <div className="logo-container">
          <a href="" target="_blank">
            <img src={aesirLogo} className="logo aesir" alt="AESIR logo" />
          </a>
          <p>GCS MJOLLNIR</p>
        </div>
        <div className="card">
          <button onClick={() => {
            setCount((prevCount) => prevCount + 1);
            handleOtherClick(); 
          }}>
            {count}
          </button>
          <p>
            Edit <code>src/App.jsx</code> and save to test HMR
          </p>
          <div style={{ display: 'flex', gap: '12px' }}>
            {serPortButtons.map((port, index) => (
              <button 
                key={index} 
                onClick={() => console.log(`Connecting to ${port}...`)}
              >
                {port}
              </button>
            ))}
          </div>
          <p>
            Incoming data is {socketData}
          </p>
        </div>
        <p className="read-the-docs">
          Click on the Vite and React logos to learn more
        </p>
    </section>
    </>
  )
}

export default App
