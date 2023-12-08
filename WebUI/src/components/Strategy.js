import React from 'react';
import { Card, CardContent, Typography, Button } from '@mui/material';

const Strategy = ({ title, strategy_id, onShowInfo }) => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="div">
          {title}
        </Typography>
        <br/>
        <Button key={strategy_id} variant="contained" color="primary" onClick={onShowInfo}>
          Show Info
        </Button>
      </CardContent>
    </Card>
  );
};

export default Strategy;
