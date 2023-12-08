import React from 'react';
import { Card, CardContent, Grid } from '@mui/material';
import { Graph } from './Graph';
import Overview from './Overview';
import NewsFeed from './NewsFeed';

const initialData = [
  [
    { time: '2018-10-19', value: 19103293.0 },
    { time: '2018-10-22', value: 21737523.0 },
    { time: '2018-10-23', value: 29328713.0 },
    { time: '2018-10-24', value: 37435638.0 },
    { time: '2018-10-25', value: 25269995.0 },
    { time: '2018-10-26', value: 24973311.0 },
    { time: '2018-10-29', value: 22103692.0 },
    { time: '2018-10-30', value: 25231199.0 },
    { time: '2018-10-31', value: 24214427.0 },
    { time: '2018-11-01', value: 22533201.0 },
    { time: '2018-11-02', value: 14734412.0 },
    { time: '2018-11-05', value: 12733842.0 },
    { time: '2018-11-06', value: 12371207.0 },
    { time: '2018-11-07', value: 14891287.0 },
    { time: '2018-11-08', value: 12482392.0 },
    { time: '2018-11-09', value: 17365762.0 },
    { time: '2018-11-12', value: 13236769.0 },
    { time: '2018-11-13', value: 13047907.0 },
    { time: '2018-11-14', value: 18288710.0 },
    { time: '2018-11-15', value: 17147123.0 },
    { time: '2018-11-16', value: 19470986.0 },
    { time: '2018-11-19', value: 18405731.0 },
    { time: '2018-11-20', value: 22028957.0 },
    { time: '2018-11-21', value: 18482233.0 },
    { time: '2018-11-23', value: 7009050.0 },
    { time: '2018-11-26', value: 12308876.0 },
    { time: '2018-11-27', value: 14118867.0 },
    { time: '2018-11-28', value: 18662989.0 },
    { time: '2018-11-29', value: 14763658.0 },
    { time: '2018-11-30', value: 31142818.0 },
    { time: '2018-12-03', value: 27795428.0 },
    { time: '2018-12-04', value: 21727411.0 },
    { time: '2018-12-06', value: 26880429.0 },
    { time: '2018-12-07', value: 16948126.0 },
    { time: '2018-12-10', value: 16603356.0 },
    { time: '2018-12-11', value: 14991438.0 },
    { time: '2018-12-12', value: 18892182.0 },
    { time: '2018-12-13', value: 15454706.0 },
    { time: '2018-12-14', value: 13960870.0 },
    { time: '2018-12-17', value: 18902523.0 },
    { time: '2018-12-18', value: 18895777.0 },
    { time: '2018-12-19', value: 20968473.0 },
    { time: '2018-12-20', value: 26897008.0 },
    { time: '2018-12-21', value: 55413082.0 },
    { time: '2018-12-24', value: 15077207.0 }
  ],
  [
    {
      time: '2018-10-19',
      open: 180.34,
      high: 180.99,
      low: 178.57,
      close: 179.85
    },
    {
      time: '2018-10-22',
      open: 180.82,
      high: 181.4,
      low: 177.56,
      close: 178.75
    },
    {
      time: '2018-10-23',
      open: 175.77,
      high: 179.49,
      low: 175.44,
      close: 178.53
    },
    {
      time: '2018-10-24',
      open: 178.58,
      high: 182.37,
      low: 176.31,
      close: 176.97
    },
    {
      time: '2018-10-25',
      open: 177.52,
      high: 180.5,
      low: 176.83,
      close: 179.07
    },
    {
      time: '2018-10-26',
      open: 176.88,
      high: 177.34,
      low: 170.91,
      close: 172.23
    },
    {
      time: '2018-10-29',
      open: 173.74,
      high: 175.99,
      low: 170.95,
      close: 173.2
    },
    {
      time: '2018-10-30',
      open: 173.16,
      high: 176.43,
      low: 172.64,
      close: 176.24
    },
    {
      time: '2018-10-31',
      open: 177.98,
      high: 178.85,
      low: 175.59,
      close: 175.88
    },
    {
      time: '2018-11-01',
      open: 176.84,
      high: 180.86,
      low: 175.9,
      close: 180.46
    },
    {
      time: '2018-11-02',
      open: 182.47,
      high: 183.01,
      low: 177.39,
      close: 179.93
    },
    {
      time: '2018-11-05',
      open: 181.02,
      high: 182.41,
      low: 179.3,
      close: 182.19
    },
    {
      time: '2018-11-06',
      open: 181.93,
      high: 182.65,
      low: 180.05,
      close: 182.01
    },
    {
      time: '2018-11-07',
      open: 183.79,
      high: 187.68,
      low: 182.06,
      close: 187.23
    },
    {
      time: '2018-11-08',
      open: 187.13,
      high: 188.69,
      low: 185.72,
      close: 188.0
    },
    {
      time: '2018-11-09',
      open: 188.32,
      high: 188.48,
      low: 184.96,
      close: 185.99
    },
    {
      time: '2018-11-12',
      open: 185.23,
      high: 186.95,
      low: 179.02,
      close: 179.43
    },
    {
      time: '2018-11-13',
      open: 177.3,
      high: 181.62,
      low: 172.85,
      close: 179.0
    },
    {
      time: '2018-11-14',
      open: 182.61,
      high: 182.9,
      low: 179.15,
      close: 179.9
    },
    {
      time: '2018-11-15',
      open: 179.01,
      high: 179.67,
      low: 173.61,
      close: 177.36
    },
    {
      time: '2018-11-16',
      open: 173.99,
      high: 177.6,
      low: 173.51,
      close: 177.02
    },
    {
      time: '2018-11-19',
      open: 176.71,
      high: 178.88,
      low: 172.3,
      close: 173.59
    },
    {
      time: '2018-11-20',
      open: 169.25,
      high: 172.0,
      low: 167.0,
      close: 169.05
    },
    {
      time: '2018-11-21',
      open: 170.0,
      high: 170.93,
      low: 169.15,
      close: 169.3
    },
    {
      time: '2018-11-23',
      open: 169.39,
      high: 170.33,
      low: 168.47,
      close: 168.85
    },
    {
      time: '2018-11-26',
      open: 170.2,
      high: 172.39,
      low: 168.87,
      close: 169.82
    },
    {
      time: '2018-11-27',
      open: 169.11,
      high: 173.38,
      low: 168.82,
      close: 173.22
    },
    {
      time: '2018-11-28',
      open: 172.91,
      high: 177.65,
      low: 170.62,
      close: 177.43
    },
    {
      time: '2018-11-29',
      open: 176.8,
      high: 177.27,
      low: 174.92,
      close: 175.66
    },
    {
      time: '2018-11-30',
      open: 175.75,
      high: 180.37,
      low: 175.11,
      close: 180.32
    },
    {
      time: '2018-12-03',
      open: 183.29,
      high: 183.5,
      low: 179.35,
      close: 181.74
    },
    {
      time: '2018-12-04',
      open: 181.06,
      high: 182.23,
      low: 174.55,
      close: 175.3
    },
    {
      time: '2018-12-06',
      open: 173.5,
      high: 176.04,
      low: 170.46,
      close: 175.96
    },
    {
      time: '2018-12-07',
      open: 175.35,
      high: 178.36,
      low: 172.24,
      close: 172.79
    },
    {
      time: '2018-12-10',
      open: 173.39,
      high: 173.99,
      low: 167.73,
      close: 171.69
    },
    {
      time: '2018-12-11',
      open: 174.3,
      high: 175.6,
      low: 171.24,
      close: 172.21
    },
    {
      time: '2018-12-12',
      open: 173.75,
      high: 176.87,
      low: 172.81,
      close: 174.21
    },
    {
      time: '2018-12-13',
      open: 174.31,
      high: 174.91,
      low: 172.07,
      close: 173.87
    },
    {
      time: '2018-12-14',
      open: 172.98,
      high: 175.14,
      low: 171.95,
      close: 172.29
    },
    {
      time: '2018-12-17',
      open: 171.51,
      high: 171.99,
      low: 166.93,
      close: 167.97
    },
    {
      time: '2018-12-18',
      open: 168.9,
      high: 171.95,
      low: 168.5,
      close: 170.04
    },
    {
      time: '2018-12-19',
      open: 170.92,
      high: 174.95,
      low: 166.77,
      close: 167.56
    },
    {
      time: '2018-12-20',
      open: 166.28,
      high: 167.31,
      low: 162.23,
      close: 164.16
    },
    {
      time: '2018-12-21',
      open: 162.81,
      high: 167.96,
      low: 160.17,
      close: 160.48
    },
    {
      time: '2018-12-24',
      open: 160.16,
      high: 161.4,
      low: 158.09,
      close: 158.14
    }
  ],
  [
    {
      time: '2018-11-20',
      position: 'aboveBar',
      color: 'red',
      shape: 'arrowDown',
    },
    {
      time: '2018-12-18',
      position: 'belowBar',
      color: 'green',
      shape: 'arrowUp',
    }
  ]
];


const StrategyInfo = (props) => {
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
              <Graph {...props} data={initialData}></Graph>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={4}>
          <Card>
            <CardContent style={{ height: 400 }}>
            <NewsFeed />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
};

export default StrategyInfo;