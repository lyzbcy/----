"""
0-1背包问题的推广（二维费用背包） - 动画演示
使用 matplotlib 手动控制动态规划的执行过程

特点：
- 可视化 DP 表格的填充过程
- 每一步的详细说明
- 物品选择状态的直观展示
"""

import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class KnapsackAnimation:
    def __init__(self, n, W, V, weights, volumes, values):
        self.n = n
        self.W = W
        self.V = V
        self.weights = weights
        self.volumes = volumes
        self.values = values
        
        # DP 表格
        self.dp = np.zeros((W + 1, V + 1), dtype=int)
        
        # 记录每一步
        self.steps = []
        self.current_step = 0
        
        # 模拟算法执行
        self._simulate_algorithm()
        
        # 创建画布
        self.fig, (self.ax_table, self.ax_info) = plt.subplots(1, 2, figsize=(16, 8))
        self.fig.canvas.manager.set_window_title('0-1背包问题的推广 - 动画演示')
        
        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)
    
    def _simulate_algorithm(self):
        """模拟动态规划过程，记录每一步"""
        
        # 初始状态
        self.steps.append({
            'type': 'init',
            'dp': self.dp.copy(),
            'action': '初始化 DP 表格，所有值为 0',
            'item': -1,
            'detail': {
                'what': '创建二维 DP 表格 dp[W+1][V+1]',
                'why': 'dp[j][k] 表示重量不超过j，体积不超过k时的最大价值',
                'purpose': '为动态规划填表做准备'
            }
        })
        
        # 遍历每个物品
        for i in range(self.n):
            w, c, v = self.weights[i], self.volumes[i], self.values[i]
            
            self.steps.append({
                'type': 'item_start',
                'dp': self.dp.copy(),
                'action': f'开始处理物品 {i+1}: 重量={w}, 体积={c}, 价值={v}',
                'item': i,
                'detail': {
                    'what': f'考虑第 {i+1} 个物品',
                    'why': '动态规划需要逐个考虑每个物品',
                    'purpose': '决定是否选择该物品'
                }
            })
            
            # 逆序遍历
            for j in range(self.W, w - 1, -1):
                for k in range(self.V, c - 1, -1):
                    old_val = self.dp[j][k]
                    new_val = self.dp[j - w][k - c] + v
                    
                    if new_val > old_val:
                        self.dp[j][k] = new_val
                        self.steps.append({
                            'type': 'update',
                            'dp': self.dp.copy(),
                            'action': f'更新 dp[{j}][{k}] = {new_val} (选择物品 {i+1})',
                            'item': i,
                            'cell': (j, k),
                            'old_val': old_val,
                            'new_val': new_val,
                            'detail': {
                                'what': f'dp[{j}][{k}] = max({old_val}, dp[{j-w}][{k-c}]+{v}) = {new_val}',
                                'why': f'选择物品{i+1}后价值更高',
                                'purpose': '更新最优解'
                            }
                        })
        
        # 最终结果
        self.steps.append({
            'type': 'result',
            'dp': self.dp.copy(),
            'action': f'算法结束！最大价值 = {self.dp[self.W][self.V]}',
            'item': -1,
            'detail': {
                'what': f'dp[{self.W}][{self.V}] = {self.dp[self.W][self.V]}',
                'why': '这是满足重量≤W且体积≤V的最大价值',
                'purpose': '得到最终答案'
            }
        })
    
    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step
        
        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index
        step_data = self.steps[step_index]
        
        # 绘制 DP 表格
        self.ax_table.clear()
        
        dp = step_data['dp']
        
        # 只显示部分表格（避免太大）
        display_W = min(self.W + 1, 12)
        display_V = min(self.V + 1, 12)
        
        im = self.ax_table.imshow(dp[:display_W, :display_V], cmap='YlGnBu', aspect='auto')
        
        # 添加数值标注
        for i in range(display_W):
            for j in range(display_V):
                text = self.ax_table.text(j, i, dp[i, j],
                                         ha='center', va='center', fontsize=10)
                
                # 高亮当前更新的单元格
                if step_data['type'] == 'update':
                    cell = step_data.get('cell', (-1, -1))
                    if (i, j) == cell:
                        text.set_color('red')
                        text.set_fontweight('bold')
                        text.set_fontsize(12)
        
        self.ax_table.set_xlabel('体积 (Volume)', fontsize=12)
        self.ax_table.set_ylabel('重量 (Weight)', fontsize=12)
        self.ax_table.set_title(f'DP 表格 (步骤 {step_index + 1}/{len(self.steps)})', fontsize=14)
        
        # 绘制信息区域
        self.ax_info.clear()
        self.ax_info.axis('off')
        
        y_pos = 0.95
        
        # 当前操作
        self.ax_info.text(0.05, y_pos, '📋 当前操作', fontsize=14, fontweight='bold',
                         transform=self.ax_info.transAxes)
        y_pos -= 0.08
        
        self.ax_info.text(0.05, y_pos, step_data['action'], fontsize=12,
                         transform=self.ax_info.transAxes,
                         bbox=dict(boxstyle='round', facecolor='#e8f6f3', alpha=0.9))
        y_pos -= 0.12
        
        # 详细说明
        detail = step_data.get('detail', {})
        if detail:
            self.ax_info.text(0.05, y_pos, '📖 详细说明', fontsize=14, fontweight='bold',
                             transform=self.ax_info.transAxes)
            y_pos -= 0.08
            
            info_text = []
            if 'what' in detail:
                info_text.append(f"做什么：{detail['what']}")
            if 'why' in detail:
                info_text.append(f"为什么：{detail['why']}")
            if 'purpose' in detail:
                info_text.append(f"目的：{detail['purpose']}")
            
            self.ax_info.text(0.05, y_pos, '\n'.join(info_text), fontsize=11,
                             transform=self.ax_info.transAxes, linespacing=1.5,
                             bbox=dict(boxstyle='round', facecolor='#fdebd0', alpha=0.9))
            y_pos -= 0.20
        
        # 物品信息
        self.ax_info.text(0.05, y_pos, '📦 物品列表', fontsize=14, fontweight='bold',
                         transform=self.ax_info.transAxes)
        y_pos -= 0.08
        
        items_text = "序号  重量  体积  价值\n"
        items_text += "-" * 25 + "\n"
        for i in range(self.n):
            marker = "→" if step_data.get('item', -1) == i else " "
            items_text += f"{marker} {i+1:2d}    {self.weights[i]:3d}   {self.volumes[i]:3d}   {self.values[i]:3d}\n"
        
        self.ax_info.text(0.05, y_pos, items_text, fontsize=10, family='monospace',
                         transform=self.ax_info.transAxes,
                         bbox=dict(boxstyle='round', facecolor='#d5f5e3', alpha=0.9))
        
        # 操作提示
        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q 退出'
        self.ax_info.text(0.5, 0.02, controls_text, transform=self.ax_info.transAxes,
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
    print("    0-1背包问题的推广 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("  1. 示例 1: 题目样例 (3个物品)")
    print("  2. 示例 2: 5个物品")
    print("  3. 自定义输入")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    if choice == '1':
        n, W, V = 3, 4, 5
        weights = [1, 2, 3]
        volumes = [2, 3, 4]
        values = [3, 4, 5]
    elif choice == '2':
        n, W, V = 5, 10, 10
        weights = [2, 3, 4, 5, 1]
        volumes = [3, 4, 5, 6, 2]
        values = [4, 5, 6, 7, 3]
    elif choice == '3':
        line = input("请输入 n W V: ").split()
        n, W, V = int(line[0]), int(line[1]), int(line[2])
        weights, volumes, values = [], [], []
        for i in range(n):
            line = input(f"物品 {i+1} (重量 体积 价值): ").split()
            weights.append(int(line[0]))
            volumes.append(int(line[1]))
            values.append(int(line[2]))
    else:
        print("无效选择，使用示例 1")
        n, W, V = 3, 4, 5
        weights = [1, 2, 3]
        volumes = [2, 3, 4]
        values = [3, 4, 5]
    
    print("\n" + "─" * 60)
    print(f"物品数: {n}, 重量限制: {W}, 体积限制: {V}")
    print("─" * 60)
    print("\n📌 操作提示：")
    print("   空格 / 右箭头 ：下一步")
    print("   左箭头       ：上一步")
    print("   Home / End   ：跳转到起点 / 终点")
    print("   Q / Esc      ：退出动画")
    print("\n⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")
    
    anim = KnapsackAnimation(n, W, V, weights, volumes, values)
    anim.show()


if __name__ == '__main__':
    main()
