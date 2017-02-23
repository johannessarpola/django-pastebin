//import 'style-loader!css-loader!../css/font-awesome.min.css';
//import 'style-loader!css-loader!../css/milligram.min.css';
//import 'style-loader!css-loader!../css/pastebin.css';

/**
 * Created by johanness on 23/02/2017.
 */
let React = require('react');
let ReactDOM = require('react-dom');
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
});