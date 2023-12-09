import React, { useState, useEffect } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import { Button, Modal, TextField, Box, Select, MenuItem } from '@mui/material';
import Strategy from './components/Strategy';
import StrategyInfo from './components/StrategyInfo';
import theme from './theme';
import axios from 'axios';

import "./components/graphstyles.css"

const strategies_list = [
  { title: 'Strategy SMA RSI 1', from: '2022/01/27', to: '2023/12/27', ticker: 'ALRS', profitability: '11', riskreward: '1/3', riskondeal: '2', maxloss: '122', maxdayloss: '278' },
];

function App() {
  const [selectedStrategy, setSelectedStrategy] = useState(null);
  const [openModal, setOpenModal] = useState(false);
  const [formData, setFormData] = useState({});
  const [strategies, setStrategies] = useState(strategies_list);
  const [tickers, setTickers] = useState([]);
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [forceRerender, setForceRerender] = useState(false);

  useEffect(() => {
    axios.get('http://localhost:9878/api/ticker/ticker_list')
      .then(response => {
        setTickers(response.data.tickers);
      })
      .catch(error => {
        console.error('Error fetching tickers:', error);
      });
    
  }, []);

 
  const handleShowInfo = (btn) => {
    const matches = btn.target.parentElement.textContent.match(/\d+/);
    let num = parseInt(matches[0]);
    setSelectedStrategy(strategies[num-1]);

    let originalDate = strategies[num-1].from;
    let modifiedDate = originalDate.replace(/\//g, '-');

    let originalDate2 = strategies[num-1].to;
    let modifiedDate2 = originalDate2.replace(/\//g, '-');

    const rdata = {
      ticker: strategies[num-1].ticker,
      from_date: modifiedDate,
      to_date: modifiedDate2,
      time_period: 'D'
    };

      const fetchData = async () => {
        try {
          const response = await axios.post('http://localhost:9878/api/ticker/get_candles', rdata);
          setData(response.data.candles);
          console.log(response.data.candles);
          setLoading(false); // Set loading to false when data arrives
        } catch (error) {
          console.error('Error fetching data:', error);
          setLoading(false); // Set loading to false in case of an error
        }
      };

    fetchData();
    setForceRerender(prev => !prev);
    // console.log(selectedStrategy)
  };

  const handleOpenModal = () => {
    setOpenModal(true);
  };

  const handleCloseModal = () => {
    setOpenModal(false);
  };

  const handleFormChange = (e) => {
    if (e.target && e.target.name) {
      console.log(e.target)
      setFormData({ ...formData, [e.target.name]: e.target.value });
    }
  };

  const handleSend = () => {

    let originalDate = formData.from;
    let modifiedDate = originalDate.replace(/\//g, '-');

    let originalDate2 = formData.to;
    let modifiedDate2 = originalDate.replace(/\//g, '-');

    const rdata = {
      ticker: formData.ticker,
      from_date: modifiedDate,
      to_date: modifiedDate2,
      time_period: 'D'
    };

    axios.post('http://localhost:9878/api/ticker/get_candles', rdata)
      .then(response => {
        setFormData(response.data.candles);
      })
      .catch(error => {
        console.error('Error fetching news:', error);
      });


      const newStrategy = {
        title: formData.title,
        from: formData.from,
        to: formData.to,
        ticker: formData.ticker,
        profitability: formData.profitability,
        riskreward: formData.riskreward,
        riskondeal: formData.riskondeal,
        maxdayloss: formData.maxdayloss,
        maxloss: formData.maxloss,
      };
  
      setStrategies([...strategies, newStrategy]);
      handleCloseModal();
  };

  useEffect(() => {
    const storedStrategies = JSON.parse(localStorage.getItem('strategies'));
    if (storedStrategies) {
      setStrategies(storedStrategies);
    }
  }, []);

  return (
      <ThemeProvider theme={theme}>
        <div className="App">
          <header className="header">
            <div className="header__logo">RHDV.dev</div>
          </header>
        <section className="sidebar">

          <div className="card" style={{ display: 'flex', gap: '20px' }}>
            {strategies.map((strategy, index) => (
              <Strategy
                key={index}
                title={strategy.title}
                strategy_id={strategy.id}
                onShowInfo={handleShowInfo}
              />
            ))}
            <Button variant="contained" color="primary" onClick={handleOpenModal}>
              Add
            </Button>
          </div>
        </section>

          <div>
            {selectedStrategy && <StrategyInfo data={selectedStrategy}/>}
          </div>
          <Modal open={openModal} onClose={handleCloseModal} style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '3px' }}>
          <Box sx={{ bgcolor: 'background.paper', p: 4, width: 300 }}>
            <form>
              <TextField name="title" label="Title" onChange={handleFormChange} fullWidth sx={{ mb: 4 }}/>
              <TextField name="from" label="From: YYYY/MM/DD" onChange={handleFormChange} fullWidth sx={{ mb: 4 }} slotProps={{ textField: { variant: 'outlined' } }}/>
              <TextField name="to"label="To: YYYY/MM/DD" onChange={handleFormChange} fullWidth sx={{ mb: 4 }} slotProps={{ textField: { variant: 'outlined' } }}/>
              <Select
                name="ticker"
                label="Ticker"
                value={formData.ticker || ''}
                onChange={handleFormChange}
                fullWidth
                sx={{ mb: 4 }}
              >
                {tickers.map((ticker, index) => (
                  <MenuItem key={index} value={ticker}>
                    {ticker}
                  </MenuItem>
                ))}
              </Select>
              <TextField name="riskreward" label="Risk-Reward ratio (1/3)" onChange={handleFormChange} fullWidth sx={{ mb: 4 }}/>
              <TextField name="riskondeal" label="Risk on deal (1%)" onChange={handleFormChange} fullWidth sx={{ mb: 4 }}/>
              <Button variant="contained" color="primary" onClick={handleSend} fullWidth>
                Send
              </Button>
            </form>
          </Box>
        </Modal>
        </div>
      </ThemeProvider>
  );
}

export default App;