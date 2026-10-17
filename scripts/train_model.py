"""Train one LinearRegression model with a chronological held-out test set."""
import json
import os
from pathlib import Path
import platform

os.environ.setdefault('MPLCONFIGDIR', str(Path(__file__).resolve().parents[1] / '.mplconfig'))

import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ['temperature_c', 'humidity_percent', 'wind_speed_ms']


def scores(y, prediction):
    return {'mae': float(mean_absolute_error(y, prediction)),
            'rmse': float(np.sqrt(mean_squared_error(y, prediction))),
            'r2': float(r2_score(y, prediction))}


def main():
    data = pd.read_csv(ROOT / 'data/processed/airpredict_daily.csv').sort_values('date')
    if data['date'].duplicated().any() or not np.isfinite(data[FEATURES + ['pm25']]).all().all():
        raise ValueError('Dataset has duplicates or invalid numeric values')
    split = int(len(data) * .8)
    train, test = data.iloc[:split], data.iloc[split:]
    model = LinearRegression().fit(train[FEATURES], train['pm25'])
    prediction = model.predict(test[FEATURES])
    baseline = np.full(len(test), train['pm25'].mean())
    report = {
        'model': 'Linear Regression', 'station': 'Chulalongkorn Hospital',
        'sensor_id': 1304222, 'features': FEATURES, 'rows': len(data),
        'split': 'chronological 80/20; no shuffling; model fitted only on training rows',
        'train': {'rows': len(train), 'start': train.iloc[0]['date'], 'end': train.iloc[-1]['date']},
        'test': {'rows': len(test), 'start': test.iloc[0]['date'], 'end': test.iloc[-1]['date']},
        'metrics': scores(test['pm25'], prediction),
        'baseline': scores(test['pm25'], baseline),
        'baseline_method': 'training-set mean PM2.5',
        'intercept': float(model.intercept_),
        'coefficients': dict(zip(FEATURES, map(float, model.coef_))),
        'training_ranges': {key: {'min': float(train[key].min()), 'max': float(train[key].max())} for key in FEATURES},
        'negative_test_predictions': int((prediction < 0).sum()),
        'versions': {'python': platform.python_version(), 'scikit_learn': sklearn.__version__},
        'limitations': ['Missing days are seasonally uneven.',
                       'NASA weather is gridded, not a co-located station measurement.',
                       'Inputs represent daily averages; wind speed is at 10 m.',
                       'Historical estimation experiment, not a validated real-time forecast.'],
    }
    artifacts = ROOT / 'models'
    artifacts.mkdir(exist_ok=True)
    joblib.dump({'model': model, 'features': FEATURES, 'report': report}, artifacts / 'linear_regression.joblib')
    reports = ROOT / 'reports'
    reports.mkdir(exist_ok=True)
    (reports / 'metrics.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    pd.DataFrame({'date': test['date'], 'actual_pm25': test['pm25'],
                  'predicted_pm25': prediction, 'baseline_pm25': baseline}).to_csv(reports / 'test_predictions.csv', index=False)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), layout='constrained')
    axes[0].scatter(test['pm25'], prediction, c='#0b8278', alpha=.7, s=24)
    low = min(0, float(prediction.min()))
    high = max(float(test['pm25'].max()), float(prediction.max()))
    axes[0].plot([low, high], [low, high], '--', c='#a8aeb5')
    axes[0].set(xlabel='Actual PM2.5 (µg/m³)', ylabel='Predicted PM2.5 (µg/m³)', title='Held-out test: actual vs predicted')
    axes[1].plot(pd.to_datetime(test['date']), test['pm25'], label='Actual', color='#26384d')
    axes[1].plot(pd.to_datetime(test['date']), prediction, label='Predicted', color='#0b8278')
    axes[1].set(ylabel='PM2.5 (µg/m³)', title='Chronological test period')
    axes[1].legend(frameon=False)
    axes[1].tick_params(axis='x', rotation=25)
    fig.savefig(reports / 'evaluation.png', dpi=160)
    plt.close(fig)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
