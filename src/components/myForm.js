import React from "react";

import Summand from "./summand.js";
import Result from "./result.js";

class MyForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      result: "unrun",
      num: ""
    };

    this.getResultFromChild = this.getResultFromChild.bind(this);
  }

  getResultFromChild = result => {
    this.setState({
      result: result.result,
      num: result.num
    });

    console.log(this.state);
  };

  render() {
    console.log(this.state);
    return (
      <div>
        <Summand sendResult={this.getResultFromChild} />
        <Result result={this.state.result} num={this.state.num} />
      </div>
    );
  }
}

export default MyForm;
