import React, { Component } from 'react';

class App extends Component {
  render() {
    var url = 'http://127.0.0.1:4555/';
    var fetched = ''
    fetch(url,{mode: 'no-cors'})
      .then(function(data) {
          fetched = 'Yes';
          console.log('Yes');
      }).catch(function() {
          fetched = 'No';
          console.log('No');
    });
    return (
      <p>{fetched}</p>
    );
  }
}

export default App;
