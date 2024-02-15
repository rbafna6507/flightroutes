import React, { useState, useEffect } from "react";
import { Form, Button } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const [airports, setAirports] = useState([]);
  const [source, setSource] = useState("");
  const [dest, setDest] = useState("");
  const [best_path, setBest] = useState("");
  const [second_path, setSecond] = useState("");
  const [third_path, setThird] = useState("");
  const [distances, setDistances] = useState("");
  const [times, setTimes] = useState("");

  useEffect(() => {
    fetchAirports();
  }, []);

  const fetchAirports = async () => {
    try {
      const response = await fetch("/airports.txt");
      const data = await response.text();
      console.log(data);
      const lines = data.split("\n");
      setAirports(lines);
    } catch (error) {
      console.error("Error fetching airports:", error);
    }
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/route/source=${source}&dest=${dest}`
      );
      const data = await response.json();
        console.log(data);
        let best_path = "";
        for (let i = 0; i < data.paths[0].length; i++){
          best_path= best_path + data.paths[0][i];
          best_path = best_path + " to ";
        }
        let second_path = "";
        for (let i = 0; i < data.paths[1].length; i++){
          second_path= second_path + data.paths[1][i];
          second_path = second_path + " to ";
        }
        let third_path = "";
        for (let i = 0; i < data.paths[2].length; i++){
          third_path= third_path + data.paths[2][i];
          third_path = third_path + " to ";
        }
        setBest(best_path.slice(0,-4)); // Assuming the API returns result in JSON format with a 'path' key
        setSecond(second_path.slice(0,-4));
        setThird(third_path.slice(0,-4));
        setDistances(data.distances)
        setTimes(data.times)
      } catch (error) {
        console.error("Error fetching route:", error);
        setBest("Error fetching route. Please try again.");
      }
  };

  return (
    <div className="container">
      <br />
      <h1>Flight Pathfinding with A*</h1>
      <Form>
        <Form.Group controlId="source">
          <Form.Label>From:</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter Source"
            value={source}
            onChange={(e) => setSource(e.target.value)}
          />
        </Form.Group>
        <br />
        <Form.Group controlId="dest">
          <Form.Label>To:</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter Destination"
            value={dest}
            onChange={(e) => setDest(e.target.value)}
          />
        </Form.Group>
        <br />
        <Button variant="primary" onClick={handleSubmit}>
          Submit
        </Button>
      </Form>
      <br />
      <h3>Result Paths:</h3>
      <br></br>
      {/* {result && <h3>{result}</h3>} */}
      {best_path && <h4>{best_path} </h4>}
      {times && <h5>Total distance traveled: {distances[0].toFixed(2)} kms. <br />Total time during travel: {times[0].toFixed(2)} hours.</h5>}
      <br />
      {second_path && <h4>{second_path}</h4>}
      {times && <h5>Total distance traveled: {distances[1].toFixed(2)} kms. <br />Total time during travel: {times[1].toFixed(2)} hours.</h5>}
      <br />
      {third_path && <h4>{third_path}</h4>}
      {times && <h5>Total distance traveled: {distances[2].toFixed(2)} kms. <br />Total time during travel: {times[2].toFixed(2)} hours.</h5>}
    </div>
  );
}

export default App;



// OLD V1
// import React, { useState, useEffect } from "react";

// function App() {
//   const [airports, setAirports] = useState([]);
//   const [source, setSource] = useState("");
//   const [dest, setDest] = useState("");
//   const [result, setResult] = useState("");

//   useEffect(() => {
//     fetchAirports();
//   }, []);

//   const fetchAirports = async () => {
//     try {
//       const response = await fetch("/airports.txt");
//       const data = await response.text();
//       console.log(data);
//       const lines = data.split("\n");
//       setAirports(lines);
//     } catch (error) {
//       console.error("Error fetching airports:", error);
//     }
//   };

//   const handleSubmit = async () => {
//     try {
//       const response = await fetch(
//         `http://127.0.0.1:5000/route/source=${source}&dest=${dest}`
//       );
//       const data = await response.json();
//       console.log(data);
//       let data_str = "";
//       for (let i = 0; i < data.path.length; i++){
//         data_str= data_str + data.path[i];
//         data_str = data_str + "-->";
//       }
//       setResult(data_str.slice(0,-3)); // Assuming the API returns result in JSON format with a 'path' key
//     } catch (error) {
//       console.error("Error fetching route:", error);
//       setResult("Error fetching route. Please try again.");
//     }
//   };

//   return (
//     <div>
//       <h1>Flight Route Finder</h1>
//       <div>
//         <label htmlFor="source">From:</label>
//         <select
//           id="source"
//           value={source}
//           onChange={(e) => setSource(e.target.value)}
//         >
//           <option value="">Select Source</option>
//           {airports.map((airport, index) => (
//             <option key={index} value={airport}>
//               {airport}
//             </option>
//           ))}
//         </select>
//       </div>
//       <br />
//       <div>
//         <label htmlFor="dest">To:</label>
//         <select
//           id="dest"
//           value={dest}
//           onChange={(e) => setDest(e.target.value)}
//         >
//           <option value="">Select Destination:</option>
//           {airports.map((airport, index) => (
//             <option key={index} value={airport}>
//               {airport}
//             </option>
//           ))}
//         </select>
//         <br />
//       </div>
//       <br />
//       <button onClick={handleSubmit}>Submit</button>
//       <br />
//       <br />
//       <h4>Result Path:</h4>
//       {result && <h3>{result}</h3>}
//     </div>
//   );
// }

// export default App;
