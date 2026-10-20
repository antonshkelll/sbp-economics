// Калькулятор стоимости платежа и дашборд. Формулы совпадают с analysis/payment_cost.py.
const C = { navy: '#083542', teal: '#246568', petrol: '#016A80', cyan: '#0098AE', bright: '#19C3D6',
  sky: '#5B9BD5', red: '#D70E16', coral: '#FF5A5F', amber: '#F4A62A', grey: '#BFBFBF' };
const rub = v => v.toLocaleString('ru-RU', { maximumFractionDigits: 2, minimumFractionDigits: v < 100 ? 2 : 0 }) + ' ₽';
const $ = id => document.getElementById(id);
let D, calcChart;

Chart.defaults.font.family = '"Segoe UI", system-ui, sans-serif';
Chart.defaults.color = getComputedStyle(document.documentElement).getPropertyValue('--muted').trim() || '#5E7079';
Chart.defaults.plugins.legend.position = 'bottom';

function fee(check, rate, cap, vat) {
  let f = check * rate / 100;
  if (cap) f = Math.min(f, cap);
  return f * (1 + vat / 100);
}

function recalc() {
  const T = D.tariffs;
  const turnover = +$('turnover').value || 0, check = +$('check').value || 0;
  const cardRate = +$('cardRate').value, sbpRate = +$('sbpCat').value;
  const vat = $('tax').value === 'usn' ? T.vat_acquiring : 0;
  const drRate = $('drYear').value === '2026' ? T.dr_2026 : T.dr_2027;
  const shift = +$('shift').value;
  $('shiftOut').textContent = shift + '%';

  const card = fee(check, cardRate, null, vat), sbp = fee(check, sbpRate, T.sbp_cap_rub, 0), dr = fee(check, drRate, T.dr_cap_rub, 0);
  $('cCard').textContent = rub(card); $('cSbp').textContent = rub(sbp); $('cDr').textContent = rub(dr);
  const pct = v => check ? (v / check * 100).toFixed(2).replace('.', ',') + '% от чека' : '';
  $('pCard').textContent = pct(card); $('pSbp').textContent = pct(sbp); $('pDr').textContent = pct(dr);

  const moved = turnover * shift / 100, cardEff = cardRate * (1 + vat / 100);
  $('sSbp').textContent = rub(Math.round(moved * (cardEff - sbpRate) / 100 * 12));
  $('sDr').textContent = rub(Math.round(moved * (cardEff - drRate) / 100 * 12));

  const data = [card, sbp, dr].map(v => +v.toFixed(2));
  if (calcChart) { calcChart.data.datasets[0].data = data; calcChart.update(); return; }
  calcChart = new Chart($('chCalc'), {
    type: 'bar',
    data: { labels: ['Карта', 'СБП', 'Цифровой рубль'], datasets: [{ label: '₽ с одного чека', data, backgroundColor: [C.red, C.cyan, C.teal], borderRadius: 8 }] },
    options: { indexAxis: 'y', plugins: { legend: { display: false } }, scales: { x: { grid: { display: false } }, y: { grid: { display: false } } } }
  });
}

const bar = (id, labels, data, colors, opts = {}) => new Chart($(id), {
  type: 'bar',
  data: { labels, datasets: Array.isArray(data[0]) ? data.map((d, i) => ({ label: opts.names[i], data: d, backgroundColor: colors[i], borderRadius: 6 }))
    : [{ data, backgroundColor: colors, borderRadius: 6 }] },
  options: { indexAxis: opts.horizontal ? 'y' : 'x', plugins: { legend: { display: !!opts.names } },
    scales: { x: { grid: { display: false } }, y: { grid: { display: false } } } }
});

function dashboard() {
  bar('chAnnual', D.annual.map(a => a.year), D.annual.map(a => a.vol), [C.sky, C.cyan, C.petrol]);
  bar('chDaily', D.daily.map(a => a.period), D.daily.map(a => a.value), C.cyan);
  new Chart($('chMethods'), { type: 'doughnut',
    data: { labels: D.methods.map(m => m.name), datasets: [{ data: D.methods.map(m => m.share), backgroundColor: [C.petrol, C.cyan, C.sky, C.red, C.grey], borderWidth: 0 }] },
    options: { cutout: '58%', aspectRatio: 1.6 } });
  bar('chMerchants', D.merchants.map(m => m.q), [D.merchants.map(m => m.all), D.merchants.map(m => m.sme)], [C.petrol, C.bright], { names: ['Все ТСП', 'из них МСП'] });
  bar('chCheck', D.avgCheck.map(m => m.name), D.avgCheck.map(m => m.value), D.avgCheck.map(m => m.name === 'QR-код' ? C.red : C.sky), { horizontal: true });
  bar('chIntl', D.international.map(i => `${i.system} · ${i.country}`), D.international.map(i => i.perCapita), [C.red, C.sky, C.petrol]);
  bar('chDr', [...D.digitalRuble.map(d => d.date), 'Ожидание ЦБ к концу года'], [...D.digitalRuble.map(d => d.wallets), D.drExpectation], [C.cyan, C.petrol, C.grey]);
  bar('chRegions', D.regions.map(r => r.name), D.regions.map(r => r.value), D.regions.map(r => r.name === 'СКФО' ? C.red : r.name === 'Россия' ? C.amber : C.petrol), { horizontal: true });

  const names = { primary: 'первичный', secondary: 'вторичный', disputed: 'спорно', author: 'автор' };
  $('sources').innerHTML = D.sources.map(s =>
    `<li><span class="st ${s.status}">${names[s.status]}</span><a href="${s.url}" target="_blank" rel="noopener">${s.title}</a></li>`).join('');
}

fetch('data/sbp.json').then(r => r.json()).then(json => {
  D = json;
  $('checked').textContent = D.checked.split('-').reverse().join('.');
  document.querySelectorAll('#form input, #form select').forEach(el => el.addEventListener('input', recalc));
  recalc();
  dashboard();
}).catch(err => {
  document.querySelector('main').insertAdjacentHTML('afterbegin',
    '<p class="card">Не удалось загрузить данные. Откройте сайт через веб-сервер (GitHub Pages или <code>python -m http.server</code>).</p>');
  console.error(err);
});
