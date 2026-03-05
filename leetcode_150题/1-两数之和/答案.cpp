/**
 * LeetCode 1. 两数之和 - C++ 哈希表解法（附 C 语言选手详细指南）
 *
 * 核心思想：空间换时间
 * 我们一边遍历数组，一边把遍历过的数字和它的下标存进“哈希表”里。
 * 每次遇到一个新数字，先问问哈希表：“你这里面有没有我要的另一半？”
 * 
 * 涉及的 C++ 关键特性：
 * 1. vector<int>: 可以理解为“会自动扩容的动态数组”，用法和数组 nums[] 差不多。
 * 2. unordered_map<int, int>: 就是“哈希表”。
 *    - map[key] = value;  // 存数据
 *    - map.find(key);     // 查数据
 */

#include <vector>
#include <unordered_map>
using namespace std;

class Solution {
public:
    // vector<int>& nums: 引用传递，相当于 C 语言传指针，不会拷贝整个数组，速度快
    vector<int> twoSum(vector<int>& nums, int target) {
        
        // 【C++ 语法】声明哈希表
        // <> 里的两个 int 分别代表 Key(数值) 和 Value(下标) 的类型
        // 相当于 C 语言里你需要手写一个 struct HashTable { int key; int val; ... }
        unordered_map<int, int> map;
        
        // 1. 遍历数组
        // nums.size() 获取数组长度。在 C++ vector 中，你不需要额外传 int numsSize
        for (int i = 0; i < nums.size(); ++i) {
            
            // 2. 计算我们在找的“另一半”数字
            int complement = target - nums[i];
            
            // 3. 【关键】查询哈希表
            // map.find(key) 会返回一个“迭代器”(iterator)，你可以把它想象成一个指针。
            // map.end() 是一个特殊的标志，表示“查找到了末尾也没找到”。
            // 所以 if (map.find(...) != map.end()) 翻译成人话就是：“如果在表里找到了”
            if (map.find(complement) != map.end()) {
                
                // 4. 找到了！返回结果
                // map[complement] 获取存好的那个下标，i 是当前下标
                // {a, b} 是 C++11 的语法，直接构造并返回一个包含这两个数的 vector
                // 相当于 C 语言：int* ret = malloc...; ret[0]=...; return ret;
                return {map[complement], i};
            }
            
            // 5. 没找到，将当前数字存入哈希表
            // Key 是数字数值 (nums[i])，Value 是它的下标 (i)
            // 这样之后遍历到别的数时，就能查到当前这个数了
            map[nums[i]] = i;
        }
        
        return {}; // 理论上必然有解，这里返回空数组仅为了语法完整
    }
};
