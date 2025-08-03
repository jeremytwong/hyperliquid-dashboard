"""
main.py – FastAPI proxy for Hyperliquid dashboard
-------------------------------------------------
Streams:
  • Live open positions + open orders
  • Dynamic l2Book (coin from ?coin= query)
REST:
  • Paged historical fills
"""
import os, json, logging
from typing import List, Dict
from urllib.parse import parse_qs

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from hyperliquid.info import Info
from hyperliquid.utils import constants
import websockets
from websockets.exceptions import ConnectionClosed

# ────────── Config ──────────
HL_WS_URL = "wss://api.hyperliquid.xyz/ws"
PORT      = int(os.getenv("PORT", 8000))
ORIGINS   = ["http://localhost:3000", "http://localhost:3001"]
# ───────────────────────────

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logging.getLogger("uvicorn").setLevel(logging.WARNING)

# REST client (no WS from SDK)
info = Info(constants.MAINNET_API_URL, skip_ws=True)


def parse_positions(asset_positions: List[Dict]) -> List[Dict]:
    out = []
    for slot in asset_positions:
        p = slot.get("position") or {}
        if not p:
            continue
        out.append({
            "asset": p.get("coin", ""),
            "size": float(p.get("szi", 0) or 0),
            "entry_price": float(p.get("entryPx", 0) or 0),
            "unrealized_pnl": float(p.get("unrealizedPnl", 0) or 0),
            "leverage": p.get("leverage", {}).get("value", 0),
        })
    return out


def parse_orders(raw: List[Dict]) -> List[Dict]:
    out = []
    for o in raw:
        if "order" in o:
            if o.get("status") not in ("open", "resting", "pending", "openActive"):
                continue
            o = o["order"]
        out.append({
            "oid": o["oid"],
            "coin": o["coin"],
            "side": "Buy" if o["side"] == "B" else "Sell",
            "price": float(o["limitPx"]),
            "size": float(o["sz"]),
            "ts": o["timestamp"],
        })
    return out


def parse_executions(raw_fills: List[Dict]) -> List[Dict]:
    """Parse execution data for historical analysis and CVD calculations"""
    print('ss')
    out = []
    for f in raw_fills:
        # Convert string values to appropriate types
        px = float(f.get("px", 0))
        sz = float(f.get("sz", 0))
        side = f.get("side", "B")  # B for buy, A for ask (sell)
        
        # Calculate notional value
        notional = px * sz
        
        # Determine if it's a buy or sell from user's perspective
        # In Hyperliquid, 'B' means the user bought (taker bought)
        user_side = "Buy" if side == "B" else "Sell"
        
        out.append({
            "time": f.get("time", 0),  # timestamp
            "coin": f.get("coin", ""),
            "side": user_side,
            "px": px,
            "sz": sz,
            "notional": notional,
            "oid": f.get("oid", ""),
            "tid": f.get("tid", ""),  # trade ID
            "fee": float(f.get("fee", 0)),
            "fee_coin": f.get("feeCoin", ""),
        })
    return out


def calculate_cvd(executions: List[Dict], coin: str = None) -> Dict:
    """Calculate Cumulative Volume Delta for executions"""
    if coin:
        executions = [e for e in executions if e["coin"] == coin]
    
    # Sort by timestamp
    executions.sort(key=lambda x: x["time"])
    
    cvd_data = []
    cumulative_delta = 0
    cumulative_volume = 0
    
    for exec_data in executions:
        volume = exec_data["sz"]
        if exec_data["side"] == "Buy":
            delta = volume  # Positive delta for buys
        else:
            delta = -volume  # Negative delta for sells
        
        cumulative_delta += delta
        cumulative_volume += volume
        
        cvd_data.append({
            "time": exec_data["time"],
            "coin": exec_data["coin"],
            "px": exec_data["px"],
            "sz": exec_data["sz"],
            "side": exec_data["side"],
            "delta": delta,
            "cumulative_delta": cumulative_delta,
            "cumulative_volume": cumulative_volume,
            "notional": exec_data["notional"],
        })
    
    return {
        "cvd_data": cvd_data,
        "total_delta": cumulative_delta,
        "total_volume": cumulative_volume,
        "coin": coin,
        "trade_count": len(cvd_data)
    }


