/**
 * 0-1背包问题的推广（二维费用背包）
 * 
 * 使用动态规划求解
 * 时间复杂度：O(n × W × V)
 * 空间复杂度：O(W × V)
 */

#include <iostream>
#include <cstring>
#include <algorithm>

using namespace std;

const int MAX_N = 105;
const int MAX_W = 115;
const int MAX_V = 115;

// dp[j][k] 表示重量不超过j，体积不超过k时的最大价值
int dp[MAX_W][MAX_V];

// 物品属性
int w[MAX_N];  // 重量
int c[MAX_N];  // 体积
int v[MAX_N];  // 价值

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int n, W, V;
    
    // 读取输入：物品数n，重量限制W，体积限制V
    cin >> n >> W >> V;
    
    // 读取每个物品的属性
    for (int i = 0; i < n; i++) {
        cin >> w[i] >> c[i] >> v[i];
    }
    
    // 初始化 dp 数组为 0
    memset(dp, 0, sizeof(dp));
    
    // 动态规划
    for (int i = 0; i < n; i++) {
        // 逆序遍历重量，保证每个物品只被选一次
        for (int j = W; j >= w[i]; j--) {
            // 逆序遍历体积
            for (int k = V; k >= c[i]; k--) {
                // 状态转移：选或不选第i个物品
                dp[j][k] = max(dp[j][k], dp[j - w[i]][k - c[i]] + v[i]);
            }
        }
    }
    
    // 输出最大价值
    cout << dp[W][V] << endl;
    
    return 0;
}
