//import 'style-loader!css-loader!../css/font-awesome.min.css';
//import 'style-loader!css-loader!../css/milligram.min.css';
//import 'style-loader!css-loader!../css/pastebin.css';

/**
 * Created by johanness on 23/02/2017.
 */
import Axios from 'axios';
import React from 'react';
import ReactDOM from 'react-dom';
const app_baseurl = "/pastebin/";

class ShortenButton extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isButtonDisabled: false
        };
    }

    handleClick() {
        this.fetchShortenedAction();
    }


    render() {
        return (
            <button onClick={(e) => this.handleClick(e)}
            disabled={this.state.isButtonDisabled}>
                Shorten!
            </button>
        );
    }

    fetchShortenedAction() {
        this.setState({isButtonDisabled: true});
        ReactDOM.render(
            <FetchShortenedUrl/>,
            document.getElementById('react_shortened')
        );
    }
}

class FetchShortenedUrl extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    componentDidMount() {
        Axios.post(app_baseurl + 'api/shorten', {
            url: FetchShortenedUrl.get_url()
        })
            .then(res => {
                if (res.data.shortened_url) {
                    const shortened_url = res.data.shortened_url;
                    this.setState({shortened_url});
                }
                else if (res.data.message) {
                    const message = res.data.message;
                    this.setState({message});
                }
                else {

                }
            });
    }

    static get_url() {
        return window.location.href
    }

    render() {
        return (
            <div>
                {this.state.shortened_url ? this.printShortenedUrl() : this.printMsg()}
            </div>);
    }

    printShortenedUrl() {
        return (
            <p><a href={this.state.shortened_url}> Shortened url</a></p>
        );
    }

    printMsg() {
        return (
            <p> {this.state.message} </p>
        );
    }

}
$(document).ready(function () {
    ReactDOM.render(
        <ShortenButton/>,
        document.getElementById('react_shorten_button')
    );
})