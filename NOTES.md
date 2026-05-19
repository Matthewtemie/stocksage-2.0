# StockSage 2.0 — Refactor Notes

## Code inventory from StockSage 1.0

### data_pipeline.py
- Lines 51-87: Alpaca client setup
- Lines 90-159: fetch_stock_data() — hits Alpaca API
- Line 120: get_stock_bars() calls 
- Lines 228-325: engineer_features() — computes 13 features and data cleaning
- Lines 328-405: Full pipeline runner

### train_models.py
- Lines 147-223: training all models

### predict_and_notify.py
- Lines 47-127: prediction logic
- Lines 130-256: email/SMTP logic


### app.py
- - Lines 109-140:  DAILY SCHEDULER — runs in both local and production mode

## Refactor decisions / questions


## Things to fix in 2.0
- - engineer_features() is a 100-line god function; each of the 13 features should probably be its own small function
- A 70-line fetch_stock_data() likely mixes API calls, retry logic, and dataframe assembly — same problem

##  Dependencies between files
- app.py imports from: predict_and_notify, data_pipeline
- predict_and_notify.py imports from: data_pipeline, train_models
- train_models.py imports from: data_pipeline
- run.py imports from: all of the above

_legacy/app.py:18:from flask import Flask, render_template, jsonify, request, redirect, url_for
_legacy/app.py:19:import json
_legacy/app.py:20:import os
_legacy/app.py:21:from datetime import datetime
_legacy/app.py:22:from apscheduler.schedulers.background import BackgroundScheduler
_legacy/app.py:24:from data_pipeline import STOCKS
_legacy/app.py:25:from predict_and_notify import predict_all_stocks, send_email
_legacy/data_pipeline.py:25:import pandas as pd
_legacy/data_pipeline.py:26:import numpy as np
_legacy/data_pipeline.py:27:from datetime import datetime, timedelta
_legacy/data_pipeline.py:28:import os
_legacy/data_pipeline.py:29:import json
_legacy/predict_and_notify.py:18:import pandas as pd
_legacy/predict_and_notify.py:19:import numpy as np
_legacy/predict_and_notify.py:20:import json
_legacy/predict_and_notify.py:21:import os
_legacy/predict_and_notify.py:22:import joblib
_legacy/predict_and_notify.py:23:import smtplib
_legacy/predict_and_notify.py:24:from email.mime.text import MIMEText
_legacy/predict_and_notify.py:25:from email.mime.multipart import MIMEMultipart
_legacy/predict_and_notify.py:26:from datetime import datetime, timedelta
_legacy/predict_and_notify.py:28:from data_pipeline import (
_legacy/run.py:17:import sys
_legacy/run.py:18:import os
_legacy/startup.py:7:import os
_legacy/startup.py:13:from data_pipeline import prepare_all_stocks
_legacy/startup.py:14:from train_models import train_all_models
_legacy/startup.py:15:from predict_and_notify import predict_all_stocks
_legacy/train_models.py:34:import pandas as pd
_legacy/train_models.py:35:import numpy as np
_legacy/train_models.py:36:import json
_legacy/train_models.py:37:import os
_legacy/train_models.py:38:import joblib
_legacy/train_models.py:39:from datetime import datetime
_legacy/train_models.py:41:from sklearn.preprocessing import StandardScaler
_legacy/train_models.py:42:from sklearn.linear_model import HuberRegressor
_legacy/train_models.py:43:from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
_legacy/train_models.py:44:from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
_legacy/train_models.py:46:from data_pipeline import STOCKS, FEATURE_COLUMNS, prepare_all_stocks
(venv)

