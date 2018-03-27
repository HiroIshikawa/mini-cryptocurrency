// var data = {{ node_data|tojson|safe }};
// console.log(data);

// class Example React.Component {
//     render() {
//         <p>this</p>
//     }
// }

// const element = <h1>Hello World</h1>;
// ReactDOM.render(element, documentElementById('root'))
// 
var data = {{ node_data|tojson|safe }};
console.log(data);

React.render(<p>{data.blockchain}</p>, document.getElementById('root'));