import { useState, useEffect, useRef } from 'react'
import aesirLogo from './assets/ÆSIR.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [socketData, setSocketData] = useState("None")
  const socketRef = useRef(null);

  useEffect(() => {
    socketRef.current = new WebSocket("ws://localhost:8000/ws");

    socketRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setSocketData(data["data"]);
      console.log(data);
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
      socketRef.current.send(`Count: ${count}`);
    } else {
      console.error("WebSocket is not open.");
    }
  }

  return (
    <>
      <section className="window">
        <div>
          <a href="https://react.dev" target="_blank">
            <img src={aesirLogo} className="logo aesir" alt="AESIR logo" />
          </a>
        </div>
        <h1>Mjöllnir GCS</h1>
        <div className="card">
          <button onClick={() => {
            setCount((prevCount) => prevCount + 1);
            handleOtherClick(); 
          }}>
            count is {count}
          </button>
          <p>
            Edit <code>src/App.jsx</code> and save to test HMR
          </p>
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
