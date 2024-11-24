// App.js
import React, { useState } from 'react';
import CandlestickChart from './components/Chart';

const App = () => {
    const [symbol, setSymbol] = useState('AAPL');

    return (
        <div>
            <h1>Interactive Candlestick Chart</h1>
            <CandlestickChart symbol={symbol} />
        </div>
    );
};

export default App;
