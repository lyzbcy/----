/**
 * TOP K问题 - 快速选择算法
 * 
 * 时间复杂度：O(n) 期望
 * 空间复杂度：O(1)
 */

#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <algorithm>

using namespace std;

class Solution {
public:
    // 分区操作
    int partition(vector<int>& nums, int left, int right) {
        int pivot = nums[right];
        int i = left - 1;
        
        for (int j = left; j < right; j++) {
            if (nums[j] <= pivot) {
                i++;
                swap(nums[i], nums[j]);
            }
        }
        swap(nums[i + 1], nums[right]);
        return i + 1;
    }
    
    // 随机化分区
    int randomPartition(vector<int>& nums, int left, int right) {
        int randomIndex = left + rand() % (right - left + 1);
        swap(nums[randomIndex], nums[right]);
        return partition(nums, left, right);
    }
    
    // 快速选择
    int quickSelect(vector<int>& nums, int left, int right, int k) {
        if (left == right) {
            return nums[left];
        }
        
        int pivotIndex = randomPartition(nums, left, right);
        
        if (k == pivotIndex) {
            return nums[k];
        } else if (k < pivotIndex) {
            return quickSelect(nums, left, pivotIndex - 1, k);
        } else {
            return quickSelect(nums, pivotIndex + 1, right, k);
        }
    }
    
    // 找第k小的数
    int findKthSmallest(vector<int>& nums, int k) {
        int n = nums.size();
        return quickSelect(nums, 0, n - 1, k - 1);  // 转为0-indexed
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    srand(time(nullptr));
    
    int n, k;
    cin >> n >> k;
    
    vector<int> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }
    
    Solution solution;
    int result = solution.findKthSmallest(nums, k);
    
    cout << result << endl;
    
    return 0;
}
