/**
 * 硬币付款问题 - 最小重量
 * 
 * 使用动态规划（完全背包变形）求解
 * 时间复杂度：O(n × target)
 * 空间复杂度：O(target)
 */

#include <iostream>
#include <vector>
#include <sstream>
#include <algorithm>
#include <climits>

using namespace std;

const int INF = INT_MAX / 2;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    string line;
    vector<int> coins, weights;
    
    // 读取硬币面值
    getline(cin, line);
    istringstream iss1(line);
    int val;
    while (iss1 >> val) {
        coins.push_back(val);
    }
    
    // 读取硬币重量
    getline(cin, line);
    istringstream iss2(line);
    while (iss2 >> val) {
        weights.push_back(val);
    }
    
    // 读取目标金额
    int target;
    cin >> target;
    
    int n = coins.size();
    
    // 初始化 dp 数组
    // dp[i] = 凑够金额i的最小重量
    vector<int> dp(target + 1, INF);
    dp[0] = 0;  // 凑够0元需要0重量
    
    // 动态规划（完全背包，正序遍历金额）
    for (int i = 1; i <= target; i++) {
        for (int j = 0; j < n; j++) {
            // 如果当前硬币面值不超过i，且i-coins[j]可以凑够
            if (coins[j] <= i && dp[i - coins[j]] != INF) {
                dp[i] = min(dp[i], dp[i - coins[j]] + weights[j]);
            }
        }
    }
    
    // 输出结果
    cout << dp[target] << endl;
    
    return 0;
}
