#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int M, N;
int min_guards;
int solution_count;
vector<vector<int>> covered;
vector<vector<int>> guards;

// Directions: Center, Up, Down, Left, Right
int dr[5] = {0, -1, 1, 0, 0};
int dc[5] = {0, 0, 0, -1, 1};

bool is_valid(int r, int c) {
    return r >= 0 && r < M && c >= 0 && c < N;
}

void add_guard(int r, int c) {
    guards[r][c] = 1;
    for (int i = 0; i < 5; ++i) {
        int nr = r + dr[i];
        int nc = c + dc[i];
        if (is_valid(nr, nc)) {
            covered[nr][nc]++;
        }
    }
}

void remove_guard(int r, int c) {
    guards[r][c] = 0;
    for (int i = 0; i < 5; ++i) {
        int nr = r + dr[i];
        int nc = c + dc[i];
        if (is_valid(nr, nc)) {
            covered[nr][nc]--;
        }
    }
}

void solve(int idx, int count) {
    // Pruning 1: Count check
    if (count > min_guards) return;

    if (idx == M * N) {
        bool all_covered = true;
        for (int i = 0; i < M; ++i) {
            for (int j = 0; j < N; ++j) {
                if (covered[i][j] == 0) {
                    all_covered = false;
                    break;
                }
            }
            if (!all_covered) break;
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

    // Pruning 2: Connectivity check
    // If (r-1, c) is not covered, we MUST place a guard at (r, c)
    bool must_place = false;
    if (r > 0) {
        if (covered[r-1][c] == 0) {
            must_place = true;
        }
    }

    // Try placing guard
    if (count + 1 <= min_guards) {
        add_guard(r, c);
        solve(idx + 1, count + 1);
        remove_guard(r, c);
    }

    // Try NOT placing guard (only if not forced)
    if (!must_place) {
        solve(idx + 1, count);
    }
}

int main() {
    if (cin >> M >> N) {
        min_guards = M * N + 1;
        solution_count = 0;
        covered.assign(M, vector<int>(N, 0));
        guards.assign(M, vector<int>(N, 0));

        solve(0, 0);

        cout << min_guards << endl;
        cout << solution_count << endl;
    }
    return 0;
}
