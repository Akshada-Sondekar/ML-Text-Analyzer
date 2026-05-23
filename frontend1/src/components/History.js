import React, { useEffect, useState } from "react";
import API from "../api";

function History() {

  const [history, setHistory] = useState([]);

  useEffect(() => {

    fetchHistory();

  }, []);

  const fetchHistory = async () => {

    try {

      const response = await API.get("/history");

      setHistory(response.data);

    } catch (error) {

      console.log(error);

    }

  };

  return (

    <div className="card">

      <h2>Prediction History</h2>

      {history.map((item) => (

        <div key={item.id} className="history-item">

          <p>
            <strong>Text:</strong> {item.text}
          </p>

          <p>
            <strong>Prediction:</strong> {item.prediction}
          </p>

        </div>

      ))}

    </div>

  );
}

export default History;