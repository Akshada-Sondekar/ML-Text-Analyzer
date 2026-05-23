import React, { useState } from "react";
import API from "../api";

function PredictForm() {

  const [text, setText] = useState("");

  const [result, setResult] = useState("");

  const handleSubmit = async (e) => {

    e.preventDefault();

    try {

      const response = await API.post("/predict", {
        text: text
      });

      setResult(response.data.prediction);

      setText("");

    } catch (error) {

      console.log(error);

    }

  };

  return (

    <div className="card">

      <form onSubmit={handleSubmit}>

        <textarea
          rows="5"
          placeholder="Enter your message"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button type="submit">

          Predict

        </button>

      </form>

      {result && (

        <div className="result">

          Prediction: {result}

        </div>

      )}

    </div>

  );
}

export default PredictForm;