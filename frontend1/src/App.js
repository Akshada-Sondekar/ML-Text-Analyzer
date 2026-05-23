import React from "react";

import "./App.css";

import PredictForm from "./components/PredictForm";

import History from "./components/History";

function App() {

  return (

    <div className="app">

      <div className="overlay">

        <div className="container">

          <h1 className="title">
             AI Spam Classifier
          </h1>

          <p className="subtitle">
            Detect spam messages using Machine Learning
          </p>

          <PredictForm />

          <History />

        </div>

      </div>

    </div>

  );
}

export default App;