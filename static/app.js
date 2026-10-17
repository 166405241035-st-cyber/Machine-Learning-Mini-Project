const form = document.querySelector('#predict-form');
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (!form.reportValidity()) return;
  const button = document.querySelector('#predict-button');
  const error = document.querySelector('#form-error');
  const warning = document.querySelector('#warnings');
  const prediction = document.querySelector('#prediction');
  button.disabled = true;
  error.textContent = '';
  prediction.textContent = '…';
  warning.hidden = true;
  document.querySelector('#result-hint').textContent = 'กำลังคำนวณ…';
  try {
    const payload = Object.fromEntries([...new FormData(form)].map(([key, value]) => [key, Number(value)]));
    const response = await fetch('/api/predict', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'คำนวณไม่สำเร็จ');
    prediction.textContent = data.pm25 === null ? '—' : data.pm25.toFixed(2);
    document.querySelector('#result-hint').textContent = data.pm25 === null ? 'โมเดลให้ผลนอกขอบเขตทางกายภาพ' : 'ผลจากข้อมูลสภาพอากาศที่คุณกรอก';
    warning.textContent = data.warnings.join(' • ');
    warning.hidden = !data.warnings.length;
  } catch (err) {
    prediction.textContent = '—';
    error.textContent = err.message;
    document.querySelector('#result-hint').textContent = 'ยังไม่มีผลประมาณ กรุณาลองอีกครั้ง';
  } finally {
    button.disabled = false;
  }
});
