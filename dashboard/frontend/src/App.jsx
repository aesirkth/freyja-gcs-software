import { useState, useEffect, useRef, React } from 'react'
import aesirLogo from './assets/ÆSIR.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0);
  const [socketData, setSocketData] = useState("None");
  const [serPortButtons, setSerPortButtons] = useState([]);
  const actItems = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "12"];
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
        <div className="main-screen">
          <div className="table-tab">
            <table className="table-1">
              {actItems.map((item, index) => (
                <div key={index}>
                  <p className="data-title">AC</p>
                  <p className="data-value">{item}</p>
                </div>
              ))}
            </table>
            <table className="table-2">
              {actItems.map((item, index) => (
                <div key={index}>
                  <p className="data-title">AC</p>
                  <p className="data-value">{item}</p>
                </div>
              ))}
            </table>
          </div>
          <div className="procedure-list">
            <h3>
              TEST PROCEDURE
            </h3>
            <table>       
                
            </table>
          </div>
          <div className="command-list">
            <div className="command">
              <h3>
                ACTUATION CONTROLS
              </h3>
              <div className="control-wrapper">
                {actItems.map((item, index) => (
                  <button key={index}>
                    AC{item}
                  </button>
                ))}
              </div>
              <h3>
                STEPPER CONTROLS
              </h3>
            </div>
          </div>
        </div>
        <footer className="control-footer">

        </footer>
    </section>
    </>
  )
}

export default App
