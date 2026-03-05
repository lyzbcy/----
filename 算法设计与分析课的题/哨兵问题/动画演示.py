"""
哨兵问题 - 动画演示
使用 matplotlib 手动控制回溯法的执行过程

特点：
- 可视化网格和哨兵放置
- 每一步的详细说明
- 回溯过程的直观展示
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class SentinelAnimation:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.covered = [[0] * n for _ in range(m)]
        self.guards = [[0] * n for _ in range(m)]
        
        # 记录步骤
        self.steps = []
        self.solutions = []
        self.min_guards = m * n
        self.current_step = 0
        
        # 方向
        self.dr = [0, -1, 1, 0, 0]
        self.dc = [0, 0, 0, -1, 1]
        
        # 模拟算法
        self._simulate(0, 0)
        
        # 创建画布
        self.fig, (self.ax_grid, self.ax_info) = plt.subplots(1, 2, figsize=(14, 8))
        self.fig.canvas.manager.set_window_title('哨兵问题 - 动画演示')
        
        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)
    
    def _is_valid(self, r, c):
        return 0 <= r < self.m and 0 <= c < self.n
    
    def _add_guard(self, r, c):
        self.guards[r][c] = 1
        for i in range(5):
            nr, nc = r + self.dr[i], c + self.dc[i]
            if self._is_valid(nr, nc):
                self.covered[nr][nc] += 1
    
    def _remove_guard(self, r, c):
        self.guards[r][c] = 0
        for i in range(5):
            nr, nc = r + self.dr[i], c + self.dc[i]
            if self._is_valid(nr, nc):
                self.covered[nr][nc] -= 1
    
    def _copy_state(self):
        return {
            'covered': [row[:] for row in self.covered],
            'guards': [row[:] for row in self.guards]
        }
    
    def _simulate(self, idx, count):
        if count > self.min_guards:
            return
        
        if idx == self.m * self.n:
            # 检查是否全部覆盖
            all_covered = all(self.covered[i][j] > 0 
                            for i in range(self.m) for j in range(self.n))
            if all_covered:
                if count < self.min_guards:
                    self.min_guards = count
                    self.solutions = [self._copy_state()]
                elif count == self.min_guards:
                    self.solutions.append(self._copy_state())
                
                self.steps.append({
                    'type': 'found',
                    'state': self._copy_state(),
                    'idx': idx,
                    'count': count,
                    'action': f'🎉 找到解！使用 {count} 个哨兵',
                    'detail': {
                        'what': '所有格子都被覆盖',
                        'why': '这是一个有效的方案',
                        'purpose': '记录并继续搜索更优解'
                    }
                })
            return
        
        r, c = idx // self.n, idx % self.n
        
        # 可行性剪枝
        must_place = False
        if r > 0 and self.covered[r-1][c] == 0:
            must_place = True
        
        if must_place:
            self.steps.append({
                'type': 'force_place',
                'state': self._copy_state(),
                'idx': idx,
                'r': r, 'c': c,
                'count': count,
                'action': f'强制放置：({r},{c}) 上方未覆盖',
                'detail': {
                    'what': f'格子({r-1},{c})未被覆盖',
                    'why': '这是覆盖它的最后机会',
                    'purpose': '必须在此放置哨兵'
                }
            })
            
            self._add_guard(r, c)
            self.steps.append({
                'type': 'place',
                'state': self._copy_state(),
                'idx': idx,
                'r': r, 'c': c,
                'count': count + 1,
                'action': f'放置哨兵：({r},{c})',
                'detail': {
                    'what': f'在({r},{c})放置第 {count+1} 个哨兵',
                    'why': '强制放置',
                    'purpose': '覆盖周围5个格子'
                }
            })
            self._simulate(idx + 1, count + 1)
            self._remove_guard(r, c)
            self.steps.append({
                'type': 'backtrack',
                'state': self._copy_state(),
                'idx': idx,
                'r': r, 'c': c,
                'count': count,
                'action': f'回溯：移除({r},{c})的哨兵',
                'detail': {
                    'what': f'撤销({r},{c})的哨兵',
                    'why': '探索其他可能',
                    'purpose': '回溯搜索'
                }
            })
        else:
            # 先尝试不放
            self.steps.append({
                'type': 'skip',
                'state': self._copy_state(),
                'idx': idx,
                'r': r, 'c': c,
                'count': count,
                'action': f'跳过：不在({r},{c})放置',
                'detail': {
                    'what': f'尝试不在({r},{c})放哨兵',
                    'why': '优先尝试使用更少的哨兵',
                    'purpose': '探索最优解'
                }
            })
            self._simulate(idx + 1, count)
            
            # 再尝试放
            if count + 1 <= self.min_guards:
                self._add_guard(r, c)
                self.steps.append({
                    'type': 'place',
                    'state': self._copy_state(),
                    'idx': idx,
                    'r': r, 'c': c,
                    'count': count + 1,
                    'action': f'放置哨兵：({r},{c})',
                    'detail': {
                        'what': f'在({r},{c})放置第 {count+1} 个哨兵',
                        'why': '尝试这个分支',
                        'purpose': '覆盖周围5个格子'
                    }
                })
                self._simulate(idx + 1, count + 1)
                self._remove_guard(r, c)
                self.steps.append({
                    'type': 'backtrack',
                    'state': self._copy_state(),
                    'idx': idx,
                    'r': r, 'c': c,
                    'count': count,
                    'action': f'回溯：移除({r},{c})的哨兵',
                    'detail': {
                        'what': f'撤销({r},{c})的哨兵',
                        'why': '该分支探索完毕',
                        'purpose': '回溯搜索'
                    }
                })
    
    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step
        
        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index
        step_data = self.steps[step_index]
        
        # 绘制网格
        self.ax_grid.clear()
        
        state = step_data['state']
        covered = state['covered']
        guards = state['guards']
        
        # 绘制格子
        for i in range(self.m):
            for j in range(self.n):
                color = 'white'
                if guards[i][j]:
                    color = '#e74c3c'  # 哨兵
                elif covered[i][j] > 0:
                    color = '#a8e6cf'  # 被覆盖
                
                rect = patches.Rectangle((j, self.m - 1 - i), 1, 1,
                                         linewidth=2, edgecolor='black',
                                         facecolor=color)
                self.ax_grid.add_patch(rect)
                
                # 显示覆盖次数
                if covered[i][j] > 0:
                    self.ax_grid.text(j + 0.5, self.m - 0.5 - i,
                                     str(covered[i][j]),
                                     ha='center', va='center',
                                     fontsize=14, fontweight='bold')
                
                # 哨兵标记
                if guards[i][j]:
                    self.ax_grid.text(j + 0.5, self.m - 0.5 - i, '👮',
                                     ha='center', va='center', fontsize=20)
        
        # 高亮当前格子
        if 'r' in step_data and 'c' in step_data:
            r, c = step_data['r'], step_data['c']
            highlight = patches.Rectangle((c, self.m - 1 - r), 1, 1,
                                          linewidth=4, edgecolor='blue',
                                          facecolor='none')
            self.ax_grid.add_patch(highlight)
        
        self.ax_grid.set_xlim(-0.1, self.n + 0.1)
        self.ax_grid.set_ylim(-0.1, self.m + 0.1)
        self.ax_grid.set_aspect('equal')
        self.ax_grid.axis('off')
        self.ax_grid.set_title(f'步骤 {step_index + 1}/{len(self.steps)}',
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
            y_pos -= 0.18
        
        # 统计信息
        count = step_data.get('count', 0)
        self.ax_info.text(0.05, y_pos, f'当前哨兵数: {count}\n最优解: {self.min_guards}',
                         fontsize=12, transform=self.ax_info.transAxes,
                         bbox=dict(boxstyle='round', facecolor='#d5f5e3', alpha=0.9))
        
        # 图例
        self.ax_info.text(0.05, 0.25, '图例：\n👮 哨兵\n🟥 哨兵位置\n🟩 被覆盖\n⬜ 未覆盖\n🔵 当前格子',
                         fontsize=11, transform=self.ax_info.transAxes,
                         bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
        
        # 操作提示
        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Q 退出'
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
    print("    哨兵问题 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("  1. 2×3 网格（题目样例）")
    print("  2. 3×3 网格")
    print("  3. 自定义输入")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    if choice == '1':
        m, n = 2, 3
    elif choice == '2':
        m, n = 3, 3
    elif choice == '3':
        line = input("请输入 m 和 n（空格分隔）: ").split()
        m, n = int(line[0]), int(line[1])
    else:
        print("无效选择，使用 2×3")
        m, n = 2, 3
    
    print("\n" + "─" * 60)
    print(f"网格大小: {m} × {n}")
    print("─" * 60)
    print("\n📌 操作提示：")
    print("   空格 / 右箭头 ：下一步")
    print("   左箭头       ：上一步")
    print("   Q / Esc      ：退出动画")
    print("\n⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")
    
    anim = SentinelAnimation(m, n)
    anim.show()


if __name__ == '__main__':
    main()
