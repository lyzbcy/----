"""
LeetCode 36. 有效的数独 - 动画演示
使用 matplotlib 手动控制逐格扫描并展示三张标记表的更新过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 示例棋盘（示例1）
BOARD_EXAMPLE1 = [
    ["5","3",".",".","7",".",".",".","."],
    ["6",".",".","1","9","5",".",".","."],
    [".","9","8",".",".",".",".","6","."],
    ["8",".",".",".","6",".",".",".","3"],
    ["4",".",".","8",".","3",".",".","1"],
    ["7",".",".",".","2",".",".",".","6"],
    [".","6",".",".",".",".","2","8","."],
    [".",".",".",".","1","9",".",".","5"],
    [".",".",".",".","8",".",".","7","9"],
]

# 示例棋盘（示例2，左上角 8 和第4行第0列 8 冲突宫）
BOARD_EXAMPLE2 = [
    ["8","3",".",".","7",".",".",".","."],
    ["6",".",".","1","9","5",".",".","."],
    [".","9","8",".",".",".",".","6","."],
    ["8",".",".",".","6",".",".",".","3"],
    ["4",".",".","8",".","3",".",".","1"],
    ["7",".",".",".","2",".",".",".","6"],
    [".","6",".",".",".",".","2","8","."],
    [".",".",".",".","1","9",".",".","5"],
    [".",".",".",".","8",".",".","7","9"],
]


class SudokuAnimation:
    def __init__(self, board):
        self.board = board
        self.steps = []
        self.current_step = 0

        self.code_lines = [
            "bool row[9][10], col[9][10], box[9][10];",
            "memset(row/col/box, 0, ...);",
            "for(int i=0; i<9; i++){",
            "  for(int j=0; j<9; j++){",
            "    if(board[i][j]=='.') continue;",
            "    int num = board[i][j]-'0';",
            "    int boxIndex=(i/3)*3+j/3;",
            "    if(row[i][num]||col[j][num]",
            "       ||box[boxIndex][num])",
            "      return false;",
            "    row[i][num]=true;",
            "    col[j][num]=true;",
            "    box[boxIndex][num]=true;",
            "  }",
            "}",
            "return true;",
        ]

        self._simulate()

        self.fig, self.ax = plt.subplots(figsize=(16, 10))
        self.fig.canvas.manager.set_window_title('有效的数独 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-0.5, 22)
        self.ax.set_ylim(-1, 13)
        self.fig.canvas.mpl_connect('key_press_event', self._on_key)

    def _simulate(self):
        row = [[False]*10 for _ in range(9)]
        col = [[False]*10 for _ in range(9)]
        box = [[False]*10 for _ in range(9)]

        self.steps.append({
            'cur': None,
            'row': [r[:] for r in row],
            'col': [c[:] for c in col],
            'box': [b[:] for b in box],
            'conflict': None,
            'valid': None,
            'action': '初始化：三张标记表全部置 false，准备从 (0,0) 开始扫描',
            'code_hl': [0, 1, 2, 3],
            'explains': ['预分配 row[9][10]、col[9][10]、box[9][10] 三张布尔表。',
                         '从左到右、从上到下逐格扫描 81 个格子。']
        })

        result = True
        conflict_cell = None
        for i in range(9):
            for j in range(9):
                ch = self.board[i][j]
                if ch == '.':
                    self.steps.append({
                        'cur': (i, j),
                        'row': [r[:] for r in row],
                        'col': [c[:] for c in col],
                        'box': [b[:] for b in box],
                        'conflict': None,
                        'valid': None,
                        'action': f'格子 ({i},{j}) = "."，空格跳过',
                        'code_hl': [3, 4],
                        'explains': [f'当前格子 ({i},{j}) 是空格 "."，', '无需检查，直接跳过。']
                    })
                    continue

                num = ord(ch) - ord('0')
                bi = (i // 3) * 3 + j // 3

                conflict = row[i][num] or col[j][num] or box[bi][num]
                if conflict:
                    conflict_cell = (i, j)
                    self.steps.append({
                        'cur': (i, j),
                        'row': [r[:] for r in row],
                        'col': [c[:] for c in col],
                        'box': [b[:] for b in box],
                        'conflict': (i, j),
                        'valid': False,
                        'action': f'❌ 格子 ({i},{j}) = {ch}（宫{bi}）发现冲突！返回 false',
                        'code_hl': [5, 6, 7, 8, 9],
                        'explains': [
                            f'num={num}，宫编号 boxIndex=({i}//3)*3+{j}//3={bi}。',
                            f'row[{i}][{num}]={row[i][num]} | col[{j}][{num}]={col[j][num]} | box[{bi}][{num}]={box[bi][num]}。',
                            '存在重复！立即返回 false。'
                        ]
                    })
                    result = False
                    # 不break，继续标记显示
                    return  # 冲突后直接结束模拟，最后步已记录

                self.steps.append({
                    'cur': (i, j),
                    'row': [r[:] for r in row],
                    'col': [c[:] for c in col],
                    'box': [b[:] for b in box],
                    'conflict': None,
                    'valid': None,
                    'action': f'格子 ({i},{j}) = {ch}，num={num}，宫{bi}，无冲突 → 标记',
                    'code_hl': [5, 6, 7, 8, 10, 11, 12],
                    'explains': [
                        f'num={num}，宫编号 boxIndex=({i}//3)*3+{j}//3={bi}。',
                        f'row[{i}][{num}]、col[{j}][{num}]、box[{bi}][{num}] 均为 false，无冲突。',
                        '将三张表对应位置置为 true，继续扫描。'
                    ]
                })

                row[i][num] = True
                col[j][num] = True
                box[bi][num] = True

        self.steps.append({
            'cur': None,
            'row': [r[:] for r in row],
            'col': [c[:] for c in col],
            'box': [b[:] for b in box],
            'conflict': None,
            'valid': True,
            'action': '✅ 全部 81 格扫描完毕，无冲突，返回 true',
            'code_hl': [14, 15],
            'explains': ['所有数字均符合行、列、宫规则。', '数独有效，返回 true。']
        })

    def _draw_board(self, step_data):
        """绘制 9×9 棋盘"""
        ox, oy = 0.0, 1.5
        cell = 0.9

        # 9×9 格子
        for i in range(9):
            for j in range(9):
                ch = self.board[i][j]
                # 颜色
                color = 'white'
                if step_data['cur'] == (i, j):
                    color = 'yellow' if step_data['conflict'] is None else 'tomato'
                elif step_data['cur'] is not None:
                    ci, cj = step_data['cur']
                    if i < ci or (i == ci and j < cj):
                        color = 'lightgreen'

                rect = patches.Rectangle(
                    (ox + j * cell, oy + (8 - i) * cell), cell, cell,
                    linewidth=0.5, edgecolor='gray', facecolor=color
                )
                self.ax.add_patch(rect)
                if ch != '.':
                    self.ax.text(ox + j * cell + cell / 2,
                                 oy + (8 - i) * cell + cell / 2,
                                 ch, ha='center', va='center', fontsize=13, fontweight='bold')

        # 粗线分隔 3×3 宫
        for k in range(4):
            lw = 2.5 if k % 3 == 0 else 0.5
            self.ax.plot([ox + k * 3 * cell, ox + k * 3 * cell],
                         [oy, oy + 9 * cell], 'k-', linewidth=lw)
            self.ax.plot([ox, ox + 9 * cell],
                         [oy + k * 3 * cell, oy + k * 3 * cell], 'k-', linewidth=lw)
        self.ax.plot([ox + 9 * cell, ox + 9 * cell], [oy, oy + 9 * cell], 'k-', linewidth=2.5)
        self.ax.plot([ox, ox + 9 * cell], [oy + 9 * cell, oy + 9 * cell], 'k-', linewidth=2.5)

        self.ax.text(ox + 9 * cell / 2, oy + 9 * cell + 0.3,
                     '数独棋盘', ha='center', fontsize=12, fontweight='bold')

    def _draw_mini_table(self, table, name, ox, oy):
        """绘制一张 9行×9列 的迷你标记表（显示1~9）"""
        cell = 0.35
        self.ax.text(ox + 4.5 * cell, oy + 0.3, name,
                     ha='center', fontsize=9, fontweight='bold',
                     bbox=dict(boxstyle='round', facecolor='thistle', alpha=0.6))
        for r in range(9):
            for c in range(1, 10):
                val = table[r][c]
                fc = 'gold' if val else 'white'
                self.ax.add_patch(patches.Rectangle(
                    (ox + (c - 1) * cell, oy - r * cell - cell),
                    cell, cell,
                    linewidth=0.3, edgecolor='gray', facecolor=fc
                ))
                self.ax.text(ox + (c - 1) * cell + cell / 2,
                             oy - r * cell - cell / 2,
                             str(c), ha='center', va='center', fontsize=5.5)

    def _draw_code(self, step_data):
        sx, sy = 14.5, 12
        hl = set(step_data.get('code_hl', []))
        self.ax.text(sx, sy + 0.3, 'C 代码同步', fontsize=10, fontweight='bold',
                     bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.6))
        for idx, line in enumerate(self.code_lines):
            fc = 'peachpuff' if idx in hl else 'white'
            self.ax.text(sx, sy - idx * 0.52 - 0.3,
                         f'{idx+1:02d} {line}',
                         ha='left', va='center', fontsize=7.5, family='monospace',
                         bbox=dict(boxstyle='round', facecolor=fc, alpha=0.9, pad=0.2))

    def _draw_step(self, idx=None):
        if idx is None:
            idx = self.current_step
        idx = max(0, min(idx, len(self.steps) - 1))
        self.current_step = idx
        sd = self.steps[idx]

        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim(-0.5, 22)
        self.ax.set_ylim(-1, 13)

        # 标题
        self.ax.text(10, 12.6,
                     f'步骤 {idx+1}/{len(self.steps)}  |  LeetCode 36. 有效的数独',
                     ha='center', fontsize=14, fontweight='bold',
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        # 动作
        self.ax.text(6.5, 12.0, sd['action'],
                     ha='center', fontsize=10.5,
                     bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

        # 解释
        if sd['explains']:
            self.ax.text(6.5, 11.1, '\n'.join(f'· {l}' for l in sd['explains']),
                         ha='center', fontsize=10,
                         bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.9))

        # 操作提示
        self.ax.text(6.5, 10.1,
                     '操作：空格/→ 下一步 · ← 上一步 · Home/End 首尾 · Q/Esc 退出',
                     ha='center', fontsize=9,
                     bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6))

        # 结果标签
        if sd['valid'] is True:
            self.ax.text(6.5, 9.4, '✅ 返回 true', ha='center', fontsize=13,
                         color='green', fontweight='bold',
                         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
        elif sd['valid'] is False:
            self.ax.text(6.5, 9.4, '❌ 返回 false', ha='center', fontsize=13,
                         color='red', fontweight='bold',
                         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

        # 棋盘
        self._draw_board(sd)

        # 三张标记表
        self._draw_mini_table(sd['row'], 'row 行标记（金=已出现）', 9.5, 8.8)
        self._draw_mini_table(sd['col'], 'col 列标记', 9.5, 5.3)
        self._draw_mini_table(sd['box'], 'box 宫标记', 9.5, 1.8)

        # 代码面板
        self._draw_code(sd)

        # 图例
        legend = [('lightgreen', '已扫描'), ('yellow', '当前格'), ('tomato', '冲突格')]
        for li, (lc, lt) in enumerate(legend):
            self.ax.add_patch(patches.Rectangle((li * 2.5, 0.2), 0.5, 0.4,
                                                facecolor=lc, edgecolor='black'))
            self.ax.text(li * 2.5 + 0.6, 0.4, lt, fontsize=9, va='center')

        self.fig.canvas.draw()

    def _on_key(self, event):
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
        plt.tight_layout()
        plt.show()


def main():
    print("=" * 60)
    print("LeetCode 36. 有效的数独 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1：有效数独 → 返回 true")
    print("2. 示例 2：左上宫有两个 8 → 返回 false")

    choice = input("\n请输入选择 (1/2): ").strip()

    if choice == '2':
        board = BOARD_EXAMPLE2
        print("使用示例 2（冲突棋盘）")
    else:
        board = BOARD_EXAMPLE1
        print("使用示例 1（有效棋盘）")

    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转首尾")
    print("  Q / Esc      ：退出\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = SudokuAnimation(board)
    anim.show()


if __name__ == '__main__':
    main()
