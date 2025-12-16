"""
硬币付款问题 - 动画演示
使用 matplotlib 手动控制动态规划的执行过程

特点：
- 可视化 DP 表格的填充过程
- 每一步的详细说明
- 硬币选择状态的直观展示
"""

import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

INF = float('inf')


class CoinPaymentAnimation:
    def __init__(self, coins, weights, target):
        self.coins = coins
        self.weights = weights
        self.target = target
        self.n = len(coins)
        
        # DP 数组
        self.dp = [INF] * (target + 1)
        self.dp[0] = 0
        
        # 记录每一步
        self.steps = []
        self.current_step = 0
        
        # 模拟算法执行
        self._simulate_algorithm()
        
        # 创建画布
        self.fig, (self.ax_dp, self.ax_info) = plt.subplots(2, 1, figsize=(14, 10),
                                                             gridspec_kw={'height_ratios': [2, 1]})
        self.fig.canvas.manager.set_window_title('硬币付款问题 - 动画演示')
        
        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)
    
    def _simulate_algorithm(self):
        """模拟动态规划过程，记录每一步"""
        
        # 初始状态
        self.steps.append({
            'type': 'init',
            'dp': self.dp.copy(),
            'action': '初始化 DP 表格，dp[0]=0，其他为 INF',
            'i': -1,
            'j': -1,
            'detail': {
                'what': 'dp[i] 表示凑够金额 i 所需的最小重量',
                'why': 'dp[0]=0 表示凑够0元需要0重量',
                'purpose': '为动态规划填表做准备'
            }
        })
        
        # 遍历每个金额
        for i in range(1, self.target + 1):
            best_j = -1
            old_val = self.dp[i]
            
            for j in range(self.n):
                if self.coins[j] <= i and self.dp[i - self.coins[j]] != INF:
                    new_val = self.dp[i - self.coins[j]] + self.weights[j]
                    if new_val < self.dp[i]:
                        self.dp[i] = new_val
                        best_j = j
                        
                        self.steps.append({
                            'type': 'update',
                            'dp': self.dp.copy(),
                            'action': f'更新 dp[{i}] = {new_val}（使用面值{self.coins[j]}的硬币）',
                            'i': i,
                            'j': j,
                            'detail': {
                                'what': f'dp[{i}] = dp[{i}-{self.coins[j]}] + {self.weights[j]} = {new_val}',
                                'why': f'使用面值{self.coins[j]}、重量{self.weights[j]}的硬币',
                                'purpose': f'凑够金额{i}的最小重量更新为{new_val}'
                            }
                        })
            
            if best_j == -1 and self.dp[i] == INF:
                self.steps.append({
                    'type': 'skip',
                    'dp': self.dp.copy(),
                    'action': f'无法凑够金额 {i}（保持 INF）',
                    'i': i,
                    'j': -1,
                    'detail': {
                        'what': f'没有硬币组合能凑够金额{i}',
                        'why': '所有硬币都不满足条件',
                        'purpose': 'dp[{i}]保持为INF'
                    }
                })
        
        # 最终结果
        result = self.dp[self.target]
        self.steps.append({
            'type': 'result',
            'dp': self.dp.copy(),
            'action': f'算法结束！凑够{self.target}元的最小重量 = {result if result != INF else "无法凑够"}',
            'i': self.target,
            'j': -1,
            'detail': {
                'what': f'dp[{self.target}] = {result if result != INF else "INF"}',
                'why': '这是凑够目标金额的最小重量',
                'purpose': '得到最终答案'
            }
        })
    
    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step
        
        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index
        step_data = self.steps[step_index]
        
        # 绘制 DP 数组
        self.ax_dp.clear()
        
        dp = step_data['dp']
        display_len = min(len(dp), 20)  # 最多显示20个格子
        
        colors = ['#3498db'] * display_len
        current_i = step_data.get('i', -1)
        
        for idx in range(display_len):
            if idx == current_i:
                colors[idx] = '#e74c3c'  # 红色（当前更新）
            elif dp[idx] == INF:
                colors[idx] = '#bdc3c7'  # 灰色（无法凑够）
        
        # 显示数值
        display_vals = []
        for i in range(display_len):
            if dp[i] == INF:
                display_vals.append(999)  # 用大数代替
            else:
                display_vals.append(dp[i])
        
        bars = self.ax_dp.bar(range(display_len), display_vals, color=colors,
                              edgecolor='black', linewidth=1.5)
        
        # 添加标签
        for i, (bar, val) in enumerate(zip(bars, dp[:display_len])):
            label = '∞' if val == INF else str(val)
            y_pos = bar.get_height() + 1 if val != INF else 10
            self.ax_dp.text(bar.get_x() + bar.get_width() / 2, y_pos,
                           label, ha='center', va='bottom', fontsize=10, fontweight='bold')
            # 索引标签
            self.ax_dp.text(bar.get_x() + bar.get_width() / 2, -5,
                           f'{i}元', ha='center', va='top', fontsize=9, color='gray')
        
        max_val = max(v for v in dp[:display_len] if v != INF) if any(v != INF for v in dp[:display_len]) else 10
        self.ax_dp.set_ylim(-10, max(max_val * 1.3, 20))
        self.ax_dp.set_title(f'步骤 {step_index + 1}/{len(self.steps)}: {step_data["action"]}',
                              fontsize=14, fontweight='bold')
        self.ax_dp.set_xlabel('金额', fontsize=12)
        self.ax_dp.set_ylabel('最小重量', fontsize=12)
        
        # 绘制信息区域
        self.ax_info.clear()
        self.ax_info.axis('off')
        
        # 硬币信息
        coin_info = "💰 硬币信息：\n"
        coin_info += "面值: " + " ".join(str(c) for c in self.coins) + "\n"
        coin_info += "重量: " + " ".join(str(w) for w in self.weights) + "\n"
        coin_info += f"目标: 凑够 {self.target} 元\n"
        
        self.ax_info.text(0.02, 0.95, coin_info, transform=self.ax_info.transAxes,
                         fontsize=11, verticalalignment='top', family='monospace',
                         bbox=dict(boxstyle='round', facecolor='#d5f5e3', alpha=0.9))
        
        # 详细说明
        detail = step_data.get('detail', {})
        if detail:
            info_text = "📖 当前操作：\n"
            if 'what' in detail:
                info_text += f"• 做什么：{detail['what']}\n"
            if 'why' in detail:
                info_text += f"• 为什么：{detail['why']}\n"
            if 'purpose' in detail:
                info_text += f"• 目的：{detail['purpose']}\n"
            
            self.ax_info.text(0.5, 0.95, info_text, transform=self.ax_info.transAxes,
                             fontsize=11, verticalalignment='top',
                             bbox=dict(boxstyle='round', facecolor='#fdebd0', alpha=0.9))
        
        # 操作提示
        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q 退出'
        self.ax_info.text(0.5, 0.05, controls_text, transform=self.ax_info.transAxes,
                         ha='center', fontsize=10,
                         bbox=dict(boxstyle='round', facecolor='#ecf0f1', alpha=0.8))
        
        self.fig.tight_layout()
        self.fig.canvas.draw()
    
    def _on_key_press(self, event):
        if event.key in ('right', ' ', 'enter'):
            if self.current_step < len(self.steps) - 1:
                self.current_step += 1
                self._draw_step()
        elif event.key == 'left':
            if self.current_step > 0:
                self.current_step -= 1
                self._draw_step()
        elif event.key == 'home':
            self.current_step = 0
            self._draw_step()
        elif event.key == 'end':
            self.current_step = len(self.steps) - 1
            self._draw_step()
        elif event.key in ('q', 'escape'):
            plt.close(self.fig)
    
    def show(self):
        self._draw_step(0)
        plt.show()


