/**
 * 0-1背包问题的推广（二维费用背包）
 * 
 * 使用动态规划求解
 * 时间复杂度：O(n × W × V)
 * 空间复杂度：O(W × V)
 */

#include <stdio.h>
#include <string.h>

#define MAX_N 105
#define MAX_W 115
#define MAX_V 115

// dp[j][k] 表示重量不超过j，体积不超过k时的最大价值
int dp[MAX_W][MAX_V];

// 物品属性
int w[MAX_N];  // 重量
int c[MAX_N];  // 体积
int v[MAX_N];  // 价值

// 返回两个数中的较大值
int max(int a, int b) {
    return a > b ? a : b;
}

int main() {
    int n, W, V;
    
    // 读取输入：物品数n，重量限制W，体积限制V
    scanf("%d %d %d", &n, &W, &V);
    
    // 读取每个物品的属性
    for (int i = 0; i < n; i++) {
        scanf("%d %d %d", &w[i], &c[i], &v[i]);
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
    printf("%d\n", dp[W][V]);
    
    return 0;
}
