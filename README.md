
<<<<<<< HEAD
=======
![LangGraph_Node](https://github.com/user-attachments/assets/ca9b183e-3971-4fc2-8174-ecd8bd72a8bf)
>>>>>>> 161a5c6a4539e1432e5bedf87250683349817f1f

# Air Monitor LangGraph

A real-time air quality monitoring system using LangGraph that fetches sensor data, validates it, analyzes conditions, and provides AI-powered recommendations with continuous monitoring.

## Features

- **Real-time Data Fetching**: Connects to ESP32 sensor via HTTP
- **Data Validation**: Comprehensive validation with type and range checking
- **AI Analysis**: Uses OpenAI to generate practical advice based on sensor readings
- **Continuous Monitoring**: Loop node for recurring data collection
- **Logging**: Tracks all operations with timestamps
- **Async Processing**: Non-blocking async/await architecture

## Project Structure

```
air_monitor_LangGraph/
├── main.py           # Entry point
├── graph.py          # LangGraph workflow definition
├── nodes.py          # Node implementations (fetch, validate, analyze, log)
├── state.py          # State type definitions
├── .env              # Environment variables
└── README.md         # This file
```

## Prerequisites

- Python 3.9+
- ESP32 sensor running on `http://localhost:8000/sensor`
- OpenAI API key

## Installation

1. **Clone/Navigate to project**:
   ```bash
   cd /home/hossein/Public/Project/air_monitor_LangGraph
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install langgraph httpx openai python-dotenv
   ```

4. **Create `.env` file**:
   ```env
   OPENAI_API_KEY=your_api_key_here
   OPENAI_BASE_URL=https://api.openai.com/v1
   ```

## Usage

Run the monitoring system:

```bash
python main.py
```

## Workflow

```
START
  ↓
[Fetch Node] → Gets sensor data from ESP32
  ↓
[Validate Node] → Validates temperature, humidity, gas levels
  ↓
[Analyze Node] → Generates AI-powered advice via OpenAI
  ↓
[Logger Node] → Logs results with timestamps
  ↓
[Loop Decision] → Continue monitoring or END
  ↓
(if continue) → Back to Fetch Node
(if stop) → END
```

## Loop Node Implementation

The loop node enables continuous monitoring at intervals:

```python
def loop_node(state):
    """
    Decide whether to continue monitoring or exit.
    Can be based on time, condition, or external signal.
    """
    import time
    
    # Option 1: Time-based loop (monitor every 30 seconds)
    time.sleep(30)
    return {'should_continue': True}
    
    # Option 2: Condition-based (e.g., high pollution)
    if state.get('valid') and state['valid'].get('gas', 0) > 500:
        return {'should_continue': True}  # Continue if high gas
    return {'should_continue': False}
    
    # Option 3: Counter-based (max iterations)
    iterations = state.get('iterations', 0)
    if iterations < 5:
        return {'should_continue': True, 'iterations': iterations + 1}
    return {'should_continue': False}
```

## Sensor Data Format

Expected JSON from ESP32:
```json
{
  "temperature": 22.5,
  "humidity": 45.0,
  "gas": 150.0
}
```

## Validation Rules

| Field | Type | Range |
|-------|------|-------|
| temperature | float/int | -50 to 100 °C |
| humidity | float/int | 0 to 100 % |
| gas | float/int | ≥ 0 ppm |

## Output

The system returns the final state containing:
- `raw`: Original sensor data
- `valid`: Validated sensor data
- `advice`: AI-generated recommendations
- `logs`: Timestamped operation logs

Example output:
```
Final Advice: Consider opening windows to reduce humidity and improve air circulation.
Logs: ['2025-11-15 10:30:45.123456 | raw= {...} | advice= ...']
```

## Loop Node Best Practices

1. **Add delays** between iterations to avoid overwhelming the sensor
2. **Use conditions** to stop monitoring when not needed
3. **Limit iterations** to prevent infinite loops
4. **Update state** to track monitoring sessions
5. **Handle timeouts** gracefully with try-except

## Error Handling

- **ESP32 Unreachable**: Returns error message, skips validation
- **Invalid Data**: Returns `None` for valid field, logs error
- **API Error**: Returns error message instead of advice
- **Loop Timeout**: Breaks loop after max retries
