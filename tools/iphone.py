import asyncio, base64
from playwright.async_api import async_playwright
W,H=402,874
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        ctx=await b.new_context(viewport={'width':W,'height':H},device_scale_factor=3,is_mobile=True,has_touch=True,
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 26_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Mobile/15E148 Safari/604.1')
        pg=await ctx.new_page()
        await pg.route('**/fonts.googleapis.com/**',lambda r:r.abort())
        # pantalla 1: inicio con datos
        await pg.goto('file:///home/claude/work/index.html#s7-d2')
        await pg.evaluate("localStorage.clear()")
        await pg.reload()
        await pg.fill('#bw','72');await pg.fill('#bs','100');await pg.fill('#fs','85')
        # marca algo de progreso
        for sel in ['[data-toggle="7-2-1"]','[data-toggle="7-2-2"]']:
            await pg.click(sel)
        await pg.click('[data-w="5"]'); 
        for i in range(1,10): await pg.click(f'[data-toggle="5-1-{i}"]')
        await pg.click('[data-w="7"]'); await pg.click('[data-d="2"]')
        await pg.evaluate("window.scrollTo(0,0)")
        await pg.wait_for_timeout(300)
        await pg.screenshot(path='s1.png')
        # pantalla 2: detalle del día
        await pg.evaluate("document.querySelector('.day-head').scrollIntoView()")
        await pg.evaluate("window.scrollBy(0,-70)")
        await pg.wait_for_timeout(200)
        await pg.screenshot(path='s2.png')
        # pantalla 3: ejercicio olímpico con series y temporizador
        await pg.click('[data-set="7-2-5"][data-i="0"]')
        await pg.click('[data-set="7-2-5"][data-i="1"]')
        await pg.click('[data-desc="7-2-5"]')
        await pg.click('[data-timer="7-2-5"]')
        await pg.evaluate("document.querySelectorAll('.ex')[4].scrollIntoView({block:'center'})")
        await pg.wait_for_timeout(1300)
        await pg.screenshot(path='s3.png')
        await b.close()
asyncio.run(main())
