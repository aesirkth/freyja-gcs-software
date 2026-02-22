import { useState, useEffect, useRef } from 'react'
import aesirLogo from './assets/ÆSIR.svg'
import './App.css'

function App() {
  const [socketData, setSocketData] = useState("None");
  const [serPortButtons, setSerPortButtons] = useState([]);
  const adc_dict = {
    "1": { "tag": "ADC1", "value": 0.0 },
    "2": { "tag": "ADC2", "value": 0.0 },
    "3": { "tag": "ADC3", "value": 0.0 },
    "4": { "tag": "ADC4", "value": 0.0 },
    "5": { "tag": "ADC5", "value": 0.0 },
    "6": { "tag": "ADC6", "value": 0.0 },
    "7": { "tag": "ADC7", "value": 0.0 },
    "8": { "tag": "ADC8", "value": 0.0 },
    "9": { "tag": "ADC9", "value": 0.0 },
    "10": { "tag": "ADC10", "value": 0.0 },
    "11": { "tag": "ADC11", "value": 0.0 },
    "12": { "tag": "ADC12", "value": 0.0 }
  };

  const switch_dict = {
    "1": { "tag": "SW1", "status": false },
    "2": { "tag": "SW2", "status": false },
    "3": { "tag": "SW3", "status": false },
    "4": { "tag": "SW4", "status": false },
    "5": { "tag": "SW5", "status": false },
    "6": { "tag": "SW6", "status": false },
    "7": { "tag": "SW7", "status": false },
    "8": { "tag": "SW8", "status": false },
    "9": { "tag": "SW9", "status": false },
    "10": { "tag": "SW10", "status": false },
    "11": { "tag": "SW11", "status": false },
    "12": { "tag": "SW12", "status": false }
  };
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
          Object.entries(adc_dict).forEach(([id, entry]) => {
            const lookupKey = `value${id}`; 
            
            if (data.adc_measurements[lookupKey] !== undefined) {
              entry.value = data.adc_measurements[lookupKey];
            }
          });
        }
        
        if (data.switch_states) {
          Object.entries(switch_dict).forEach(([id, entry]) => {
            const lookupKey = `sw${id}`; 
            
            if (data.switch_states[lookupKey] !== undefined) {
              entry.status = data.adc_measurements[lookupKey];
            }
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

  const submitCommand = (key) => {
    const buffer = {
      "id": key,
      "status": switch_dict["status"]
    };
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
        const cmd_payload = JSON.stringify(buffer); 
        socketRef.current.send(cmd_payload);
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
                {Object.keys(adc_dict).map((key, index) => (
                  <div key={index}>
                    <p className="data-title">{adc_dict[key]["tag"]}</p>
                    <p className="data-value">{adc_dict[key]["value"]}</p>
                  </div>
                ))}
              </div>
              <div className="table-2">
                {Object.keys(switch_dict).map((key, index) => (
                  <div key={index}>
                    <p className="data-title">{switch_dict[key]["tag"]}</p>
                    <p className="data-value">{switch_dict[key]["status"]}</p>
                  </div>
                ))}
              </div>
            </div>
            <div className="procedure-list">
              <h3>
                TEST PROCEDURES
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
                  {Object.keys(switch_dict).map((key, index) => (
                    <button onClick={() => submitCommand(key)} key={index}>
                      AC{key}
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
