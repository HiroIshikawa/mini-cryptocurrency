import React, { Component } from 'react';
import axios from 'axios';
// import renderHTML from 'react-render-html';

class App extends Component {
  componentWillMount(props){
    this.setState({ showExternalHTML: false });
    this.setState({ body: <div>Nothing loaded yet</div>})
    this.toggleExternalHTML = this.toggleExternalHTML.bind(this);
  }

  createMarkup() { 
    var url = 'http://127.0.0.1:4555/json/';
    var fetched_data = ''
    axios.get(url, {
        headers: {
          'Access-Control-Allow-Origin': '*',
        },
        mode: 'no-cors'
      })
      .then(response => {
          fetched_data = response.data
          console.log(fetched_data);
      }).catch(error => {
          console.log('No');
    });
  }

  toggleExternalHTML() {
    if (this.state.showExternalHTML === true) {
      this.createMarkup()
    }
    this.setState({showExternalHTML: !this.state.showExternalHTML});
  }

  render() {
    return (
      <div>
        <button onClick={this.toggleExternalHTML}>Toggle Html</button>
        {this.state.showExternalHTML ? <div>{this.state.body}</div> : null}
      </div>
    );
  }
}

export default App;


// 