import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Overview = (props) => {
//   const [props, setProps] = useState(null);

//   useEffect(() => {
//     axios.get('http://localhost:3001/api/strategy/{id}')
//       .then(response => {
//         setprops(response.data);
//       })
//       .catch(error => {
//         console.error('Error fetching strategy:', error);
//       });
//   }, []); 

  // let props = {
  //   title: "test",
  //   description: "for test",
  //   from: "1984/12/27",
  //   to: "2228/12/27",
  //   ticker: "GAZP",
  //   profitability: "228%",
  //   riskreward: "1/3",
  //   riskondeal: "2%",
  //   maxloss: "500$",
  //   maxdayloss: "278$"
  // }
  
  const profitabilityText = props?.profitability ? props.profitability : '0';
  let profitabilityColor = '';
  if (profitabilityText === 'Not tested') profitabilityColor = 'red';
  else profitabilityColor = props?.profitability?.includes('-') ? 'red' : 'green';
  const maxLossText = props?.maxloss ? props.maxloss : '0';
  const maxDayLossText = props?.maxdayloss ? props.maxdayloss : '0';

  return (
    <section className="overview">
      <h2>Overview</h2>
      {props && (
        <div>
          <p>title: {props.title}</p>
          <p>from: {props.from}</p>
          <p>to: {props.to}</p>
          <p>ticker: {props.ticker}</p>
          <p>profitability: <span style={{ color: profitabilityColor }}>{profitabilityText+'%'}</span></p>
          <p>risk-reward: {props.riskreward}</p>
          <p>risk on deal: {props.riskondeal+'%'}</p>
          <p>max day loss: <span style={{ color: 'red' }}>{maxDayLossText+'$'}</span></p>
          <p>max loss: <span style={{ color: 'red' }}>{maxLossText+'$'}</span></p>
        </div>
      )}
    </section>
  );
};

export default Overview;
