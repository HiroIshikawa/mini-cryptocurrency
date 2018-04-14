import React, { Component } from 'react';
import axios from 'axios';

class NodeInfo extends Component {
  constructor(props) {
    super(props);
    this.state =  {
      node_type: 'No type fetched yet',
      pub_key: 'No pubkey fetched yet'
    };
  }

  componentDidMount() {
    var url = 'http://127.0.0.1:4555/json/node/';
    axios.get(url, {
        headers: {
          'Access-Control-Allow-Origin': '*', 
        },
        mode: 'no-cors'
      })
      .then(response => {
          let fetched_data = response.data
          console.log(fetched_data);
          let type = fetched_data['type']
          console.log(type);
          let pub_key = fetched_data['pub_key']
          console.log(pub_key)
          this.setState({
            node_type: type,
            pub_key: pub_key 
          });
      }).catch(error => {
          console.log('No');
    });
  }

  render() {
    return (
      <div>
        <div>
          {this.state.node_type}
        </div>
        <div>
          {this.state.pub_key}
        </div>
      </div>
    );
  }
}

export default NodeInfo