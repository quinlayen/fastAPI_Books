#!/bin/bash

FASTAPI_LOG="backend/fastapi.log"
STREAMLIT_LOG="frontend/streamlit.log"


touch $FASTAPI_LOG $STREAMLIT_LOG
chmod 666 $FASTAPI_LOG $STREAMLIT_LOG

source fastapi_env/bin/activate

cd backend
uvicorn main:app --reload >> "../$FASTAPI_LOG" 2>&1 &
cd ..

sleep 3

cd frontend
streamlit run app.py >> "../$STREAMLIT_LOG" 2>&1 &
cd ..

wait