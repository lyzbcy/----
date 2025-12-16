"""
Latin矩阵问题 - 动画演示
使用 matplotlib 手动控制回溯法的执行过程

特点：
- 可视化矩阵填充过程
- 每一步的详细说明
- 回溯过程的直观展示
"""

import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class LatinSquareAnimation:
    def __init__(self, n):
        self.n = n
        self.matrix = [[0] * n for _ in range(n)]
        self.rowUsed = [[False] * (n + 1) for _ in range(n)]
        self.colUsed = [[False] * (n + 1) for _ in range(n)]
        
        # 初始化第一行
        for i in range(n):
            self.matrix[0][i] = i + 1
            self.rowUsed[0][i + 1] = True
            self.colUsed[i][i + 1] = True
        
        # 记录步骤
        self.steps = []
        self.solutions = []
        self.current_step = 0
        
        # 模拟算法
        self._simulate(1, 0)
        
        # 创建画布
        self.fig, (self.ax_matrix, self.ax_info) = plt.subplots(1, 2, figsize=(14, 8))
        self.fig.canvas.manager.set_window_title('Latin矩阵问题 - 动画演示')
        
        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)
    
    def _copy_matrix(self):
        return [row[:] for row in self.matrix]
    
    def _simulate(self, row, col):
        """模拟回溯算法"""
        
        if row == self.n:
            self.solutions.append(self._copy_matrix())
            self.steps.append({
                'type': 'found',
                'matrix': self._copy_matrix(),
                'row': row,
                'col': col,
                'action': f'🎉 找到一个解！（第 {len(self.solutions)} 个）',
                'detail': {
                    'what': '所有格子都已填满',
                    'why': '满足所有约束条件',
                    'purpose': '记录这个有效的拉丁方'
                }
            })
            return
        
        nextRow = row + 1 if col == self.n - 1 else row
        nextCol = 0 if col == self.n - 1 else col + 1
        
        for num in range(1, self.n + 1):
            if not self.rowUsed[row][num] and not self.colUsed[col][num]:
                # 放置
                self.matrix[row][col] = num
                self.rowUsed[row][num] = True
                self.colUsed[col][num] = True
                
                self.steps.append({
                    'type': 'place',
                    'matrix': self._copy_matrix(),
                    'row': row,
                    'col': col,
                    'num': num,
                    'action': f'放置 {num} 到位置 ({row}, {col})',
                    'detail': {
                        'what': f'在第{row+1}行第{col+1}列放置数字{num}',
                        'why': f'{num}不在第{row+1}行和第{col+1}列中',
                        'purpose': '尝试这个选择'
                    }
                })
                
                self._simulate(nextRow, nextCol)
                
                # 回溯
                self.matrix[row][col] = 0
                self.rowUsed[row][num] = False
                self.colUsed[col][num] = False
                
                self.steps.append({
                    'type': 'backtrack',
                    'matrix': self._copy_matrix(),
                    'row': row,
                    'col': col,
                    'num': num,
                    'action': f'回溯：移除位置 ({row}, {col}) 的 {num}',
                    'detail': {
                        'what': f'撤销第{row+1}行第{col+1}列的数字{num}',
                        'why': '需要尝试其他可能性',
                        'purpose': '探索其他分支'
                    }
                })
    
    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step
        
        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index
        step_data = self.steps[step_index]
        
        # 绘制矩阵
        self.ax_matrix.clear()
        matrix = step_data['matrix']
        
        # 创建颜色矩阵
        colors = np.ones((self.n, self.n, 3))  # 白色背景
        
        current_row = step_data.get('row', -1)
        current_col = step_data.get('col', -1)
        
        for i in range(self.n):
            for j in range(self.n):
                if i == 0:
                    colors[i][j] = [0.9, 0.9, 1.0]  # 第一行浅蓝色
                elif i == current_row and j == current_col:
                    if step_data['type'] == 'place':
                        colors[i][j] = [0.5, 1.0, 0.5]  # 绿色（放置）
                    elif step_data['type'] == 'backtrack':
                        colors[i][j] = [1.0, 0.5, 0.5]  # 红色（回溯）
                    else:
                        colors[i][j] = [1.0, 1.0, 0.5]  # 黄色（找到解）
        
        self.ax_matrix.imshow(colors, aspect='equal')
        
        # 添加网格线
        for i in range(self.n + 1):
            self.ax_matrix.axhline(i - 0.5, color='black', linewidth=2)
            self.ax_matrix.axvline(i - 0.5, color='black', linewidth=2)
        
        # 添加数字
        for i in range(self.n):
            for j in range(self.n):
                if matrix[i][j] != 0:
                    self.ax_matrix.text(j, i, str(matrix[i][j]),
                                       ha='center', va='center',
                                       fontsize=20, fontweight='bold')
        
        self.ax_matrix.set_xlim(-0.5, self.n - 0.5)
        self.ax_matrix.set_ylim(self.n - 0.5, -0.5)
        self.ax_matrix.set_xticks(range(self.n))
        self.ax_matrix.set_yticks(range(self.n))
        self.ax_matrix.set_xticklabels([f'列{i+1}' for i in range(self.n)])
        self.ax_matrix.set_yticklabels([f'行{i+1}' for i in range(self.n)])
        self.ax_matrix.set_title(f'步骤 {step_index + 1}/{len(self.steps)}',
                                  fontsize=14, fontweight='bold')
        
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
            self.ax_info.text(0.05, y_pos, '📖 说明', fontsize=14, fontweight='bold',
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
        
        # 已找到的解数量
        solutions_found = sum(1 for s in self.steps[:step_index+1] if s['type'] == 'found')
        self.ax_info.text(0.05, y_pos, f'已找到解的数量: {solutions_found}', fontsize=12,
                         transform=self.ax_info.transAxes,
                         bbox=dict(boxstyle='round', facecolor='#d5f5e3', alpha=0.9))
        
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
    print("    Latin矩阵问题 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("  1. n = 3（3阶拉丁方，较快）")
    print("  2. n = 4（4阶拉丁方，题目要求）")
    
    choice = input("\n请输入选择 (1-2): ").strip()
    
    if choice == '1':
        n = 3
    elif choice == '2':
        n = 4
    else:
        print("无效选择，使用 n = 3")
        n = 3
    
    print("\n" + "─" * 60)
    print(f"生成 {n} 阶拉丁方（第一行固定为 1,2,...,{n}）")
    print("─" * 60)
    print("\n📌 操作提示：")
    print("   空格 / 右箭头 ：下一步")
    print("   左箭头       ：上一步")
    print("   Home / End   ：跳转到起点 / 终点")
    print("   Q / Esc      ：退出动画")
    print("\n⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")
    
    anim = LatinSquareAnimation(n)
    anim.show()


if __name__ == '__main__':
    main()