def main():
    print("=" * 60)
    print("    硬币付款问题 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("  1. 题目样例")
    print("  2. 简单示例: coins=[1,2,5], weights=[2,3,6], target=11")
    print("  3. 自定义输入")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    if choice == '1':
        coins = [2, 5, 7, 1, 4, 6, 9, 15, 21, 35]
        weights = [2, 5, 7, 10, 16, 22, 38][:len(coins)]  # 根据实际情况调整
        target = 43
    elif choice == '2':
        coins = [1, 2, 5]
        weights = [2, 3, 6]
        target = 11
    elif choice == '3':
        coins = list(map(int, input("请输入硬币面值（空格分隔）: ").split()))
        weights = list(map(int, input("请输入硬币重量（空格分隔）: ").split()))
        target = int(input("请输入目标金额: "))
    else:
        print("无效选择，使用示例 2")
        coins = [1, 2, 5]
        weights = [2, 3, 6]
        target = 11
    
    print("\n" + "─" * 60)
    print(f"硬币面值: {coins}")
    print(f"硬币重量: {weights}")
    print(f"目标金额: {target}")
    print("─" * 60)
    print("\n📌 操作提示：")
    print("   空格 / 右箭头 ：下一步")
    print("   左箭头       ：上一步")
    print("   Home / End   ：跳转到起点 / 终点")
    print("   Q / Esc      ：退出动画")
    print("\n⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")
    
    anim = CoinPaymentAnimation(coins, weights, target)
    anim.show()


if __name__ == '__main__':
    main()
