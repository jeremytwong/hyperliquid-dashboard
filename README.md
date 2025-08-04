# Hyperliquid Dashboard

A real-time trading dashboard for Hyperliquid exchange with live position tracking, order management, and market data visualization.

## 🚀 Features

- **Live Position Tracking**: Real-time monitoring of open positions and PnL
- **Order Management**: View and manage open orders
- **Market Data**: Live L2 order book data with depth analysis
- **Advanced Analytics**: 
  - CVD (Cumulative Volume Delta) calculations
  - Spread analysis and monitoring
  - Market depth calculations
  - Orderbook bar graph visualization
- **Historical Analysis**: Trade execution history with detailed metrics
- **Responsive UI**: Modern React interface with Tailwind CSS
- **Real-time Updates**: WebSocket connections for live data streaming

## 🏗️ Project Structure

```
hyperliquid-dashboard/
├── backend/                 # FastAPI Python backend
│   ├── main.py             # Main FastAPI application
│   └── main2.py            # Additional backend functionality
├── frontend/               # React frontend application
│   ├── src/                # React source code
│   ├── public/             # Static assets
│   ├── package.json        # Node.js dependencies
│   └── tailwind.config.js  # Tailwind CSS configuration
└── README.md               # This file
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **WebSockets**: Real-time data streaming
- **Hyperliquid SDK**: Official Hyperliquid API integration
- **Uvicorn**: ASGI server

### Frontend
- **React 18**: Modern React with hooks
- **Tailwind CSS**: Utility-first CSS framework
- **Chart.js**: Interactive charts and graphs
- **React Chart.js 2**: React wrapper for Chart.js
- **Recharts**: Additional charting library

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- Hyperliquid account address

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/hyperliquid-dashboard.git
cd hyperliquid-dashboard
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
python main.py
```

The backend will start on `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will start on `http://localhost:3000`

## 🔧 Configuration

### Environment Variables (Optional)

The backend uses minimal configuration. You can optionally create a `.env` file in the backend directory:

```env
PORT=8000
```

### CORS Configuration

The backend is configured to allow requests from:
- `http://localhost:3000`
- `http://localhost:3001`

## 📡 API Endpoints

### WebSocket Endpoints
- `ws://localhost:8000/ws/{wallet}` - Live position and order streaming
- Query parameter `?coin=ETH` for specific coin data

### REST Endpoints
- `GET /executions/{wallet}` - Historical trade executions
- `GET /open_orders/{wallet}` - Current open orders

## 🎯 Usage

1. **Connect Wallet**: Enter your Hyperliquid wallet address
2. **View Positions**: Monitor your open positions and unrealized PnL
3. **Track Orders**: View pending and open orders
4. **Analyze Market Data**: 
   - View live orderbook with depth visualization
   - Monitor CVD (Cumulative Volume Delta) trends
   - Track spread analysis and market depth
   - Analyze historical trade executions
5. **Visualize Data**: Interactive charts and bar graphs for market analysis

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is for educational and informational purposes only. Trading cryptocurrencies involves substantial risk of loss and is not suitable for all investors. The value of cryptocurrencies can go down as well as up, and you may lose some or all of your investment.

## 🔗 Links

- [Hyperliquid Exchange](https://hyperliquid.xyz/)
- [Hyperliquid API Documentation](https://hyperliquid.gitbook.io/hyperliquid/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/) 
