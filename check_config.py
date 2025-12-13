import toml
import os

def check_config():
    config_files = ["hugo.toml", "config/_default/languages.zh-cn.toml"]
    
    for file in config_files:
        if os.path.exists(file):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    toml.load(f)
                print(f"✅ {file} 语法正确")
            except Exception as e:
                print(f"❌ {file} 语法错误: {e}")
        else:
            print(f"⚠️  {file} 不存在")

check_config()