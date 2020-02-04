import React from "react";
import { InputGroup, FormControl } from "react-bootstrap";

class Result extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      res_placeholder: "Diverges | Converges | Inconclusive",
      res_num: "#"
    };
  }

  componentDidUpdate(prevProps) {
    // Typical usage (don't forget to compare props):
    if (this.props.result !== prevProps.result) {
      this.setState({
        res_placeholder: this.props.result,
        res_num: this.props.num.toFixed(4)
      });
    }
  }

  render() {
    return (
      <InputGroup className="result">
        <InputGroup.Prepend>
          <InputGroup.Text id="basic-addon1">
            <b>Result</b>
          </InputGroup.Text>
        </InputGroup.Prepend>
        <FormControl readOnly placeholder={this.state.res_placeholder} />
        <InputGroup.Prepend>
          <InputGroup.Text id="basic-addon1">
            <b>Value</b>
          </InputGroup.Text>
        </InputGroup.Prepend>
        <FormControl readOnly placeholder={this.state.res_num} />
      </InputGroup>
    );
  }
}

export default Result;
