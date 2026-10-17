"""Reproduce explanatory plots without refitting or tuning the model."""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.mplconfig'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

FEATURES = ['temperature_c', 'humidity_percent', 'wind_speed_ms']
LABELS = ['Temperature (°C)', 'Relative humidity (%)', 'Wind speed at 10 m (m/s)']
COLOR = '#127c70'


def main():
    data = pd.read_csv(ROOT / 'data/processed/airpredict_daily.csv').sort_values('date')
    report = json.loads((ROOT / 'reports/metrics.json').read_text())
    prediction = pd.read_csv(ROOT / 'reports/test_predictions.csv')
    train = data[data.date <= report['train']['end']]
    test = data[data.date >= report['test']['start']]
    assert len(train) == report['train']['rows'] and len(test) == report['test']['rows']
    assert list(test.date) == list(prediction.date)
    assert np.allclose(test.pm25, prediction.actual_pm25)
    out = ROOT / 'docs/analysis'
    figs = out / 'figures'
    figs.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'svg.hashsalt': 'airpredict-analysis-v1',
                         'font.family': 'DejaVu Sans', 'font.size': 10, 'axes.spines.top': False,
                         'axes.spines.right': False, 'figure.facecolor': 'white'})

    def save(fig, name):
        fig.savefig(figs / f'{name}.png', dpi=180, bbox_inches='tight')
        fig.savefig(figs / f'{name}.svg', bbox_inches='tight', metadata={'Date': None})
        plt.close(fig)

    # Primary explanatory analysis uses training data only.
    corr = train[FEATURES + ['pm25']].corr()
    fig, axes = plt.subplots(1, 3, figsize=(13, 4), layout='constrained')
    for ax, field, label in zip(axes, FEATURES, LABELS):
        ax.scatter(train[field], train.pm25, alpha=.45, s=15, color=COLOR)
        slope, intercept = np.polyfit(train[field], train.pm25, 1)
        x = np.array([train[field].min(), train[field].max()])
        ax.plot(x, intercept + slope * x, color='#d88c36', linewidth=2)
        ax.set(xlabel=label, ylabel='PM2.5 (µg/m³)', title=f'Pearson r = {corr.loc[field, "pm25"]:.3f}')
    fig.suptitle(f'Weather and PM2.5 | training data only (n={len(train)})\nOrange line: separate univariate trend, not the multivariable model', fontsize=12)
    save(fig, '01_weather_relationships')

    fig, ax = plt.subplots(figsize=(7, 5.7), layout='constrained')
    im = ax.imshow(corr, vmin=-1, vmax=1, cmap='BrBG')
    short = ['Temperature', 'Humidity', 'Wind speed', 'PM2.5']
    ax.set_xticks(range(4), short, rotation=20)
    ax.set_yticks(range(4), short)
    for i in range(4):
        for j in range(4):
            ax.text(j, i, f'{corr.iloc[i, j]:.3f}', ha='center', va='center', color='white' if abs(corr.iloc[i,j]) > .65 else '#17332c')
    fig.colorbar(im, ax=ax, label='Pearson correlation')
    ax.set_title('Pairwise correlations | training data only')
    save(fig, '02_correlations')

    # Compare coefficients after expressing each predictor change as one training SD.
    effects = pd.Series(report['coefficients']) * train[FEATURES].std(ddof=1)
    fig, ax = plt.subplots(figsize=(8, 4), layout='constrained')
    ax.barh(LABELS, effects.values, color=COLOR)
    ax.axvline(0, color='#67756f', linewidth=1)
    ax.set(xlabel='Change in predicted PM2.5 per +1 training SD (µg/m³)',
           title='Conditional model effects | other predictors held fixed')
    for i, value in enumerate(effects):
        ax.text(value, i, f' {value:.2f} ', va='center', ha='right' if value < 0 else 'left')
    ax.margins(x=.25)
    save(fig, '03_coefficient_effects')

    residual = prediction.actual_pm25 - prediction.predicted_pm25
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), layout='constrained')
    axes[0].scatter(prediction.actual_pm25, prediction.predicted_pm25, color=COLOR, s=22, alpha=.7)
    low = min(prediction.actual_pm25.min(), prediction.predicted_pm25.min())
    high = max(prediction.actual_pm25.max(), prediction.predicted_pm25.max())
    axes[0].plot([low, high], [low, high], '--', color='#d88c36')
    axes[0].set(xlabel='Actual PM2.5 (µg/m³)', ylabel='Predicted PM2.5 (µg/m³)', title='Held-out predictions vs actual')
    axes[1].scatter(prediction.predicted_pm25, residual, color=COLOR, s=22, alpha=.7)
    axes[1].axhline(0, linestyle='--', color='#d88c36')
    axes[1].set(xlabel='Predicted PM2.5 (µg/m³)', ylabel='Residual: actual − predicted (µg/m³)', title='Positive residual = underestimation')
    save(fig, '04_prediction_residuals')

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), layout='constrained')
    x = np.arange(2)
    model_scores = [report['metrics']['mae'], report['metrics']['rmse']]
    baseline_scores = [report['baseline']['mae'], report['baseline']['rmse']]
    axes[0].bar(x-.18, model_scores, .36, label='Linear Regression', color=COLOR)
    axes[0].bar(x+.18, baseline_scores, .36, label='Training-mean baseline', color='#b9c9c0')
    axes[0].set_xticks(x, ['MAE', 'RMSE'])
    axes[0].set(ylabel='Error (µg/m³); lower is better', title='Same 98 held-out days')
    axes[0].legend(fontsize=8)
    for i in range(2):
        axes[0].text(i-.18, model_scores[i]+.1, f'{model_scores[i]:.2f}', ha='center')
        axes[0].text(i+.18, baseline_scores[i]+.1, f'{baseline_scores[i]:.2f}', ha='center')
    dates = pd.to_datetime(prediction.date)
    # Show observations as points: lines would imply continuity across missing days.
    axes[1].scatter(dates, prediction.actual_pm25, label='Actual', color='#314d62', s=15)
    axes[1].scatter(dates, prediction.predicted_pm25, label='Predicted', color=COLOR, s=15)
    axes[1].set(ylabel='PM2.5 (µg/m³)', title='Test observations across time (gaps retained)')
    axes[1].tick_params(axis='x', rotation=30)
    axes[1].legend(fontsize=8)
    save(fig, '05_test_performance')

    months = pd.period_range('2024-01', '2025-12', freq='M')
    counts = pd.to_datetime(data.date).dt.to_period('M').value_counts().reindex(months, fill_value=0)
    fig, ax = plt.subplots(figsize=(12, 4), layout='constrained')
    ax.bar(range(24), [p.days_in_month for p in months], color='#e2e9e4', label='Calendar days')
    ax.bar(range(24), counts.values, color=COLOR, label='Usable matched days')
    ax.set_xticks(range(24), [str(p) for p in months], rotation=60)
    ax.set(ylabel='Days', title='Missingness by month | full dataset, data-quality analysis only')
    ax.legend(fontsize=8)
    save(fig, '06_monthly_completeness')

    improvement = (1-report['metrics']['mae']/report['baseline']['mae'])*100
    stats = {'training_correlations': corr.to_dict(), 'effects_per_training_sd': effects.to_dict(),
             'mean_test_residual': float(residual.mean()), 'test_underestimated_days': int((residual>0).sum()),
             'test_overestimated_days': int((residual<0).sum()), 'mae_improvement_percent': improvement,
             'usable_days_by_month': {str(k): int(v) for k,v in counts.items()}}
    (out / 'analysis_statistics.json').write_text(json.dumps(stats, indent=2), encoding='utf-8')
    rows = '\n'.join(f'| {label} | {corr.loc[field,"pm25"]:.3f} | {report["coefficients"][field]:.4f} | {effects[field]:.2f} |' for field,label in zip(FEATURES,['อุณหภูมิ','ความชื้นสัมพัทธ์','ความเร็วลม']))
    narrative = f'''# การวิเคราะห์ข้อมูลและโมเดล AirPredict

โครงงานนี้ศึกษาว่าอุณหภูมิ ความชื้นสัมพัทธ์ และความเร็วลมช่วยประมาณ PM2.5 บริเวณโรงพยาบาลจุฬาลงกรณ์ได้เพียงใด ผลทดสอบย้อนหลังแสดงว่า Linear Regression มี MAE {report['metrics']['mae']:.2f} µg/m³ ต่ำกว่าวิธีใช้ค่าเฉลี่ยชุดฝึก แต่ผลยังจำกัดด้วยข้อมูลที่ขาดตามฤดูกาลและพื้นที่ศึกษาเดียว

## ข้อมูลและวิธีวิเคราะห์

ใช้ข้อมูลจริงที่ผ่านเกณฑ์ 490 วันจากปี 2024–2025 โดยนำ PM2.5 จาก OpenAQ มาจับคู่กับอากาศ NASA POWER ในช่วงเวลาเดียวกัน หน่วยคืออุณหภูมิ °C ความชื้น % และลม m/s ที่ความสูง 10 เมตร คัดฝุ่นที่มี coverage อย่างน้อย 75% ไม่มี quality flag และไม่ติดลบ ต้องมีอากาศครบ 24 ชั่วโมง ไม่เติมค่าขาด

แบ่งตามเวลาเป็นชุดฝึก 392 วัน (2024-01-01 ถึง 2025-06-12) และชุดทดสอบ 98 วัน (2025-06-13 ถึง 2025-12-31) กราฟความสัมพันธ์และการตีความสัมประสิทธิ์ใช้ชุดฝึกเท่านั้น ส่วนชุดทดสอบใช้ประเมินโมเดลที่ตรึงไว้แล้ว ไม่มีการปรับโมเดลตามกราฟชุดทดสอบ

## ความสัมพันธ์ของสภาพอากาศกับ PM2.5

![ความสัมพันธ์กับฝุ่น](figures/01_weather_relationships.svg)

แต่ละจุดแทนวันหนึ่งในชุดฝึก เส้นสีส้มเป็นแนวโน้มเชิงเส้นที่วิเคราะห์ทีละตัวแปร ไม่ใช่เส้นของโมเดลหลายตัวแปร ค่า Pearson r วัดทิศทางและระดับความสัมพันธ์เชิงเส้นแบบจับคู่ ค่าติดลบหมายถึงในข้อมูลนี้ ตัวแปรที่สูงขึ้นมักพบร่วมกับ PM2.5 ที่ต่ำลง ไม่พิสูจน์ว่าตัวแปรนั้นเป็นสาเหตุให้ฝุ่นลด

| ตัวแปร | Pearson r กับ PM2.5 ในชุดฝึก | สัมประสิทธิ์ในหน่วยเดิม | ผลต่อ PM2.5 เมื่อเพิ่ม 1 SD ของชุดฝึก |
|---|---:|---:|---:|
{rows}

ผลที่พบในชุดฝึกคือความชื้นมีความสัมพันธ์เชิงเส้นแบบจับคู่กับ PM2.5 ชัดที่สุดในสามตัวแปร (r≈−0.674) ขณะที่อุณหภูมิ (r≈−0.020) และลม (r≈−0.101) มีความสัมพันธ์แบบจับคู่ค่อนข้างอ่อน โดยเฉพาะอุณหภูมิที่เกือบศูนย์ สัมประสิทธิ์อุณหภูมิในโมเดลหลายตัวแปรยังเป็นลบได้ เพราะเป็นความสัมพันธ์เมื่อคงตัวแปรอื่นไว้ ไม่ใช่การวัดแบบเดียวกับ Pearson r จึงไม่ควรอ้างจากสมการเพียงอย่างเดียวว่าอุณหภูมิสัมพันธ์กับฝุ่นแรง

![เมทริกซ์สหสัมพันธ์](figures/02_correlations.svg)

กราฟนี้แสดงทั้งความสัมพันธ์กับฝุ่นและความสัมพันธ์ระหว่างตัวแปรอากาศเอง จึงช่วยอธิบายว่าค่า r แบบจับคู่อาจแตกต่างจากสัมประสิทธิ์ที่ควบคุมตัวแปรอื่นแล้ว ไม่ควรตีความว่าสหสัมพันธ์ต่ำแปลว่าไม่มีความสัมพันธ์ทุกรูปแบบ และยังไม่ได้รายงานนัยสำคัญทางสถิติหรือช่วงความเชื่อมั่น

## สมการ Linear Regression และความหมาย

```text
PM2.5 = 172.7018 − 1.7790 × T − 1.1593 × H − 2.9386 × W
T = อุณหภูมิเฉลี่ยรายวัน (°C)
H = ความชื้นสัมพัทธ์เฉลี่ยรายวัน (%)
W = ความเร็วลมเฉลี่ยรายวันที่ 10 เมตร (m/s)
ผลลัพธ์ = µg/m³
```

- เมื่อคงความชื้นและลมไว้เท่าเดิม อุณหภูมิเพิ่ม 1°C โมเดลให้ค่าฝุ่นลดลงประมาณ 1.7790 µg/m³
- เมื่อคงอุณหภูมิและลมไว้เท่าเดิม ความชื้นเพิ่ม 1 จุดเปอร์เซ็นต์ เช่น 70% เป็น 71% โมเดลให้ค่าฝุ่นลดลงประมาณ 1.1593 µg/m³
- เมื่อคงอุณหภูมิและความชื้นไว้เท่าเดิม ลมเพิ่ม 1 m/s โมเดลให้ค่าฝุ่นลดลงประมาณ 2.9386 µg/m³
- จุดตัดแกน 172.7018 คือค่าคำนวณเมื่อ T, H, W เป็นศูนย์ทั้งหมด ซึ่งอยู่นอกช่วงข้อมูลฝึก จึงไม่ควรตีความว่าเป็นค่าฝุ่นพื้นฐานจริงของกรุงเทพฯ

ตัวอย่าง T=30, H=70, W=2 แทนค่าแล้วได้ PM2.5 ประมาณ 32.30 µg/m³ ตัวเลขในสมการปัดเศษเพื่ออ่านง่าย โค้ดใช้สัมประสิทธิ์เต็ม

![ผลสัมประสิทธิ์เมื่อเพิ่มหนึ่งส่วนเบี่ยงเบนมาตรฐาน](figures/03_coefficient_effects.svg)

ห้ามเปรียบเทียบความสำคัญจากขนาดสัมประสิทธิ์ดิบโดยตรง เพราะตัวแปรใช้คนละหน่วย กราฟนี้ใช้สัมประสิทธิ์คูณส่วนเบี่ยงเบนมาตรฐานของตัวแปรในชุดฝึก เพื่อเทียบผลของการเพิ่มแต่ละตัวแปรหนึ่ง SD โดยคงตัวอื่นไว้ เป็นการสรุปพฤติกรรมของโมเดล ไม่ใช่ causal importance และไม่มีช่วงความเชื่อมั่น

## ผลทำนายและข้อผิดพลาด

![ผลประมาณและ residual](figures/04_prediction_residuals.svg)

ด้านซ้าย จุดใกล้เส้นทแยงหมายถึงค่าประมาณใกล้ค่าจริง ด้านขวา residual นิยามเป็นค่าจริงลบค่าประมาณ: บวกคือโมเดลประมาณต่ำไป ลบคือประมาณสูงไป ในชุดทดสอบ residual เฉลี่ย {residual.mean():.2f} µg/m³ และมี {int((residual>0).sum())} วันที่ประมาณต่ำไป กับ {int((residual<0).sum())} วันที่ประมาณสูงไป ค่าเฉลี่ยใกล้ศูนย์เพียงอย่างเดียวไม่ได้แปลว่าผิดพลาดน้อย เพราะค่าบวกและลบหักล้างกันได้

ค่า residual เฉลี่ยที่ติดลบประมาณ −2.36 และจำนวนวันที่ประมาณสูงไป 70/98 วัน ชี้ว่าโมเดลมีแนวโน้มประมาณสูงเกินจริงในชุดทดสอบนี้ แม้ MAE จะดีกว่า baseline จึงควรนำเสนออคติทิศทางนี้ควบคู่กับตัวเลขความคลาดเคลื่อน ไม่ปรับแก้โมเดลด้วยข้อมูลทดสอบชุดเดิมเพื่อทำให้ผลดูดีขึ้น

![เปรียบเทียบ baseline และผลตามเวลา](figures/05_test_performance.svg)

| ตัวชี้วัดชุดทดสอบ | Linear Regression | ค่าเฉลี่ยจากชุดฝึก |
|---|---:|---:|
| MAE (µg/m³) | {report['metrics']['mae']:.2f} | {report['baseline']['mae']:.2f} |
| RMSE (µg/m³) | {report['metrics']['rmse']:.2f} | {report['baseline']['rmse']:.2f} |
| R² | {report['metrics']['r2']:.3f} | {report['baseline']['r2']:.3f} |

โมเดลลด MAE จาก baseline ได้ประมาณ {improvement:.1f}% บนวันทดสอบเดียวกัน MAE คือขนาดความผิดพลาดเฉลี่ย ไม่ใช่ช่วงรับประกันค่าทำนายรายครั้ง RMSE ให้น้ำหนักกับข้อผิดพลาดขนาดใหญ่มากกว่า ส่วน R²=0.529 หมายถึงอธิบายความแปรปรวนของ PM2.5 ในชุดทดสอบได้ประมาณ 52.9% ตามนิยาม R² ไม่ใช่ทำนายถูก 52.9% และ R² ของ baseline ติดลบได้เพราะใช้ค่าเฉลี่ยชุดฝึกแทนค่าเฉลี่ยชุดทดสอบ

## ความครบของข้อมูลและขอบเขตข้อสรุป

![จำนวนวันใช้งานได้รายเดือน](figures/06_monthly_completeness.svg)

ข้อมูลขาดไม่เท่ากันตามเดือน โดย พ.ย. 2024 เหลือ 3 วัน ธ.ค. 2024 ไม่มีวันผ่านเกณฑ์ ม.ค. 2025 เหลือ 5 วัน และ ก.ค. 2025 ไม่มีวันผ่านเกณฑ์ จึงไม่สามารถอ้างว่าชุดข้อมูลแทนทุกฤดูกาลได้ดีเท่ากัน หรือว่าผลประเมินนี้ใช้แทนผลตลอดทั้งปีได้ นอกจากนี้ 98 วันทดสอบเป็น 98 วันที่มีข้อมูล ไม่ใช่ 98 วันปฏิทินติดต่อกัน

อากาศ NASA POWER เป็นข้อมูลกริด ไม่ใช่เครื่องวัดร่วม ณ จุดเดียวกับสถานีฝุ่น ตัวแปรที่ไม่ได้รวม เช่น แหล่งกำเนิดฝุ่น ฝน หรือสภาพการกระจายตัวของอากาศ อาจสัมพันธ์กับความผิดพลาด แต่การทดลองนี้ยังไม่ได้ทดสอบอิทธิพลของตัวแปรเหล่านั้น และไม่ได้ทำ validation หลายช่วงเวลา

ข้อสรุปที่รองรับได้คือ โมเดลเชิงเส้นที่ใช้ตัวแปรอากาศสามตัวประมาณฝุ่นได้ดีกว่า baseline ค่าเฉลี่ยในการแบ่งข้อมูลครั้งนี้ ผลเป็นการประมาณย้อนหลังจากอากาศเฉลี่ยของวันเดียวกัน ไม่ใช่พยากรณ์อนาคต ไม่ควรตีความความสัมพันธ์เป็นเหตุและผลหรือรับรองการใช้กับพื้นที่อื่น

## วิธีสร้างผลซ้ำและที่มาข้อมูล

หลังเตรียมข้อมูลและฝึกโมเดลตาม README ให้รัน:

```powershell
.\\.venv\\Scripts\\python.exe scripts\\analyze_results.py
```

สคริปต์อ่าน data/processed/airpredict_daily.csv, reports/metrics.json และ reports/test_predictions.csv แล้วสร้างรูป PNG/SVG และ analysis_statistics.json โดยไม่ฝึกหรือปรับโมเดลใหม่

- [OpenAQ](https://docs.openaq.org/) — location 5545, sensor 1304222
- [NASA POWER Hourly API](https://power.larc.nasa.gov/docs/services/api/temporal/hourly/) — UTC, T2M/RH2M/WS10M
- โค้ดและขั้นตอน: scripts/check_coverage.py, prepare_dataset.py, train_model.py และ analyze_results.py ใน repository
'''
    (out / 'ANALYSIS_TH.md').write_text(narrative, encoding='utf-8')
    print(json.dumps(stats, indent=2))


if __name__ == '__main__':
    main()

