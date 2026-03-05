/**
 * 零钱系统问题 - 贪心算法解法
 * 
 * 问题：零钱系统币值为 {1, p, p², ..., pⁿ}，p>1，每个硬币重量为1
 * 目标：对任意金额 y，找到使用最少硬币的方案
 * 
 * 算法思想：贪心算法 = p进制转换
 * 时间复杂度：O(n) = O(log_p(y))
 * 空间复杂度：O(n)
 */

#include <stdio.h>
#include <math.h>

#define MAX_N 100

/**
 * 计算最少硬币数及具体方案
 * 
 * @param y      目标金额
 * @param p      币值基数
 * @param n      最大幂次
 * @param coins  输出：每种面值使用的硬币数
 * @return       最少硬币总数
 */
int minCoins(int y, int p, int n, int coins[]) {
    int total = 0;
    int remaining = y;
    
    // 从最大面值开始贪心选择（等价于p进制转换）
    for (int i = n; i >= 0; i--) {
        int denomination = (int)pow(p, i);  // 当前面值 p^i
        coins[i] = remaining / denomination; // 使用多少个该面值
        remaining %= denomination;           // 剩余金额
        total += coins[i];                   // 累加硬币数
    }
    
    return total;
}

/**
 * 打印结果
 */
void printResult(int y, int p, int n, int coins[], int total) {
    printf("=== 零钱系统问题求解 ===\n");
    printf("币值系统: {");
    for (int i = 0; i <= n; i++) {
        printf("%d", (int)pow(p, i));
        if (i < n) printf(", ");
    }
    printf("}\n");
    printf("目标金额: %d\n", y);
    printf("最少硬币数: %d\n\n", total);
    
    printf("具体方案:\n");
    int first = 1;
    for (int i = n; i >= 0; i--) {
        if (coins[i] > 0) {
            if (!first) printf(" + ");
            printf("%d×%d", coins[i], (int)pow(p, i));
            first = 0;
        }
    }
    printf(" = %d\n\n", y);
    
    // 显示p进制表示
    printf("p进制表示 (%d进制): ", p);
    int started = 0;
    for (int i = n; i >= 0; i--) {
        if (coins[i] > 0 || started) {
            printf("%d", coins[i]);
            started = 1;
        }
    }
    if (!started) printf("0");
    printf("\n");
    printf("各位数字之和: %d\n", total);
}

int main() {
    int p, n, y;
    int coins[MAX_N] = {0};
    
    printf("请输入 p (币值基数, p>1): ");
    scanf("%d", &p);
    
    printf("请输入 n (最大幂次): ");
    scanf("%d", &n);
    
    printf("请输入 y (目标金额): ");
    scanf("%d", &y);
    
    printf("\n");
    
    // 验证输入
    if (p <= 1) {
        printf("错误: p 必须大于 1\n");
        return 1;
    }
    if (n < 0) {
        printf("错误: n 必须非负\n");
        return 1;
    }
    if (y < 0) {
        printf("错误: y 必须非负\n");
        return 1;
    }
    
    // 检查是否可以表示
    int maxValue = (int)(pow(p, n + 1) - 1) / (p - 1);
    if (y > maxValue && (int)pow(p, n) < y) {
        // 由于有面值1，任何非负整数都可以表示
        // 但为了效率，打印警告
        printf("注意: 金额较大，可能需要更多硬币\n\n");
    }
    
    int total = minCoins(y, p, n, coins);
    printResult(y, p, n, coins, total);
    
    return 0;
}

/*
 * 示例运行:
 * 
 * 输入: p=3, n=3, y=23
 * 
 * 币值系统: {1, 3, 9, 27}
 * 目标金额: 23
 * 最少硬币数: 5
 * 
 * 具体方案:
 * 2×9 + 1×3 + 2×1 = 23
 * 
 * p进制表示 (3进制): 212
 * 各位数字之和: 5
 */
