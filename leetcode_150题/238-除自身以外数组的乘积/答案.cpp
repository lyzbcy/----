/**
 * LeetCode 238. 除自身以外数组的乘积
 *
 * 时间复杂度：O(n)
 * 空间复杂度：O(1) 额外空间
 */

#include <vector>
using namespace std;

class Solution {
public:
    vector<int> productExceptSelf(vector<int>& nums) {
        const int n = static_cast<int>(nums.size());
        vector<int> answer(n, 1);

        int prefix = 1;  // 左侧乘积
        for (int i = 0; i < n; ++i) {
            answer[i] = prefix;
            prefix *= nums[i];
        }

        int suffix = 1;  // 右侧乘积
        for (int i = n - 1; i >= 0; --i) {
            answer[i] *= suffix;
            suffix *= nums[i];
        }

        return answer;
    }
};














