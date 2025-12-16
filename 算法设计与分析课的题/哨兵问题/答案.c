#include <stdio.h>
#include <stdlib.h>

int M, N;
int grid[105][105]; // 记录每个格子被多少个卫兵监视
int min_guards;     // 当前找到的最小卫兵数
int solution_count; // 达到最小卫兵数的方案数

// 在 (r, c) 放置或移除卫兵
// val = 1 表示放置（增加覆盖计数），val = -1 表示移除（减少覆盖计数）
void update_coverage(int r, int c, int val) {
    grid[r][c] += val;
    if (r > 0) grid[r - 1][c] += val;
    if (r < M - 1) grid[r + 1][c] += val;
    if (c > 0) grid[r][c - 1] += val;
    if (c < N - 1) grid[r][c + 1] += val;
}

void dfs(int k, int current_guards) {
    // 剪枝 1：如果当前卫兵数已经超过了已知的最小值，没必要继续
    if (current_guards > min_guards) return;

    // 基本情况：遍历完所有格子
    if (k == M * N) {
        // 检查最后一行是否全部被覆盖
        // (之前的逻辑保证了除最后一行外的所有行都被覆盖，且最后一行的大部分也被约束，但需最后确认)
        for (int j = 0; j < N; j++) {
            if (grid[M - 1][j] == 0) return;
        }

        // 更新最优解
        if (current_guards < min_guards) {
            min_guards = current_guards;
            solution_count = 1;
        } else if (current_guards == min_guards) {
            solution_count++;
        }
        return;
    }

    int r = k / N;
    int c = k % N;

    // 剪枝 2：强制放置逻辑 (Pruning by Necessity)
    // 检查是否存在“由于离开了当前位置，将永远无法被覆盖”的格子
    int must_place = 0;

    // 检查上方格子：如果 (r-1, c) 未被覆盖，且当前在 (r, c)，这是覆盖它的最后机会
    if (r > 0 && grid[r - 1][c] == 0) {
        must_place = 1;
    }
    // 检查最后一行时的左侧格子：如果 (r, c-1) 未被覆盖，这是覆盖它的最后机会
    else if (r == M - 1 && c > 0 && grid[r][c - 1] == 0) {
        must_place = 1;
    }
    // 检查最后一个格子：如果自己没被覆盖，必须放
    else if (r == M - 1 && c == N - 1 && grid[r][c] == 0) {
        must_place = 1;
    }

    if (must_place) {
        // 必须放置
        update_coverage(r, c, 1);
        dfs(k + 1, current_guards + 1);
        update_coverage(r, c, -1); // 回溯
    } else {
        // 分支 1：不放卫兵
        // 优先尝试不放，有助于快速找到较小的解（贪心倾向）
        dfs(k + 1, current_guards);

        // 分支 2：放置卫兵
        // 只有在当前数量加 1 仍有可能成为最优解时才尝试
        if (current_guards + 1 <= min_guards) {
            update_coverage(r, c, 1);
            dfs(k + 1, current_guards + 1);
            update_coverage(r, c, -1); // 回溯
        }
    }
}

int main() {
    if (scanf("%d %d", &M, &N) != 2) return 0;

    // 优化：确保 N 是较小的一维，这样能更快触发基于行 (r-1) 的剪枝
    // 因为问题关于旋转是对称的，这不影响结果数值
    if (M < N) {
        int temp = M;
        M = N;
        N = temp;
    }

    // 初始化
    min_guards = M * N; // 最坏情况是每个格子放一个
    solution_count = 0;

    // 处理边界情况
    if (M == 0) {
        printf("0\n0\n");
        return 0;
    }

    // 开始搜索
    dfs(0, 0);

    // 输出结果
    printf("%d\n%d\n", min_guards, solution_count);

    return 0;
}
