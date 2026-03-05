/**
 * 哨兵问题 - C++ 版本
 * 
 * 使用回溯法 + 剪枝求解
 * 求最小哨兵数量和方案数
 */

#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int M, N;
int min_guards;
int solution_count;
vector<vector<int>> covered;

// 方向数组：自己、上、下、左、右
int dr[5] = {0, -1, 1, 0, 0};
int dc[5] = {0, 0, 0, -1, 1};

// 检查坐标是否有效
bool is_valid(int r, int c) {
    return r >= 0 && r < M && c >= 0 && c < N;
}

// 放置哨兵：增加覆盖计数
void add_guard(int r, int c) {
    for (int i = 0; i < 5; ++i) {
        int nr = r + dr[i];
        int nc = c + dc[i];
        if (is_valid(nr, nc)) {
            covered[nr][nc]++;
        }
    }
}

// 移除哨兵：减少覆盖计数（回溯）
void remove_guard(int r, int c) {
    for (int i = 0; i < 5; ++i) {
        int nr = r + dr[i];
        int nc = c + dc[i];
        if (is_valid(nr, nc)) {
            covered[nr][nc]--;
        }
    }
}

void solve(int idx, int count) {
    // 剪枝1：当前哨兵数超过已知最优解
    if (count > min_guards) return;

    // 终止条件：遍历完所有格子
    if (idx == M * N) {
        // 检查是否全部覆盖
        bool all_covered = true;
        for (int i = 0; i < M && all_covered; ++i) {
            for (int j = 0; j < N; ++j) {
                if (covered[i][j] == 0) {
                    all_covered = false;
                    break;
                }
            }
        }

        if (all_covered) {
            if (count < min_guards) {
                min_guards = count;
                solution_count = 1;
            } else if (count == min_guards) {
                solution_count++;
            }
        }
        return;
    }

    int r = idx / N;
    int c = idx % N;

    // 剪枝2：可行性剪枝
    // 如果 (r-1, c) 未被覆盖，当前位置是最后机会
    bool must_place = false;
    if (r > 0 && covered[r-1][c] == 0) {
        must_place = true;
    }
    // 最后一行左侧格子的检查
    else if (r == M-1 && c > 0 && covered[r][c-1] == 0) {
        must_place = true;
    }
    // 最后一个格子的检查
    else if (r == M-1 && c == N-1 && covered[r][c] == 0) {
        must_place = true;
    }

    if (must_place) {
        // 必须放置
        add_guard(r, c);
        solve(idx + 1, count + 1);
        remove_guard(r, c);
    } else {
        // 分支1：不放（优先尝试）
        solve(idx + 1, count);

        // 分支2：放置
        if (count + 1 <= min_guards) {
            add_guard(r, c);
            solve(idx + 1, count + 1);
            remove_guard(r, c);
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    if (cin >> M >> N) {
        // 优化：确保 N 是较小的维度
        if (M < N) swap(M, N);
        
        min_guards = M * N;
        solution_count = 0;
        covered.assign(M, vector<int>(N, 0));

        solve(0, 0);

        cout << min_guards << endl;
        cout << solution_count << endl;
    }
    return 0;
}
