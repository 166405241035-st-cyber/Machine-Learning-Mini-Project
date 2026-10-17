"""AirPredict local Flask application. Run train_model.py before starting."""
import math
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_from_directory
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parent
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8192


def load_bundle():
    path = ROOT / 'models/linear_regression.joblib'
    return joblib.load(path) if path.exists() else None


@app.get('/')
def index():
    bundle = load_bundle()
    return render_template('index.html', report=bundle['report'] if bundle else None)


@app.post('/api/predict')
def predict():
    bundle = load_bundle()
    if bundle is None:
        return jsonify(error='ยังไม่มีโมเดล กรุณารัน scripts/train_model.py ก่อน'), 503
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error='กรุณาส่งข้อมูลเป็น JSON object'), 400
    bounds = {'temperature_c': (-10, 60), 'humidity_percent': (0, 100), 'wind_speed_ms': (0, 60)}
    values = {}
    for field, (low, high) in bounds.items():
        value = payload.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            return jsonify(error=f'{field}: กรุณาระบุตัวเลขที่ถูกต้อง'), 400
        if not low <= value <= high:
            return jsonify(error=f'{field}: ต้องอยู่ระหว่าง {low} ถึง {high}'), 400
        values[field] = value
    result = float(bundle['model'].predict(pd.DataFrame([values], columns=bundle['features']))[0])
    if not math.isfinite(result):
        return jsonify(error='โมเดลไม่สามารถคำนวณผลได้'), 422
    outside = [field for field, value in values.items()
               if not bundle['report']['training_ranges'][field]['min'] <= value <= bundle['report']['training_ranges'][field]['max']]
    warnings = []
    if outside:
        warnings.append('ข้อมูลบางค่าอยู่นอกช่วงชุดฝึก ผลประมาณอาจไม่น่าเชื่อถือ')
    if result < 0:
        warnings.append('โมเดลให้ค่าติดลบ ซึ่งไม่มีความหมายทางกายภาพ จึงไม่แสดงเป็นปริมาณฝุ่น')
    return jsonify(pm25=round(result, 2) if result >= 0 else None,
                   raw_prediction=round(result, 2), warnings=warnings, outside_training_range=outside)


@app.get('/evaluation.png')
def evaluation():
    return send_from_directory(ROOT / 'reports', 'evaluation.png')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
