/**
 * LeetCode 1. 两数之和 - C 语言哈希表解法 (纯手写实现)
 *
 * ⚠️ 注意：
 * C 语言标准库没有哈希表 (Map)，所以我们需要自己造轮子！
 * 这就是为什么刷题时大家更喜欢 C++/Java/Python 的原因 —— 工具齐全。
 * 
 * 下面我们实现一个简单的【链地址法哈希表】。
 */

#include <stdio.h>
#include <stdlib.h>

// 定义哈希节点
struct HashNode {
    int key;            // 存数值 (nums[i])
    int value;          // 存下标 (i)
    struct HashNode* next; // 拉链法解决冲突
};

// 定义哈希表结构
struct HashMap {
    struct HashNode** buckets; // 桶数组
    int size;                  // 桶的大小
};

// 哈希函数：把任意整数映射到 [0, size-1] 的范围内
int hash(int key, int size) {
    // abs 取绝对值，防止负数下标
    return abs(key) % size;
}

// 创建哈希表
struct HashMap* createHashMap(int size) {
    struct HashMap* map = (struct HashMap*)malloc(sizeof(struct HashMap));
    map->size = size;
    // 使用 calloc 初始化，确保所有指针为 NULL
    map->buckets = (struct HashNode**)calloc(size, sizeof(struct HashNode*));
    return map;
}

// 插入数据 put(key, value)
void put(struct HashMap* map, int key, int value) {
    int idx = hash(key, map->size);
    
    // 头插法：新节点直接插在链表头部，最快
    struct HashNode* newNode = (struct HashNode*)malloc(sizeof(struct HashNode));
    newNode->key = key;
    newNode->value = value;
    newNode->next = map->buckets[idx];
    map->buckets[idx] = newNode;
}

// 查找数据 get(key)
// 返回 -1 表示没找到，否则返回对应的下标 (value)
// 注意：这里假设下标都是非负的，所以用 -1 代表无效
int get(struct HashMap* map, int key) {
    int idx = hash(key, map->size);
    struct HashNode* curr = map->buckets[idx];
    
    while (curr != NULL) {
        if (curr->key == key) {
            return curr->value;
        }
        curr = curr->next;
    }
    return -1; // 没找到
}

// 释放哈希表内存（虽然刷题时不释放也不会报错，但好习惯很重要）
void freeHashMap(struct HashMap* map) {
    for (int i = 0; i < map->size; i++) {
        struct HashNode* curr = map->buckets[i];
        while (curr != NULL) {
            struct HashNode* temp = curr;
            curr = curr->next;
            free(temp);
        }
    }
    free(map->buckets);
    free(map);
}

// --- 以上是造轮子，下面才是两数之和的代码 ---

int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    // 1. 初始化哈希表
    // 桶的大小设为 numsSize 在做题时通常够用，能保证冲突不太多
    struct HashMap* map = createHashMap(numsSize);
    
    int* result = (int*)malloc(sizeof(int) * 2);
    *returnSize = 0; // 默认 0
    
    for (int i = 0; i < numsSize; i++) {
        int complement = target - nums[i];
        
        // 2. 查表：看看之前有没有存过另一半
        int foundIndex = get(map, complement);
        
        if (foundIndex != -1) {
            // 找到了！
            result[0] = foundIndex;
            result[1] = i;
            *returnSize = 2;
            
            // 记得释放内存
            freeHashMap(map);
            return result;
        }
        
        // 3. 没找到：把自己存进去
        put(map, nums[i], i);
    }
    
    // 没找到（理论上不会执行）
    freeHashMap(map);
    return NULL;
}
