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

			candleSeries.setData(data[1]);
			candleSeries.setMarkers(data[2]);

			window.addEventListener('resize', handleResize);

			return () => {
				window.removeEventListener('resize', handleResize);

				chart.remove();
			};
		},
		[data, backgroundColor, lineColor, textColor, areaTopColor, areaBottomColor]
	);

	return (
		<div
			ref={chartContainerRef}
		/>
	);
};