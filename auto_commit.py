import subprocess
import os
from datetime import datetime
import sys

def auto_commit():
    """自动化提交和推送博客更新"""
    
    # 获取当前时间
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    date_only = now.strftime("%Y-%m-%d")
    
    # 提交信息选项
    commit_messages = {
        "1": f"更新博客内容 - {timestamp}",
        "2": f"发布新文章 - {date_only}",
        "3": f"日常更新 - {timestamp}",
        "4": "修复样式和配置",
        "5": "自定义提交信息"
    }
    
    print("🚀 Hugo博客自动化提交工具")
    print("=" * 40)
    print("请选择提交类型：")
    for key, message in commit_messages.items():
        print(f"{key}. {message}")
    
    choice = input("\n请输入选项 (1-5): ").strip()
    
    if choice == "5":
        custom_msg = input("请输入自定义提交信息: ").strip()
        if custom_msg:
            commit_message = custom_msg
        else:
            commit_message = f"博客更新 - {timestamp}"
    else:
        commit_message = commit_messages.get(choice, f"博客更新 - {timestamp}")
    
    try:
        print(f"\n📦 开始提交: {commit_message}")
        
        # 检查是否有更改
        status_result = subprocess.run(["git", "status", "--porcelain"], 
                                      capture_output=True, text=True)
        
        if not status_result.stdout.strip():
            print("❌ 没有检测到文件更改，跳过提交")
            return
        
        # 添加所有更改
        print("1. 添加文件到暂存区...")
        subprocess.run(["git", "add", "."], check=True)
        
        # 提交更改
        print("2. 提交更改...")
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # 推送到GitHub
        print("3. 推送到GitHub...")
        push_result = subprocess.run(["git", "push", "origin", "main"], 
                                   capture_output=True, text=True)
        
        if push_result.returncode == 0:
            print("✅ 提交成功！")
            print("🌐 GitHub Actions将自动部署你的博客")
            print(f"📊 查看部署状态: https://github.com/mieor/mieor.github.io/actions")
        else:
            print("❌ 推送失败，错误信息:")
            print(push_result.stderr)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 执行命令时出错: {e}")
    except Exception as e:
        print(f"❌ 发生未知错误: {e}")

if __name__ == "__main__":
    auto_commit()