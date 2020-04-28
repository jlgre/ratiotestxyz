import React from 'react';
import { InputGroup, FormControl, Button } from 'react-bootstrap';

class Summand extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            result: '',
            num: 0
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.sendResult = this.sendResult.bind(this);
    }

    sendResult = () => {
        this.props.sendResult(this.state);
    };

    handleChange(event) {
        this.setState({ value: event.target.value });
    }

    handleSubmit(event) {
        let url = 'https://api.lukegreen.xyz/ratioTest?';
        // This is test url for local python server
        //let url = 'http://localhost:8000/ratioTest?';

        const summand = this.state.value;
        const escapedSummand = 'summand=' + encodeURIComponent(summand);

        url += escapedSummand;

        fetch(url)
            .then(data => {
                return data.json();
            })
            .then(res => {
                console.log(res);
                const result = res['result'];
                const value = res['num'];
                if (isNaN(value)) {
                    alert(result, value);
                } else {
                    console.log(result);
                    console.log(value);
                    this.setState({
                        num: value,
                        result: result
                    });
                    this.sendResult();
                }
            });

        event.preventDefault();
    }

    render() {
        return (
            <InputGroup className="summand">
                <InputGroup.Prepend>
                    <InputGroup.Text id="basic-addon1">
                        <b>&#931;</b>
                    </InputGroup.Text>
                </InputGroup.Prepend>
                <FormControl
                    placeholder="Summand"
                    aria-label="Summand"
                    aria-describedby="basic-addon1"
                    onChange={this.handleChange}
                />
                <Button
                    variant="secondary"
                    type="submit"
                    onClick={this.handleSubmit}
                >
                    Calculate
                </Button>
            </InputGroup>
        );
    }
}

export default Summand;
