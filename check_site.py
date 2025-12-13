import requests
import time
from datetime import datetime

def check_blog_status():
    blog_url = "https://mieor.github.io"
    
    # 添加随机参数避免浏览器缓存影响，强制获取最新版本
    timestamp = int(time.time())
    test_urls = [
        f"{blog_url}?v={timestamp}",  # 带版本号的URL，用于检查CDN缓存
        f"{blog_url}/index.html?t={timestamp}",  # 检查首页
    ]
    
    print("🔍 开始检查博客状态...")
    print("=" * 60)
    
    # 首先检查GitHub Actions构建状态（这比检查网页更直接）
    print("📊 正在检查GitHub Actions最新构建状态...")
    # 注意：这里无法通过API直接获取私有仓库的详细状态，但我们可以通过一个逻辑推断
    print("💡 提示：请手动访问 https://github.com/mieor/mieor.github.io/actions 确认最近一次工作流是否成功（绿色勾号✅）。")
    
    print("\n🌐 开始检查网站可访问性...")
    all_accessible = True
    for url in test_urls:
        try:
            start_time = time.time()
            response = requests.get(url, timeout=15)  # 设置超时
            response_time = round((time.time() - start_time) * 1000, 2)  # 计算响应时间（毫秒）
            
            status_icon = "✅" if response.status_code == 200 else "❌"
            print(f"{status_icon} 页面: {url}")
            print(f"   状态码: {response.status_code}")
            print(f"   响应时间: {response_time}ms")
            
            # 检查页面内容长度，极短的内容可能意味着构建失败
            content_length = len(response.text)
            print(f"   内容长度: {content_length} 字符")
            
            if response.status_code != 200:
                all_accessible = False
                print("   🚨 网站返回异常状态码，可能部署失败或配置有误。")
            elif content_length < 100:  # 如果首页内容非常少，可能构建出了问题
                print("   ⚠️  首页内容过短，可能是Hugo构建未生成完整内容。")
                all_accessible = False
            else:
                # 简单检查是否包含Hugo或常见静态站点关键词
                if any(keyword in response.text.lower() for keyword in ['hugo', '</html>', '<body>']):
                    print("   📄 页面包含常见HTML元素，构建可能正常。")
                else:
                    print("   🤔 页面内容似乎不标准，建议手动访问确认。")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 无法访问: {url}")
            print(f"   错误详情: {e}")
            all_accessible = False
        print()  # 空行分隔每个测试结果
    
    # 总结与建议
    print("=" * 60)
    print("📋 检查结果总结:")
    if all_accessible:
        print("🎉 您的博客可以正常访问！")
        print("💡 如果您在浏览器中仍看不到更新，这通常是缓存问题：")
        print("   1. 尝试强制刷新浏览器 (Ctrl+F5 或 Cmd+Shift+R)")
        print("   2. 使用无痕/隐私模式访问")
        print("   3. 等待一段时间（最多1小时）让GitHub全球CDN刷新")
    else:
        print("😥 您的博客访问存在问题。")
        print("🔧 建议排查步骤：")
        print("   1. 确认GitHub Actions工作流最新一次运行是否成功")
        print("   2. 检查hugo.toml等配置文件是否有语法错误")
        print("   3. 查看Actions构建日志中的错误信息")
    
    print(f"\n⏰ 检查完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    check_blog_status()