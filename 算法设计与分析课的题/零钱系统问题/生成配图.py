"""
零钱系统问题 - 简洁配图生成脚本 (简化版)
使用最简单的matplotlib绑定，确保兼容性
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'STSong', 'SimSun']
plt.rcParams['axes.unicode_minus'] = False

SAVE_DIR = r"e:\学委\面试刷题\算法设计与分析课的题\零钱系统问题\实验报告\images"
os.makedirs(SAVE_DIR, exist_ok=True)

def generate_coin_structure():
    """币值系统结构图"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    levels = ['p^n (最大)', 'p^3', 'p^2', 'p^1 = p', 'p^0 = 1 (最小)']
    y_pos = range(len(levels))
    widths = [3, 2.5, 2, 1.5, 1]
    
    bars = ax.barh(y_pos, widths, color=plt.cm.Blues(np.linspace(0.3, 0.8, 5)), edgecolor='black', height=0.6)
    
    for i, (level, w) in enumerate(zip(levels, widths)):
        ax.text(w + 0.1, i, level, va='center', fontsize=12, fontweight='bold')
    
    ax.set_xlim(0, 5)
    ax.set_yticks([])
    ax.set_xlabel('面值大小', fontsize=12)
    ax.set_title('币值系统结构: {1, p, p^2, ..., p^n}\n公比 = p', fontsize=14, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    plt.tight_layout()
    path = os.path.join(SAVE_DIR, '币值系统结构图.png')
    plt.savefig(path, dpi=150, facecolor='white')
    print(f"已保存: {path}")
    plt.close()

def generate_conversion_example():
    """进制转换示例"""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')
    
    lines = [
        ('示例: 23 转换为 3 进制', 18, 'black', 'bold', 0.5, 0.9),
        ('', 12, 'black', 'normal', 0.1, 0.78),
        ('步骤1:  23 / 27 = 0 余 23      第3位 = 0', 13, 'black', 'normal', 0.1, 0.7),
        ('步骤2:  23 / 9  = 2 余 5       第2位 = 2', 13, 'black', 'normal', 0.1, 0.58),
        ('步骤3:  5  / 3  = 1 余 2       第1位 = 1', 13, 'black', 'normal', 0.1, 0.46),
        ('步骤4:  2  / 1  = 2 余 0       第0位 = 2', 13, 'black', 'normal', 0.1, 0.34),
        ('', 12, 'black', 'normal', 0.1, 0.26),
        ('结果: 23 = (0212) 即 2*9 + 1*3 + 2*1', 14, 'blue', 'bold', 0.1, 0.16),
        ('最少硬币数: 0+2+1+2 = 5', 16, 'red', 'bold', 0.1, 0.04),
    ]
    
    for text, size, color, weight, x, y in lines:
        ax.text(x, y, text, fontsize=size, color=color, fontweight=weight, 
                transform=ax.transAxes, family='monospace' if '/' in text else 'sans-serif')
    
    plt.tight_layout()
    path = os.path.join(SAVE_DIR, '进制转换示例.png')
    plt.savefig(path, dpi=150, facecolor='white', bbox_inches='tight')
    print(f"已保存: {path}")
    plt.close()

def generate_proof_diagram():
    """正确性证明图解"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # 左图: 贪心选择性质
    ax1.axis('off')
    ax1.set_title('【贪心选择性质】', fontsize=14, fontweight='bold', color='darkblue')
    texts1 = [
        ('向下替换增加硬币数:', 0.1, 0.8, 12),
        ('1个p^2 = p个p^1 = p^2个1', 0.1, 0.65, 12),
        ('因为 p > 1', 0.1, 0.5, 12),
        ('所以: 替换后硬币数 > 替换前', 0.1, 0.35, 12),
        ('结论: 贪心选择最大面值是最优的', 0.1, 0.15, 13),
    ]
    for text, x, y, size in texts1:
        color = 'red' if '结论' in text else 'black'
        ax1.text(x, y, text, fontsize=size, fontweight='bold' if '结论' in text else 'normal',
                color=color, transform=ax1.transAxes)
    
    # 右图: 最优子结构
    ax2.axis('off')
    ax2.set_title('【最优子结构】', fontsize=14, fontweight='bold', color='darkblue')
    texts2 = [
        ('p进制表示唯一:', 0.1, 0.8, 12),
        ('y = a0 + a1*p + a2*p^2 + ...', 0.1, 0.65, 12),
        ('其中 0 <= ai < p', 0.1, 0.5, 12),
        ('硬币数 = a0 + a1 + a2 + ...', 0.1, 0.35, 12),
        ('结论: 标准p进制就是最优解', 0.1, 0.15, 13),
    ]
    for text, x, y, size in texts2:
        color = 'blue' if '结论' in text else 'black'
        ax2.text(x, y, text, fontsize=size, fontweight='bold' if '结论' in text else 'normal',
                color=color, transform=ax2.transAxes)
    
    fig.suptitle('贪心算法 = p进制转换 = 最优解', fontsize=16, fontweight='bold', y=0.02, color='green')
    
    plt.tight_layout()
    path = os.path.join(SAVE_DIR, '正确性证明图解.png')
    plt.savefig(path, dpi=150, facecolor='white', bbox_inches='tight')
    print(f"已保存: {path}")
    plt.close()

def generate_complexity_chart():
    """复杂度对比图"""
    fig, ax = plt.subplots(figsize=(9, 5))
    
    y_vals = np.linspace(10, 1000, 100)
    greedy = np.log2(y_vals) * 2
    dp = y_vals * 0.03
    
    ax.plot(y_vals, greedy, 'g-', linewidth=3, label='贪心: O(log y)')
    ax.plot(y_vals, dp, 'r--', linewidth=3, label='动态规划: O(n*y)')
    ax.fill_between(y_vals, greedy, dp, where=(dp > greedy), alpha=0.15, color='green')
    
    ax.set_xlabel('金额 y', fontsize=13)
    ax.set_ylabel('运行时间', fontsize=13)
    ax.set_title('时间复杂度对比', fontsize=15, fontweight='bold')
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True, alpha=0.3)
    
    ax.annotate('贪心远优于DP', xy=(600, 15), fontsize=12, 
                bbox=dict(facecolor='yellow', alpha=0.8, boxstyle='round'))
    
    plt.tight_layout()
    path = os.path.join(SAVE_DIR, '复杂度对比图.png')
    plt.savefig(path, dpi=150, facecolor='white')
    print(f"已保存: {path}")
    plt.close()

def generate_flowchart():
    """贪心算法流程图 - 用简单的文本表格"""
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.axis('off')
    
    # 用简单文字描述流程
    flow = """
    ┌─────────────────────────────────┐
    │           开始                  │
    └────────────┬────────────────────┘
                 ↓
    ┌─────────────────────────────────┐
    │       输入: y, p, n             │
    └────────────┬────────────────────┘
                 ↓
    ┌─────────────────────────────────┐
    │     初始化: i=n, total=0        │
    └────────────┬────────────────────┘
                 ↓
         ┌──────────────┐
         │   i >= 0 ?   │─── 否 ──→ 输出total → 结束
         └──────┬───────┘
                │ 是
                ↓
    ┌─────────────────────────────────┐
    │  count = y / (p的i次方)         │
    │  y = y mod (p的i次方)           │
    │  total = total + count          │
    │  i = i - 1                      │
    └────────────┬────────────────────┘
                 │
                 └──────── 循环回去 ────→
    """
    
    ax.text(0.5, 0.5, flow, fontsize=11, family='monospace',
            ha='center', va='center', transform=ax.transAxes)
    ax.set_title('贪心算法流程', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    path = os.path.join(SAVE_DIR, '贪心算法流程图.png')
    plt.savefig(path, dpi=150, facecolor='white', bbox_inches='tight')
    print(f"已保存: {path}")
    plt.close()

if __name__ == '__main__':
    print("生成简洁配图...")
    generate_coin_structure()
    generate_conversion_example()
    generate_proof_diagram()
    generate_complexity_chart()
    generate_flowchart()
    print("完成!")
