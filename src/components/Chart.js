// Charts.js
import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';

const CandlestickChart = ({ symbol = 'AAPL' }) => {
    const [chartData, setChartData] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Fetch the candlestick chart data from the Flask API
        fetch(`http://127.0.0.1:5000/combined-chart?symbol=${symbol}`)
            .then((response) => response.json())
            .then((data) => {
                if (data.error) {
                    setError(data.error); // Handle error if no data is returned
                } else {
                    setChartData(data); // Set the chart data
                }
            })
            .catch((error) => {
                console.error('Error fetching chart data:', error);
                setError("Error fetching chart data.");
            });
    }, [symbol]);

    if (error) {
        return <div>{error}</div>;
    }

    console.log(chartData);
    
    return (
        <div>
            {chartData ? (
                <Plot
                    data={chartData.data}
                    layout={chartData.layout}
                    config={{ responsive: true }} // Makes the chart responsive
                />
            ) : (
                <p>Loading candlestick chart...</p>
            )}
        </div>
    );
};

export default CandlestickChart;
