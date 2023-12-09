import React, { useEffect, useState } from 'react';
import { Card, CardContent, Typography, Button } from '@mui/material';
import axios from 'axios';

// const news = [
//   { tone: "positive", title: 'yjdcnm ngfh dfgdfg', link: "https://google.com/" },
//   { tone: "negative", title: 'fdg dfgdfgd 2', link: "https://google.com/" },
//   { tone: "positive", title: 'dfgggggggggggg 3', link: "https://google.com/" },
//   { tone: "negative", title: 'fghdfhgfdhfdghf 4kjhdfbg kjhdbfkjghbdkjfhbkjdhbfgkjhdbf gkjhdfb gkjdhfbgjkdf hjkdfhbkjdfh kjdfhgjkdfh jkdfhbkjdhfgkjdhfg', link: "https://google.com/" },
//   { tone: "negative", title: 'fghdfhgfdhfdghf 4kjhdfbg kjhdbfkjghbdkjfhbkjdhbfgkjhdbf gkjhdfb gkjdhfbgjkdf hjkdfhbkjdfh kjdfhgjkdfh jkdfhbkjdhfgkjdhfg', link: "https://google.com/" },
//   { tone: "negative", title: 'fghdfhgfdhfdghf 4kjhdfbg kjhdbfkjghbdkjfhbkjdhbfgkjhdbf gkjhdfb gkjdhfbgjkdf hjkdfhbkjdfh kjdfhgjkdfh jkdfhbkjdhfgkjdhfg', link: "https://google.com/" },
//   { tone: "negative", title: 'fghdfhgfdhfdghf 4kjhdfbg kjhdbfkjghbdkjfhbkjdhbfgkjhdbf gkjhdfb gkjdhfbgjkdf hjkdfhbkjdfh kjdfhgjkdfh jkdfhbkjdhfgkjdhfg', link: "https://google.com/" },
// ];

const NewsFeed = (props) => {

  const [news, setNews] = useState([]);
  const [tickerNews, setTickerNews] = useState([]);
  
  useEffect(() => {
    axios.get('http://localhost:9878/api/news/get_all_news')
      .then(response => {
        setNews(response.data);
      })
      .catch(error => {
        console.error('Error fetching news:', error);
      });
    let pdata = {
      ticker: props.ticker
    }
    axios.post('http://localhost:9878/api/news/get_news_by_ticker', pdata)
      .then(response => {
        setTickerNews(response.data);
      })
      .catch(error => {
        console.error('Error fetching news:', error);
      });
  }, []); 

  useEffect(() => {
    
  }, []); 

  const onLink = (link) => {
    window.open(link, '_blank');
  };
  
  return (
    <div>
      <div>
        <Button variant="contained" color="primary" style={{ marginRight: '10px' }} onClick={() => setTickerNews()}>
          By Ticker
        </Button>
        <Button variant="contained" color="primary" onClick={() => setNews([])}>
          All
        </Button>
      </div>
      <div style={{ height: '400px', overflow: 'auto' }}>
        {tickerNews.length > 0 ? tickerNews.map((item, index) => (
          <Card key={index} style={{ marginBottom: '3px', display: 'flex', alignItems: 'center' }}>
            <CardContent style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
              <div>                                         
                <Typography variant="body" component="div">{item.text ? item.text.split('\.')[0] : null}</Typography>
                <Typography variant="h6" >{item.source}</Typography>
              </div>
              <Button variant="contained" color="primary" onClick={() => onLink(item.link)}>
                Link
              </Button>
            </CardContent>
          </Card>
        )) : news.map((item, index) => (
          <Card key={index} style={{ marginBottom: '3px', display: 'flex', alignItems: 'center' }}>
            <CardContent style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
              <div>                                         
                <Typography variant="body" component="div">{item.text ? item.text.split('\.')[0] : null}</Typography>
                <Typography variant="h6" >{item.source}</Typography>
              </div>
              <Button variant="contained" color="primary" onClick={() => onLink(item.link)}>
                Link
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default NewsFeed;
