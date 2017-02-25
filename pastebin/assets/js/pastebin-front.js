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

let Hello = React.createClass({
    render: function () {
        return (
            <h1>
                Hello, React!
            </h1>
        )
    }
});

$(document).ready(function () {
    if (document.getElementById('container')) {
        ReactDOM.render(<Hello />, document.getElementById('container'))
    }
    if (document.getElementById('shorten')) {
        ReactDOM.render(
            <FetchShortenedUrl orig_url="reactjs"/>,
            document.getElementById('shorten')
        );
    }
});

class FetchShortenedUrl extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            posts: []
        };
    }

    componentDidMount() {
        Axios.post(app_baseurl + 'api/shorten', {
            url: FetchShortenedUrl.get_url()
        })
            .then(res => {
                console.log(res)
                if (res.data.shortened_url) {
                    const shortened_url = res.data.shortened_url
                    this.setState({shortened_url});
                    console.log(this.state)
                }
                else {
                    // TODO handle errors
                }
            });
    }

    static get_url() {
        return "https://google.fi"
    }

    render() {
        return (
            <div>
                <p><a href={this.state.shortened_url}> Shortened url</a></p>
            </div>
        );
    }
}
