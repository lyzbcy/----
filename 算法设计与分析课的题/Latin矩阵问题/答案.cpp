/**
 * Latin矩阵问题 - 回溯法
 * 
 * 生成所有第一行为 1,2,3,...,n 的 n 阶拉丁方
 */

#include <iostream>
#include <vector>
#include <cstring>

using namespace std;

int n;
vector<vector<int>> matrix;
vector<vector<bool>> rowUsed;  // rowUsed[r][num] = 第r行是否使用了num
vector<vector<bool>> colUsed;  // colUsed[c][num] = 第c列是否使用了num

// 输出当前解
void printSolution() {
    // 输出第2行到第n行，用空格分隔
    for (int r = 1; r < n; r++) {
        for (int c = 0; c < n; c++) {
            cout << matrix[r][c];
            if (r != n - 1 || c != n - 1) {
                cout << " ";
            }
        }
    }
    cout << endl;
}

// 回溯搜索
void solve(int row, int col) {
    // 递归终止：填完所有行
    if (row == n) {
        printSolution();
        return;
    }
    
    // 计算下一个位置
    int nextRow = (col == n - 1) ? row + 1 : row;
    int nextCol = (col == n - 1) ? 0 : col + 1;
    
    // 尝试每个数字 1 到 n
    for (int num = 1; num <= n; num++) {
        // 检查约束：该数字是否在当前行或列出现过
        if (!rowUsed[row][num] && !colUsed[col][num]) {
            // 放置
            matrix[row][col] = num;
            rowUsed[row][num] = true;
            colUsed[col][num] = true;
            
            // 递归搜索
            solve(nextRow, nextCol);
            
            // 回溯：恢复状态
            matrix[row][col] = 0;
            rowUsed[row][num] = false;
            colUsed[col][num] = false;
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    cin >> n;
    
    // 初始化
    matrix.assign(n, vector<int>(n, 0));
    rowUsed.assign(n, vector<bool>(n + 1, false));
    colUsed.assign(n, vector<bool>(n + 1, false));
    
    // 第一行固定为 1, 2, 3, ..., n
    for (int i = 0; i < n; i++) {
        matrix[0][i] = i + 1;
        rowUsed[0][i + 1] = true;
        colUsed[i][i + 1] = true;
    }
    
    // 从第2行第1列开始搜索
    solve(1, 0);
    
    return 0;
}
