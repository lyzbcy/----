/**
 * 硬币付款问题 - 最小重量
 * 
 * 使用动态规划（完全背包变形）求解
 * 时间复杂度：O(n × target)
 * 空间复杂度：O(target)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_COINS 15
#define MAX_TARGET 1005
#define INF 0x3f3f3f3f

int coin[MAX_COINS];    // 硬币面值
int weight[MAX_COINS];  // 硬币重量
int dp[MAX_TARGET];     // dp[i] = 凑够金额i的最小重量

int min(int a, int b) {
    return a < b ? a : b;
}

int main() {
    char line[1000];
    int n = 0;
    
    // 读取硬币面值
    if (fgets(line, sizeof(line), stdin)) {
        char *p = strtok(line, " \n");
        while (p) {
            coin[n++] = atoi(p);
            p = strtok(NULL, " \n");
        }
    }
    
    // 读取硬币重量
    if (fgets(line, sizeof(line), stdin)) {
        int idx = 0;
        char *p = strtok(line, " \n");
        while (p) {
            weight[idx++] = atoi(p);
            p = strtok(NULL, " \n");
        }
    }
    
    // 读取目标金额
    int target;
    scanf("%d", &target);
    
    // 初始化 dp 数组
    // dp[0] = 0（凑够0元需要0重量）
    // 其他初始化为无穷大（表示无法凑够）
    memset(dp, 0x3f, sizeof(dp));
    dp[0] = 0;
    
    // 动态规划（完全背包，正序遍历金额）
    for (int i = 1; i <= target; i++) {
        for (int j = 0; j < n; j++) {
            // 如果当前硬币面值不超过i，且i-coin[j]可以凑够
            if (coin[j] <= i && dp[i - coin[j]] != INF) {
                dp[i] = min(dp[i], dp[i - coin[j]] + weight[j]);
            }
        }
    }
    
    // 输出结果
    printf("%d\n", dp[target]);
    
    return 0;
}
