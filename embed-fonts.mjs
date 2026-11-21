// Скачивает шрифты Google Fonts в www/fonts, чтобы игра выглядела так же без интернета.
// Если скачать не удалось, сборка не падает: игра просто использует запасные шрифты.
import { mkdir, writeFile, readFile } from 'node:fs/promises';
const CSS = 'https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700&family=Manrope:wght@400;600;800&family=JetBrains+Mono:wght@500;700&display=swap';
const UA = 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36';
try {
  let css = await (await fetch(CSS, { headers: { 'User-Agent': UA } })).text();
  await mkdir('www/fonts', { recursive: true });
  const urls = [...new Set([...css.matchAll(/url\((https:[^)]+)\)/g)].map(m => m[1]))];
  let i = 0;
  for (const u of urls) {
    const name = `f${i++}.woff2`;
    const buf = Buffer.from(await (await fetch(u)).arrayBuffer());
    await writeFile(`www/fonts/${name}`, buf);
    css = css.split(u).join(name);
  }
  await writeFile('www/fonts/fonts.css', css);
  let html = await readFile('www/index.html', 'utf8');
  html = html.replace(/<link rel="stylesheet" href="https:\/\/fonts\.googleapis\.com[^>]*>/, '<link rel="stylesheet" href="fonts/fonts.css">');
  await writeFile('www/index.html', html);
  console.log(`Шрифты встроены: ${urls.length} файлов`);
} catch (e) {
  console.warn('Не удалось встроить шрифты, используются запасные:', e.message);
}
