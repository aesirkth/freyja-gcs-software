import { useState, useEffect, useRef } from 'react'
import aesirLogo from './assets/ÆSIR.svg'
import './App.css'

function App() {
  const [socketData, setSocketData] = useState("None");
  const [serPortButtons, setSerPortButtons] = useState([]);
  const adc_list = [
    { "id": 1, "value": 0.0 },
    { "id": 2, "value": 0.0 },
    { "id": 3, "value": 0.0 },
    { "id": 4, "value": 0.0 },
    { "id": 5, "value": 0.0 },
    { "id": 6, "value": 0.0 },
    { "id": 7, "value": 0.0 },
    { "id": 8, "value": 0.0 },
    { "id": 9, "value": 0.0 },
    { "id": 10, "value": 0.0 },
    { "id": 11, "value": 0.0 },
    { "id": 12, "value": 0.0 }
  ];
  const switch_list = [
    { "id": 1, "status": false },
    { "id": 2, "status": false },
    { "id": 3, "status": false },
    { "id": 4, "status": false },
    { "id": 5, "status": false },
    { "id": 6, "status": false },
    { "id": 7, "status": false },
    { "id": 8, "status": false },
    { "id": 9, "status": false },
    { "id": 10, "status": false },
    { "id": 11, "status": false },
    { "id": 12, "status": false }
  ];
  const cmds = {
    
  }
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

        if (data.adc_measurements) {
          Object.keys(data.adc).map(function(key) {
            adc_list[key] = data.adc[key];
          });
        }

        if (data.sw_ctrl) {
          Object.keys(data.switch).map(function(key) {
            switch_list[key] = data.switch[key];
          });
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

  const handleOtherClick = (item) => {
    const buffer = { ...item };
    buffer["status"] = !buffer["status"];
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
        const message = JSON.stringify(buffer); 
        socketRef.current.send(message);
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
              <div className="table-1">
                {adc_list.map((item, index) => (
                  <div key={index}>
                    <p className="data-title">ADC {item["id"]}</p>
                    <p className="data-value">{item["status"]}</p>
                  </div>
                ))}
              </div>
              <div className="table-2">
                {switch_list.map((item, index) => (
                  <div key={index}>
                    <p className="data-title">SW {item["id"]}</p>
                    <p className="data-value">{item["status"]}</p>
                  </div>
                ))}
              </div>
            </div>
            <div className="procedure-list">
              <h3>
                TEST PROCEDURE
              </h3>
              <div>       
                  
              </div>
            </div>
            <div className="command-list">
              <div className="command">
                <h3>
                  ACTUATION CONTROLS
                </h3>
                <div className="control-wrapper">
                  {switch_list.map((item, index) => (
                    <button onClick={() => handleOtherClick(item)} key={index}>
                      AC {item["id"]}
                    </button>
                  ))}
                </div>
                <h3>
                  
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
