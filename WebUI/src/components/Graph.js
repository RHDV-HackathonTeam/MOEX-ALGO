import { createChart, ColorType, CrosshairMode } from 'lightweight-charts';
import React, { useEffect, useRef } from 'react';

export const Graph = props => {
	const {
		data,
		colors: {
			backgroundColor = '#253248',
			lineColor = '#2962FF',
			textColor = 'white',
			areaTopColor = '#2962FF',
			areaBottomColor = 'rgba(41, 98, 255, 0.28)',
		} = {},
	} = props;

	const chartContainerRef = useRef();

	useEffect(
		() => {
			const handleResize = () => {
				chart.applyOptions({ width: chartContainerRef.current.clientWidth });
			};

			const chart = createChart(chartContainerRef.current, {
				layout: {
					background: { type: ColorType.Solid, color: backgroundColor },
					textColor,
				},
				width: chartContainerRef.current.clientWidth,
				height: 400,
			grid: {
			vertLines: {
				color: '#334158',
			},
			horzLines: {
				color: '#334158',
			},
			},
			crosshair: {
			mode: CrosshairMode.Normal,
			},
			priceScale: {
			borderColor: '#485c7b',
			},
			timeScale: {
			borderColor: '#485c7b',
			},
				});
				chart.timeScale().fitContent();

			const candleSeries = chart.addCandlestickSeries({
				upColor: '#4bffb5',
				downColor: '#ff4976',
				borderDownColor: '#ff4976',
				borderUpColor: '#4bffb5',
				wickDownColor: '#838ca1',
				wickUpColor: '#838ca1',
			});
			
			data.sort((a, b) => new Date(a.Begin) - new Date(b.Begin));

			const transformedData = data.map(item => {
				return {
				  time: item.End.split('T')[0],
				  open: item.Open,
				  high: item.High,
				  low: item.Low,
				  close: item.Close
				};
			  });

			  function calculateSMA(data, period) {
				const smaValues = [];
				for (let i = period - 1; i < data.length; i++) {
				  let sum = 0;
				  for (let j = i; j > i - period; j--) {
					sum += data[j].close;
				  }
				  smaValues.push({ time: data[i].time, value: sum / period });
				}
				return smaValues;
			  }

			  function calculateRSI(data, period) {
				const rsiValues = [];
				let gainSum = 0;
				let lossSum = 0;
			  
				for (let i = 1; i < data.length; i++) {
				  const diff = data[i].close - data[i - 1].close;
				  if (diff > 0) {
					gainSum += diff;
				  } else {
					lossSum -= diff;
				  }
			  
				  if (i >= period) {
					const avgGain = gainSum / period;
					const avgLoss = lossSum / period;
					const rs = avgGain / avgLoss;
					const rsi = 100 - (100 / (1 + rs));
					rsiValues.push({ time: data[i].time, value: rsi });
				  }
				}
				return rsiValues;
			  }
			
			const sma3 = calculateSMA(transformedData, 3);
			const rsi14 = calculateRSI(transformedData, 14);
			
			const strategy = [];
			for (let i = 1; i < rsi14.length; i++) {
				// if (rsi14[i].value > 40 && data[i].close < sma3[i].value) {
				if (rsi14[i].value > 50) {
					strategy.push({ time: rsi14[i].time, position: 'aboveBar', color: 'red', shape: 'arrowDown', text: 'SELL' });
				// } else if (rsi14[i].value < 30 && data[i].close > sma3[i].value) {
				} else if (rsi14[i].value < 35) {
					strategy.push({ time: rsi14[i].time, position: 'belowBar', color: 'green', shape: 'arrowUp', text: 'BUY' });
				}
			}
			console.log("sma", sma3)
			console.log("rsi", rsi14)
			console.log("strategy", strategy)
			candleSeries.setData(transformedData);
			candleSeries.setMarkers(strategy);
			
			const lineSeries1 = chart.addLineSeries({lineColor: "rgba(0,198,0, 1)",lineWidth: 2,});
			lineSeries1.setData(sma3)

			const lineSeries2 = chart.addAreaSeries({lineColor: "rgba(255,0,0, 1)",lineWidth: 2,});
			lineSeries2.setData(rsi14)

			window.addEventListener('resize', handleResize);

			return () => {
				window.removeEventListener('resize', handleResize);

				chart.remove();
			};
		},
		[data, backgroundColor, lineColor, textColor, areaTopColor, areaBottomColor]
	);

	return (
		<div ref={chartContainerRef}/>
	);
};