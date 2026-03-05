"""
零钱系统问题 - 贪心算法可视化
演示 p 进制转换过程

注意：使用 SimHei 字体确保中文显示正确
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def greedy_coin_change(y, p, n):
    """
    贪心算法求解零钱问题
    返回每种面值使用的硬币数
    """
    coins = []
    remaining = y
    steps = []
    
    for i in range(n, -1, -1):
        denomination = p ** i
        count = remaining // denomination
        new_remaining = remaining % denomination
        
        steps.append({
            'i': i,
            'denomination': denomination,
            'count': count,
            'remaining_before': remaining,
            'remaining_after': new_remaining
        })
        
        coins.append(count)
        remaining = new_remaining
    
    return coins, steps

def visualize_conversion(y, p, n, save_path=None):
    """
    可视化 p 进制转换过程
    """
    coins, steps = greedy_coin_change(y, p, n)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # 左图：转换步骤
    ax1 = axes[0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, len(steps) + 1)
    ax1.set_title(f'{y} 的 {p} 进制转换过程', fontsize=14, fontweight='bold')
    ax1.axis('off')
    
    y_pos = len(steps)
    for step in steps:
        text = f"步骤 {n - step['i'] + 1}: {step['remaining_before']} ÷ {step['denomination']} = {step['count']} ... {step['remaining_after']}"
        ax1.text(0.5, y_pos - 0.5, text, fontsize=11, 
                 transform=ax1.transData, verticalalignment='center')
        y_pos -= 1
    
    # 右图：硬币堆叠
    ax2 = axes[1]
    ax2.set_title(f'硬币组合 (共 {sum(coins)} 枚)', fontsize=14, fontweight='bold')
    ax2.set_xlim(0, n + 2)
    ax2.set_ylim(0, max(coins) + 2 if max(coins) > 0 else 3)
    
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, n + 1))
    
    for i, count in enumerate(coins):
        denomination = p ** (n - i)
        for j in range(count):
            circle = patches.Circle((i + 0.5, j + 0.5), 0.4, 
                                    facecolor=colors[i], edgecolor='black', linewidth=1.5)
            ax2.add_patch(circle)
        
        ax2.text(i + 0.5, -0.5, f'{p}^{n-i}={denomination}', 
                 ha='center', fontsize=9)
        ax2.text(i + 0.5, -1.2, f'×{count}', ha='center', fontsize=10, fontweight='bold')
    
    ax2.set_ylim(-2, max(coins) + 1 if max(coins) > 0 else 3)
    ax2.set_aspect('equal')
    ax2.axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight', 
                    facecolor='white', edgecolor='none')
        print(f"图像已保存: {save_path}")
    
    plt.show()
    return fig

def create_complexity_comparison(save_path=None):
    """
    创建复杂度对比图
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    y_values = np.linspace(1, 1000, 100)
    
    # 贪心算法复杂度 O(log y)
    greedy_time = np.log2(y_values)
    
    # 动态规划复杂度 O(n * y)，假设 n=10
    n_coins = 10
    dp_time = n_coins * y_values / 100  # 缩放以便显示
    
    ax.plot(y_values, greedy_time, 'g-', linewidth=2.5, 
            label=r'贪心算法: $O(\log_p y)$')
    ax.plot(y_values, dp_time, 'r--', linewidth=2.5, 
            label=r'动态规划: $O(n \times y)$')
    
    ax.set_xlabel('金额 y', fontsize=12)
    ax.set_ylabel('时间复杂度（相对值）', fontsize=12)
    ax.set_title('算法时间复杂度对比', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=11)
    ax.grid(True, alpha=0.3)
    
    # 添加注释
    ax.annotate('贪心远优于DP！', xy=(800, 10), fontsize=12,
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        print(f"图像已保存: {save_path}")
    
    plt.show()
    return fig

def create_denomination_pyramid(p, n, save_path=None):
    """
    创建币值系统金字塔图
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    ax.set_xlim(0, 10)
    ax.set_ylim(0, n + 3)
    ax.set_title(f'币值系统结构图 (p={p})', fontsize=14, fontweight='bold')
    
    colors = plt.cm.YlOrRd(np.linspace(0.3, 0.9, n + 1))
    
    for i in range(n, -1, -1):
        y_pos = n - i + 1
        width = 2 + i * 0.8
        left = 5 - width / 2
        
        rect = patches.FancyBboxPatch((left, y_pos - 0.3), width, 0.6,
                                       boxstyle="round,pad=0.03",
                                       facecolor=colors[n-i], edgecolor='black',
                                       linewidth=2)
        ax.add_patch(rect)
        
        denomination = p ** i
        ax.text(5, y_pos, f'{p}^{i} = {denomination}', ha='center', va='center',
                fontsize=12, fontweight='bold')
    
    # 添加标签
    ax.annotate('最大面值', xy=(7, 1), xytext=(8.5, 1),
                fontsize=10, arrowprops=dict(arrowstyle='->', color='gray'))
    ax.annotate('最小面值', xy=(7, n + 1), xytext=(8.5, n + 1),
                fontsize=10, arrowprops=dict(arrowstyle='->', color='gray'))
    
    ax.text(5, 0.2, f'公比 = {p}', ha='center', fontsize=11, style='italic')
    
    ax.axis('off')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        print(f"图像已保存: {save_path}")
    
    plt.show()
    return fig

def main():
    """主函数：演示零钱系统问题"""
    print("=" * 50)
    print("零钱系统问题 - 贪心算法演示")
    print("=" * 50)
    
    # 示例参数
    p = 3
    n = 3
    y = 23
    
    print(f"\n参数: p={p}, n={n}, y={y}")
    print(f"币值系统: {{1, {p}, {p**2}, {p**3}}}")
    
    # 计算结果
    coins, steps = greedy_coin_change(y, p, n)
    total = sum(coins)
    
    print(f"\n最少硬币数: {total}")
    print(f"\n详细步骤:")
    for step in steps:
        print(f"  {step['remaining_before']} ÷ {step['denomination']} = "
              f"{step['count']} ... {step['remaining_after']}")
    
    # p 进制表示
    p_repr = ''.join(str(c) for c in coins)
    print(f"\n{p} 进制表示: ({p_repr})_{p}")
    print(f"各位数字之和: {' + '.join(str(c) for c in coins)} = {total}")
    
    # 可视化
    print("\n正在生成可视化图像...")
    
    # 保存图像到实验报告目录
    import os
    save_dir = r"e:\学委\面试刷题\算法设计与分析课的题\零钱系统问题\实验报告\images"
    os.makedirs(save_dir, exist_ok=True)
    
    visualize_conversion(y, p, n, os.path.join(save_dir, "conversion_demo.png"))
    create_complexity_comparison(os.path.join(save_dir, "complexity_comparison.png"))
    create_denomination_pyramid(p, n, os.path.join(save_dir, "denomination_pyramid.png"))
    
    print("\n所有图像已生成完毕！")

if __name__ == "__main__":
    main()
