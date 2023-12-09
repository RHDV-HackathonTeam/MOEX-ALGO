import React, { useEffect, useState } from 'react';
import { Card, CardContent, Grid } from '@mui/material';
import { Graph } from './Graph';
import Overview from './Overview';
import NewsFeed from './NewsFeed';
import axios from 'axios';

const StrategyInfo = (props) => {

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  let originalDate = props.data.from;
  let modifiedDate = originalDate.replace(/\//g, '-');

  let originalDate2 = props.data.to;
  let modifiedDate2 = originalDate2.replace(/\//g, '-');

  const rdata = {
    ticker: props.data.ticker,
    from_date: modifiedDate,
    to_date: modifiedDate2,
    time_period: 'D'
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.post('http://localhost:9878/api/ticker/get_candles', rdata);
        setData(response.data.candles);
        setLoading(false); // Set loading to false when data arrives
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false); // Set loading to false in case of an error
      }
    };

    fetchData();
  }, []);

  return (
    <div style={{ width: '100%', padding: '20px' }}>
      <Grid container spacing={2}>
        <Grid item xs={2}>
          <Card>
            <CardContent style={{ height: 400 }}>
              <Overview {...props.data}/>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6}>
        <Card>
            <CardContent style={{ height: 400 }}>
            {loading ? (
              <p>Loading...</p>
            ) : (<Graph {...props} data={data}></Graph>)}
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={4}>
          <Card>
            <CardContent style={{ height: 400 }}>
            <NewsFeed {...props}/>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
};

export default StrategyInfo;