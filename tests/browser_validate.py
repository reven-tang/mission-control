#!/usr/bin/env python3
"""浏览器验证脚本 — Playwright headless 检查 console error"""

import sys
import json
from playwright.sync_api import sync_playwright

def validate_streamlit(url="http://127.0.0.1:8501"):
    """验证 Streamlit 前端 0 console error"""
    console_errors = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 收集 console 消息
        page.on("console", lambda msg: console_errors.append({
            "type": msg.type,
            "text": msg.text[:200]
        }) if msg.type == "error" else None)
        
        print(f"Navigating to {url}...")
        page.goto(url, wait_until="networkidle", timeout=15000)
        
        # 等待 Streamlit 渲染
        page.wait_for_timeout(3000)
        
        # 点击"系统健康"菜单项
        try:
            sidebar = page.locator("[data-testid='stSidebar']")
            health_nav = sidebar.locator("text=系统健康")
            if health_nav.count() > 0:
                print("Found 系统健康 nav, clicking...")
                health_nav.first.click()
                page.wait_for_timeout(2000)
            else:
                print("系统健康 nav not found in sidebar, checking radio options...")
                radio_options = page.locator("[data-testid='stRadio'] label")
                for i in range(radio_options.count()):
                    text = radio_options.nth(i).text_content()
                    if "系统健康" in text:
                        print(f"Clicking radio option: {text}")
                        radio_options.nth(i).click()
                        page.wait_for_timeout(2000)
                        break
        except Exception as e:
            print(f"Navigation attempt: {e}")
        
        # 截图保存
        page.screenshot(path="/tmp/mc-health-dashboard.png")
        print(f"Screenshot saved to /tmp/mc-health-dashboard.png")
        
        # 检查结果
        errors = [e for e in console_errors if e["type"] == "error"]
        
        browser.close()
    
    # 报告
    print(f"\n{'='*40}")
    print(f"浏览器验证结果")
    print(f"{'='*40}")
    print(f"Console errors: {len(errors)}")
    
    if errors:
        print("❌ 发现 console errors:")
        for e in errors:
            print(f"  - {e['text'][:100]}")
        return False
    else:
        print("✅ 0 console error — 门禁通过!")
        return True

if __name__ == "__main__":
    success = validate_streamlit()
    sys.exit(0 if success else 1)