def make_orderbook_payload(levels, max_levels: int = 20) -> List[Dict]:
    bids_raw, asks_raw = levels
    bids = bids_raw[:max_levels]
    asks = asks_raw[:max_levels]
    if not bids or not asks:
        return []
    mid = (float(bids[0]["px"]) + float(asks[0]["px"])) / 2
    rows = []
    for lvl in bids:
        px, sz = float(lvl["px"]), float(lvl["sz"])
        rows.append({"side": "bid", "px": px, "sz": sz,
                     "bps": round((mid - px)/mid*1e4, 2)})
    for lvl in asks:
        px, sz = float(lvl["px"]), float(lvl["sz"])
        rows.append({"side": "ask", "px": px, "sz": sz,
                     "bps": round((px - mid)/mid*1e4, 2)})
    rows.sort(key=lambda r: r["bps"])
    return rows


@app.websocket("/ws/{wallet}")
async def live_stream(ws: WebSocket, wallet: str):
    # parse optional ?coin=ETH
    qs = parse_qs(ws.scope["query_string"].decode())
    coin = qs.get("coin", ["BTC"])[0].upper()

    await ws.accept()

    positions: List[Dict] = []
    orders: Dict[int, Dict] = {}
    orderbook: List[Dict] = []

    # seed open orders via REST
    try:
        for o in info.frontend_open_orders(wallet) or []:
            orders[o["oid"]] = {"order": o, "status": "open"}
    except Exception:
        logging.warning("open-orders snapshot failed", exc_info=True)

    try:
        async with websockets.connect(HL_WS_URL, ping_interval=None) as hl:
            # subscribe positions + orders
            await hl.send(json.dumps({
                "method": "subscribe",
                "subscription": {"type": "webData2", "user": wallet}
            }))
            await hl.send(json.dumps({
                "method": "subscribe",
                "subscription": {"type": "orderUpdates", "user": wallet}
            }))
            # dynamic book for chosen coin
            await hl.send(json.dumps({
                "method": "subscribe",
                "subscription": {"type": "l2Book", "coin": coin}
            }))

            while True:
                msg = json.loads(await hl.recv())
                ch = msg.get("channel")

                if ch == "webData2":
                    ap = msg["data"].get("clearinghouseState", {}) \
                                 .get("assetPositions", [])
                    positions = parse_positions(ap)

                elif ch == "orderUpdates":
                    for upd in msg["data"]:
                        oid = upd["order"]["oid"]
                        if upd["status"] in ("open","resting","pending","openActive"):
                            orders[oid] = upd
                        else:
                            orders.pop(oid, None)

                elif ch == "l2Book":
                    orderbook = make_orderbook_payload(msg["data"]["levels"])

                # safe send
                try:
                    await ws.send_json({
                        "positions": positions,
                        "open_orders": parse_orders(list(orders.values())),
                        "orderbook": orderbook,
                    })
                except (WebSocketDisconnect, ConnectionClosed):
                    break

    except Exception:
        logging.exception("WS proxy error")
    finally:
        await ws.close()


@app.get("/executions/{wallet}")
async def executions(wallet: str, limit: int = 10, page: int = 1):
    try:
        fills = info.user_fills(wallet)
        start, end = (page-1)*limit, page*limit
        slice_ = fills[start:end]
        for f in slice_:
            f["px"] = float(f["px"]); f["sz"] = float(f["sz"])
        return {"executions": slice_, "has_more": end<len(fills), "page": page}
    except Exception as e:
        return {"executions": [], "has_more": False, "page": page, "error": str(e)}


@app.get("/open_orders/{wallet}")
async def open_orders_snapshot(wallet: str):
    try:
        raw = info.frontend_open_orders(wallet) or []
        return {"open_orders": parse_orders(raw)}
    except Exception as e:
        return {"open_orders": [], "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, reload=True)
