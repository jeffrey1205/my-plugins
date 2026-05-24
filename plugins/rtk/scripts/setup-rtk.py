#!/usr/bin/env python3
"""RTK (Rust Token Killer) 安装脚本"""

import argparse
import subprocess
import sys

INSTALL_SCRIPT_URL = "https://raw.githubusercontent.com/rtk-ai/rtk/master/install.sh"
RELEASES_URL = "https://github.com/rtk-ai/rtk/releases"
TIMEOUT_SECONDS = 90


def get_rtk_version():
    """获取 rtk 版本"""
    try:
        result = subprocess.run(
            ["rtk", "--version"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split()
            if len(parts) >= 2:
                return parts[-1]
    except (subprocess.TimeoutExpired, OSError):
        pass
    return None


def install_rtk():
    """通过 curl 安装脚本安装 rtk"""
    print("正在下载安装 RTK...")
    try:
        result = subprocess.run(
            ["curl", "-fsSL", INSTALL_SCRIPT_URL],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
        if result.returncode != 0:
            print(f"✗ 下载失败: {result.stderr}")
            print(f"\n请手动下载安装: {RELEASES_URL}")
            return False

        # 执行安装脚本
        install_result = subprocess.run(
            ["sh"],
            input=result.stdout,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
        if install_result.returncode != 0:
            print(f"✗ 安装失败: {install_result.stderr}")
            print(f"\n请手动下载安装: {RELEASES_URL}")
            return False

        return True
    except subprocess.TimeoutExpired:
        print(f"✗ 下载超时（{TIMEOUT_SECONDS}s）")
        print(f"\n请手动下载安装: {RELEASES_URL}")
        return False
    except Exception as e:
        print(f"✗ 安装出错: {e}")
        print(f"\n请手动下载安装: {RELEASES_URL}")
        return False


def main():
    parser = argparse.ArgumentParser(description="安装 RTK")
    parser.add_argument("--force", action="store_true", help="强制重新安装")
    args = parser.parse_args()

    # 检查是否已安装
    version = get_rtk_version()
    if version and not args.force:
        print(f"RTK 已安装: 版本 {version}")
        print("如需重新安装，请使用 --force 参数")
        return

    # 安装
    if not install_rtk():
        sys.exit(1)

    # 验证安装
    version = get_rtk_version()
    if not version:
        print("✗ 安装验证失败: rtk 未在 PATH 中找到或无法获取版本")
        print(f"\n请手动下载安装: {RELEASES_URL}")
        sys.exit(1)

    print(f"\n✓ RTK {version} 安装成功")

    print("✓ Hook 已通过插件 hooks/hooks.json 自动配置")
    print("\n使用方式：命令前加 'rtk'")
    print("  rtk git status    # 紧凑的 git 状态")
    print("  rtk cargo test    # 只显示测试失败")
    print("  rtk pnpm list     # 紧凑的依赖树")


if __name__ == "__main__":
    main()
