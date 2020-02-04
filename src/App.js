import React from "react";
import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";

import Ticker from "./components/ticker.js";
import MyForm from "./components/myForm.js";

function App() {
  return (
    <div className="App">
      <div className="App-content">
        <h1> Ratio Test Calculator </h1>
        <Ticker />
        <MyForm />
      </div>
      <footer>
        <p className="App-p-small">
          Given a sequence a <sub> n </sub>, this program computes the limit of
          the ratios a<sub>n</sub> /a<sub>n-1</sub> as n tends to &#8734;. If
          this value is {">"}1 the series diverges, {"<"} 1 the series
          converges. Otherwise it is inconclusive. You can find my code and
          raise issues{" "}
          <a
            href="https://github.com/jlgre/ratiotestxyz"
            target="_blank"
            rel="noopener noreferrer"
          >
            here
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;
