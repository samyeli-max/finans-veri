// Finans asistanı aracısı (Cloudflare Worker).
// Uygulama buraya konuşur; Anthropic API anahtarı yalnız burada (Cloudflare "Secret" olarak) durur, telefonda değil.
// Gerekli gizli değişkenler (Settings → Variables and Secrets → Secret):
//   ANTHROPIC_API_KEY : console.anthropic.com'dan aldığın anahtar
//   APP_KEY           : uygulamanın asistan kurulum ekranında ürettiği uzun şifre
// İsteğe bağlı: DAILY_LIMIT (varsayılan 200) — günlük istek sınırı (yalnız bu Worker örneği için, kaba sayaç)

const MODEL = 'claude-haiku-5-5';
const MAX_BODY = 200_000; // bayt
let day = '';
let count = 0;

const json = (obj, status = 200) =>
  new Response(JSON.stringify(obj), { status, headers: { 'content-type': 'application/json; charset=utf-8' } });

function same(a, b) {
  // sabit süreli karşılaştırma
  if (typeof a !== 'string' || typeof b !== 'string' || a.length !== b.length) return false;
  let r = 0;
  for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return r === 0;
}

export default {
  async fetch(request, env) {
    if (request.method === 'GET') return json({ ok: true, service: 'finans-asistan' });
    if (request.method !== 'POST') return json({ error: 'yalnız POST' }, 405);
    if (!env.APP_KEY || !env.ANTHROPIC_API_KEY) return json({ error: 'Worker ayarları eksik: APP_KEY ve ANTHROPIC_API_KEY gizli değişkenlerini ekle' }, 500);
    if (!same(request.headers.get('x-app-key') || '', env.APP_KEY)) return json({ error: 'yetkisiz' }, 401);

    const today = new Date().toISOString().slice(0, 10);
    if (today !== day) { day = today; count = 0; }
    if (++count > Number(env.DAILY_LIMIT || 200)) return json({ error: 'günlük sınır doldu' }, 429);

    const text = await request.text();
    if (text.length > MAX_BODY) return json({ error: 'istek çok büyük' }, 413);
    let body;
    try { body = JSON.parse(text); } catch { return json({ error: 'geçersiz JSON' }, 400); }
    if (!Array.isArray(body.messages)) return json({ error: 'messages yok' }, 400);

    // Model ve üst sınırlar burada sabit: uygulama başka model ya da çok uzun cevap isteyemez
    const payload = {
      model: MODEL,
      max_tokens: Math.min(Number(body.max_tokens) || 1024, 2048),
      messages: body.messages,
      ...(typeof body.system === 'string' ? { system: body.system } : {}),
      ...(Array.isArray(body.tools) ? { tools: body.tools } : {}),
    };
    const r = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return new Response(await r.text(), { status: r.status, headers: { 'content-type': 'application/json; charset=utf-8' } });
  },
};
