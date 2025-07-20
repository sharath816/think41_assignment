# Live Polling Management API (Think41 Assignment)

This is a FastAPI-based backend service for creating and managing live polls, voting on options, and retrieving results.

##  Files Present

>  Only `main.py` is currently implemented in this repository. The remaining modules (`models.py`, `schemas.py`, `database.py`, etc.) need to be created as per the structure described below.

---

##  Features Implemented in `main.py`

- **Create Poll**: `POST /polls`
- **Vote on Poll**: `POST /polls/{poll_str_id}/vote`
- **Get Poll Results**: `GET /polls/{poll_str_id}/results`
- **List Active Polls**: `GET /polls/active`
- **Close a Poll**: `PUT /polls/{poll_str_id}/status`

---

##  Project Structure (to be built)

```
live_polling_api/
├── main.py                (Implemented)
├── models.py              (To be created)
├── schemas.py             (To be created)
├── database.py            (To be created)
├── requirements.txt       (To be created)
└── README.md             
```

---

##  How to Run (once all files are ready)

1. Install dependencies:
```bash
pip install fastapi uvicorn sqlalchemy
```

2. Run the API server:
```bash
uvicorn main:app --reload
```

---

##  Author

Sharath M T  
GitHub: [sharath816](https://github.com/sharath816)